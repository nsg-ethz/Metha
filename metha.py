import argparse
import logging
import os

import rt_comparator
import test_coordinator
from Evaluation import eval_metrics
from GNS3 import gns3_interface
from GNS3.Nodes.pyez_node import PyEZNode
from GNS3.router_types import RouterTypes
from RouterConfiguration import feature_parser
from Systems.Batfish import batfish_interface
from Systems.CBGP import cbgp_interface
from Systems.NV import nv_interface
from test_generator import CombinatorialTestGenerator, BoundedTestGenerator, RandomTestGenerator
from utils import filter_optional


"""
Read a system from a string
"""
system_from_string = {
    'batfish': batfish_interface.BatfishInterface(),
    'cbgp': cbgp_interface.CBGPInterface(),
    'nv': nv_interface.NVInterface()
}


def enable_logging():
    """
    Enables both Metha logging as well as netmiko logging
    :return: Metha logger
    """
    handler = logging.FileHandler('netmiko.log')
    handler.setLevel(logging.DEBUG)
    netmiko_logger = logging.getLogger('netmiko')
    netmiko_logger.addHandler(handler)
    netmiko_logger.setLevel(logging.DEBUG)
    handler_debug = logging.FileHandler('network-testing-debug.log')
    handler_debug.setLevel(logging.DEBUG)
    handler_info = logging.FileHandler('network-testing-info.log')
    handler_info.setLevel(logging.INFO)
    logger = logging.getLogger('network-testing')
    logger.addHandler(handler_debug)
    logger.addHandler(handler_info)
    logger.setLevel(logging.DEBUG)

    return logger


def get_allowed_features(args):
    """
    Generates a list of allowed features if any feature restriction is passed as command-line argument, otherwise returns None
    :param args: Argument namespace from argparse
    :return: Either a list of allowed configuration features or None if all features are allowed
    """
    allowed_features = None
    if args.allowed_features is not None:
        allowed_features = feature_parser.parse_feature_list(args.allowed_features)

    if args.disabled_features is not None:
        allowed_features = filter_optional(feature_parser.parse_feature_list(args.disabled_features, disable_list=True),
                                           allowed_features)

    return allowed_features


def get_dir(path):
    """
    Get the absolute path to the directory at path
    :param path: Location of a directory
    :return: Absolute path to this directory
    """
    return os.path.abspath(path) + '/'


def run_gns(args):
    """
    Runs GNS3 using provided configuration files
    :param args: Argument namespace from argparse
    """
    gp, adj = gns3_interface.init_gns_from_files(get_dir(args.path))
    for name in gp.nodes:
        node = gp.nodes[name]
        if issubclass(type(node), PyEZNode):
            node.pyez_connection.close()
            node.pyez_connection = None

    print('Running GNS3')
    input('Press any key to stop execution')


def run_single_test(args):
    """
    Compares the routing tables computed using provided configurations
    :param args: Argument namespace from argparse
    """
    sys = system_from_string[args.system]
    gp, adj = gns3_interface.init_gns_from_files(args.path)
    rt_comparator.run_comparison(get_dir(args.path), gp, adj, sys)


def get_config_features(args):
    """
    Creates a JSON file containing all possible configuration features
    :param args: Argument namespace from argparse
    """
    os.makedirs(get_dir(args.path), exist_ok=True)
    feature_parser.write_all_features(get_dir(args.path))


def random_base(args):
    """
    Run the random baseline
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
        keys = ['name', 'num_nodes', 'links', 'router_types']
        topo = {key: topo[key] for key in keys}
    else:
        topo = {
            'num_nodes': 4,
            'links': [(0, 1), (0, 2), (0, 3)],
            'router_types': [RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200]
        }
    topos = [topo]

    allowed_features = get_allowed_features(args)

    if args.num_tests is None:
        n = 1794
    else:
        n = args.num_tests

    test_coordinator.generate_random_baseline_tests(topos, n, get_dir(args.path), sys, allowed_features)


def semantic(args):
    """
    Run semantic Metha
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
    else:
        topo = {
            'num_nodes': 4,
            'num_ases': 2,
            'num_areas': 2,
            'links': [(0, 1), (0, 2), (0, 3)],
            'ospf_areas': [0, 1, None],
            'ases': [0, 0, 0, 1],
            'router_types': [RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200]
        }
    topos = [topo]

    allowed_features = get_allowed_features(args)

    if args.num_tests is None:
        n = 1794
    else:
        n = args.num_tests

    test_coordinator.generate_metha_tests(
        topos,
        get_dir(args.path),
        sys,
        RandomTestGenerator,
        lambda t: {
            'num_tests': n,
        },
        allowed_features
    )


