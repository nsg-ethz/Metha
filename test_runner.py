import concurrent.futures
import logging
import time
import traceback

from pybatfish.exception import BatfishException
from concurrent.futures import TimeoutError

from timeit import default_timer as timer

from RouterConfiguration import router_configurator
import rt_comparator
from GNS3 import gns3_interface
from settings import GNS_RESTART_INTERVAL
from utils import *


def get_delta_commands(routers, prev, new, prev_args=None, new_args=None):
    """
    Finds all features which need to change to switch from one test case to the next, and returns corresponding commands
    :param routers: Routers which are used in the current test iteration
    :param prev: Features which were enabled in the last run
    :param new: Features which should be enabled in the new run
    :param prev_args: Args used in the last run, if None features are only compared for enabled / disabled
    :param new_args: Args to be used in the next run, if None features are only compared for enabled / disabled
    :return: Commands to issue to the routers, dict indexed by router name
    """
    commands = {router.name: [] for router in routers}

    if prev_args is not None and new_args is not None:
        disable_features = [f for f in prev if prev_args[f] != new_args[f]]
        enable_features = [f for f in new if prev_args[f] != new_args[f]]
    else:
        enable_features = [f for f in new if f not in prev]
        disable_features = [f for f in prev if f not in new]

    router_configurator.disable_features(commands, disable_features)
    router_configurator.enable_features(commands, enable_features)

    return commands


def write_result(path, name, comp, p_err, init_err):
    """
    Write the result of a test successfully triggering a discrepancy to disk in the results folder
    :param path: Path used to run Metha
    :param name: Name of the test case triggering a discrepancy
    :param comp: Result of the datacompy comparison of the routing tables
    :param p_err: Optional dataframe of parsing errors
    :param init_err: Optional dataframe of initialization errors
    """
    if p_err is not None and not p_err.empty:
        with open(f'{path}../results/{name}_parse_errors.csv', 'w') as f:
            f.write(p_err.to_csv(index=False))
    if init_err is not None and not init_err.empty:
        with open(f'{path}../results/{name}_init_issues.csv', 'w') as f:
            f.write(init_err.to_csv(index=False))

    with open(f'{path}../results/{name}_report.txt', 'w') as f:
        f.write(comp.report())
    with open(f'{path}../results/{name}_GNS_only.csv', 'w') as f:
        f.write(comp.df2_unq_rows.to_csv(index=False))
    with open(f'{path}../results/{name}_SUT_only.csv', 'w') as f:
        f.write(comp.df1_unq_rows.to_csv(index=False))


def write_except(path, name):
    """
    Append the stacktrace of a test resulting in an exception to an accumulation file on disk
    :param path: Path of the file to append the stacktrace to
    :param name: Name of the test case which triggered the exception
    """
    with open(path, 'a') as f:
        f.write(f'{name}:\n')
        traceback.print_exc(file=f)
        f.write('\n\n')


class TestRunner:

    def __init__(self, path, topo, system, router_features=None):
        """

        :param path: Subdirectory where all tests and results are saved
        :param topo: The topology which is being tested
        :param system: The system under test
        :param router_features: Features of the different routers in triplet format
        """
        self.topo = topo
        self.path = path
        self.gp = self.set_up_testbed()
        self.test_num = 0
        self.system = system
        self.router_features = router_features
        if router_features is not None:
            self.last_args = {router_feature: -1 for router_feature in self.router_features}
        else:
            self.last_args = None

    def set_up_testbed(self):
        """
        Sets up the GNS3 project for this test run, including initial configuration of the routers
        :return: GNS3 project
        """
        for router in self.topo.routers:
            router.write_config(f'{self.path}base_configs/configs/')

        self.topo.to_json(f'{self.path}base_configs/')
        gp = gns3_interface.setup_gns_from_topology(f'{self.path}base_configs/topology.json')
        gp.start_nodes()

        return gp

    def restart_gns(self):
        """
        Deletes current GNS3 project and creates a new GNS3 project with freshly started routers
        """
        self.gp.delete()
        self.gp = self.set_up_testbed()
        if self.router_features is not None:
            self.last_args = {router_feature: -1 for router_feature in self.router_features}
        else:
            self.last_args = None
        for router in self.topo.routers:
            router.enabled_features = {}

    def configure_routers(self, configs):
        """
        Configure the GNS3 routers and write the resulting configs to disk
        :param configs: configurations for each router, dict indexed by router name
        """
        config_outputs = {}
        path = f'{self.path}test{self.test_num}'

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_node = {
                executor.submit(self.gp.nodes[node].send_config, configs[node]): self.gp.nodes[node] for node in
                self.gp.nodes
            }
            for future in concurrent.futures.as_completed(future_to_node):
                node = future_to_node[future]
                config_outputs[node.name] = future.result()
                executor.submit(node.write_config, f'{path}/configs/')

            executor.shutdown(wait=True)

        with open(f'{path}/configuration_outputs.txt', 'w') as f:
            for node in config_outputs:
                f.write(f'{node}\n')
                if config_outputs[node] is not None:
                    f.write(config_outputs[node])
                f.write('\n' * 3)

    def set_router_args(self, args):
        """
        Sets the feature arguments on routers
        :param args: arguments as dict from (router, feature, arg) triplets to parameter values
        """
        router_configurator.set_args_from_translation(args)

    def clear_routing_tables(self):
        """
        Clears the routing tables of the GNS3 routers
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            for node in self.gp.nodes:
                executor.submit(self.gp.nodes[node].clear_routing_table)

            executor.shutdown(wait=True)

        time.sleep(1)

    def run_test(self, cur_features, cur_args=None):
        """
        Run a test case with specified features and args
        :param cur_features: Features which should be enabled in this test case
        :param cur_args: Arguments for the enabled features, if None the last args are used instead
        :return: Result of the test: 0 if comparison ok, 1 for difference, 2 for sut crash, 3 for timeout
        """
        logger = logging.getLogger('network-testing')
        logger.info(f'Running test case with features {str_repr(cur_features)}')

        if self.test_num % GNS_RESTART_INTERVAL == GNS_RESTART_INTERVAL-1:
            self.restart_gns()

        start = timer()

        last_features = [(router, *f) for router in self.topo.routers for f in router.enabled_features]

        commands = get_delta_commands(self.topo.routers, last_features, cur_features, self.last_args, cur_args)
        self.configure_routers(commands)
        self.clear_routing_tables()

        try:
            (comp, p_err, init_err) = rt_comparator.run_comparison(
                f'{self.path}test{self.test_num}/',
                self.gp,
                self.topo.get_adjacency_info(),
                self.system
            )
            if comp.matches():
                res = 0
            else:
                write_result(self.path, f'test{self.test_num}', comp, p_err, init_err)
                res = 1
        except BatfishException:
            write_except(f'{self.path}../results/crashing_tests.txt', f'test{self.test_num}')
            res = 2
        except TimeoutError:
            write_except(f'{self.path}../results/timed_out_tests.txt', f'test{self.test_num}')
            res = 3

        end = timer()

        with open(f'{self.path}../results/total_runtimes.txt', 'a') as f:
            f.write(f'test{self.test_num}: {end - start}\n')

        self.test_num += 1
        self.last_args = cur_args

        return res