def bounded(args):
    """
    Run bounded Metha
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
    else:
        topo = {
            'num_nodes': 4,
            'num_ases': 2,
            'num_areas': 2,
            'links': [(0, 1), (0, 2), (0, 3)],
            'ospf_areas': [0, 1, None],
            'ases': [0, 0, 0, 1],
            'router_types': [RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200]
        }
    topos = [topo]

    allowed_features = get_allowed_features(args)

    if args.num_tests is None:
        n = 1794
    else:
        n = args.num_tests

    test_coordinator.generate_metha_tests(
        topos,
        get_dir(args.path),
        sys,
        BoundedTestGenerator,
        lambda t: {
            'num_tests': n,
        },
        allowed_features
    )


def coverage(args):
    """
    Generate combinatorial coverage information
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
    else:
        topo = {
            'num_nodes': 4,
            'num_ases': 2,
            'num_areas': 2,
            'links': [(0, 1), (0, 2), (0, 3)],
            'ospf_areas': [0, 1, None],
            'ases': [0, 0, 0, 1],
            'router_types': [RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200, RouterTypes.Cisco7200]
        }
    topos = [topo]

    allowed_features = get_allowed_features(args)

    if args.num_tests is None:
        n = 1794
    else:
        n = args.num_tests

    eval_metrics.generate_coverage_information(topos, n, get_dir(args.path), sys, allowed_features)


def pict_time(args):
    """
    Benchmark PICT runtime
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
        topos = [topo]
    else:
        topos = test_coordinator.load_topologies()

    allowed_features = get_allowed_features(args)

    eval_metrics.check_pict_runtime(topos, get_dir(args.path), sys, allowed_features)


def run(args):
    """
    Run full Metha
    :param args: Argument namespace from argparse
    """
    os.makedirs(os.path.dirname(f'{get_dir(args.path)}../results/'), exist_ok=True)
    sys = system_from_string[args.system]

    if args.topology is not None:
        topo = test_coordinator.read_topo_from_file(args.topology)
        topos = [topo]
    else:
        topos = test_coordinator.load_topologies()

    allowed_features = get_allowed_features(args)

    test_coordinator.generate_metha_tests(
        topos,
        get_dir(args.path),
        sys,
        CombinatorialTestGenerator,
        lambda t: {
            'pict_model': f'{get_dir(args.path)}pict_model_{t["name"]}',
            'pict_output': f'{get_dir(args.path)}pict_output_{t["name"]}.csv'
        },
        allowed_features
    )


def main():
    """
    Parse command-line arguments and then call the corresponding functions
    """
    parser = argparse.ArgumentParser(description='Metha network analysis testing tool')
    parser.add_argument('--enable-logging', action='store_true')
    parser.add_argument('-p', '--path', required=True)

    subparsers = parser.add_subparsers()

    parser_single = subparsers.add_parser('single-test')
    parser_single.add_argument('-s', '--system', choices=list(system_from_string), required=True)
    parser_single.set_defaults(func=run_single_test)

    parser_gns = subparsers.add_parser('run-gns')
    parser_gns.set_defaults(func=run_gns)

    parser_features = subparsers.add_parser('get-config-features')
    parser_features.set_defaults(func=get_config_features)

    parser_eval = subparsers.add_parser('eval')
    parser_eval.add_argument('-s', '--system', choices=list(system_from_string), default='batfish')
    parser_eval.add_argument('--allowed-features')
    parser_eval.add_argument('--disabled-features')
    parser_eval.add_argument('-t', '--topology')
    subparsers_eval = parser_eval.add_subparsers()

    parser_random_base = subparsers_eval.add_parser('random-base')
    parser_random_base.add_argument('-n', '--num-tests', type=int)
    parser_random_base.set_defaults(func=random_base)

    parser_semantic = subparsers_eval.add_parser('semantic')
    parser_semantic.add_argument('-n', '--num-tests', type=int)
    parser_semantic.set_defaults(func=semantic)

    parser_bounded = subparsers_eval.add_parser('bounded')
    parser_bounded.add_argument('-n', '--num-tests', type=int)
    parser_bounded.set_defaults(func=bounded)

    parser_coverage = subparsers_eval.add_parser('coverage')
    parser_coverage.add_argument('-n', '--num-tests', type=int)
    parser_coverage.set_defaults(func=coverage)

    parser_pict_time = subparsers_eval.add_parser('pict-runtime')
    parser_pict_time.set_defaults(func=pict_time)

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('-s', '--system', choices=list(system_from_string), required=True)
    parser_run.add_argument('--allowed-features')
    parser_run.add_argument('--disabled-features')
    parser_run.add_argument('-t', '--topology')
    parser_run.set_defaults(func=run)

    args = parser.parse_args()

    if args.enable_logging:
        enable_logging()

    args.func(args)


if __name__ == '__main__':
    main()
