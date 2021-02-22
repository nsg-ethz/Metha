import os
import logging
import glob

import network_features
from Evaluation.RandomBaseline.random_generator import RandomBaselineGenerator
from Evaluation.RandomBaseline import random_generator
import delta_debugging
from RouterConfiguration.Cisco.cisco_config_features import RouteMapFeatures

from GNS3.router_types import *
from settings import TOPOLOGY_PATH, MAX_BASE_TESTS
from utils import *


def read_topo_from_file(path):
    """
    Reads the topology file located at path and returns a dict representation of this topology
    :param path: path to the location of the topology file
    :return: topology located at path as dict
    """
    with open(path) as f:
        topo = json.load(f)
        topo['router_types'] = list(map(router_type_from_string, topo['router_types']))
        if 'protocols' in topo:
            topo['protocols'] = list(
                map(lambda l: list(map(network_features.protocol_from_string, l)), topo['protocols']))
        if 'name' not in topo:
            topo['name'] = os.path.basename(path)

    return topo


def load_topologies():
    """
    Loads topologies from path specified in the config. All json files in the specified path are considered to be
    valid topologies, will crash if a json file does not follow the topology format.

    :return: List of topologies as Dict
    """
    topo_files = [f for f in glob.glob(f'{TOPOLOGY_PATH}/**/*.json', recursive=True)]
    topologies = []

    for topo in topo_files:
        t = read_topo_from_file(topo)
        topologies.append(t)

    return topologies


def cached_test(runner, cur_f, cache=None):
    """
    Run a test only if this configuration has not been tested before, otherwise read it from the cache
    :param runner: Test runner
    :param cur_f: Enabled features to run the test
    :param cache: Cache in the form of a dictionary indexed by frozensets of enabled features
    :return: Result of the test with enabled features cur_f
    """
    if cache is not None:
        if frozenset(cur_f) in cache:
            return cache[frozenset(cur_f)]
        else:
            cache[frozenset(cur_f)] = runner.run_test(cur_f)
            return cache[frozenset(cur_f)]
    else:
        return runner.run_test(cur_f)


def check_base_case(runner, features, possible_args, init):
    """
    Check if the base configuration (i.e. all features are disabled, only base configuration such as interface config,
     AS assignment, area assignment, etc.) runs without issues. If the base config does not work, rerun until either
     MAX_BASE_TESTS checks are performed or a suitable base configuration is found
    :param runner: TestRunner object to start with
    :param features: Configuration features
    :param possible_args: Possible boundary values for the features
    :param init: Initialization function used to reinitialize the arguments if the base case is faulty, must only take
        an int for the next test_num to generate as input
    :return: tuple (ok, min_subsets, runner, features, possible_args) where ok represents if a suitable base config
        was found, min_subsets is a starting set of minimal faulty configs, and runner, feature, possible_args
        represent the newest base configuration
    """
    logger = logging.getLogger('network-testing')
    checked_tests = 0
    min_subsets = set()

    while runner.run_test([]) and checked_tests < MAX_BASE_TESTS:
        logger.info(f'Found bug in base setup test case\n')
        runner, features, possible_args = init(runner.test_num)

        min_subsets = {frozenset()}
        checked_tests = checked_tests + 1

    return checked_tests < MAX_BASE_TESTS, min_subsets, runner, features, possible_args


def find_minimal_subsets(runner, cur_features, min_subsets):
    """
    Finds all minimal failure-inducing subsets of features from a starting set of features, minimal subsets are saved
    JSON format on disk
    :param runner: TestRunner for the test case to be minimized
    :param cur_features: Initially enabled features
    :param min_subsets: Previously identified minimal subsets
    """
    test_pref = runner.test_num
    logger = logging.getLogger('network-testing')

    cache = {}

    min_sets = delta_debugging.ddmin_iter(
        list(get_unique_features(cur_features)),
        lambda f: cached_test(runner, filter_features(cur_features, f), cache),
        lambda f: cached_test(runner, f, cache),
        lambda f: filter_features(cur_features, f)
    )

    logger.info(f'Found minimal feature sets: {str_repr(min_sets)}')
    for fs in min_sets:
        for (router, feature, arg) in fs:
            if feature in [RouteMapFeatures.SET_FEATURE_BGP_IN, RouteMapFeatures.SET_FEATURE_BGP_OUT]:
                fs.remove((router, feature, arg))
                fs.append((router, router.features[feature, arg][2], arg))
        min_subsets.add(frozenset(get_unique_features(fs)))
    test_next = runner.test_num
    logger.info(f'Minimized after {test_next - test_pref} iterations')

    write_json(min_subsets, f'{runner.path}../results/minimum_subsets_{runner.topo.name}.json')


def generate_tests(topos, init, test_gen, get_kwargs):
    """
    Generates tests starting with an initialization function for the base configuration and a test generator
    to generate test cases on top of the base configuration
    :param topos: Topology definitions for which tests are generated
    :param init: Initialization function, must return a TestRunner, a list of features, and possible boundary values for
        all features from a topology definition and a starting test number
    :param test_gen: TestGenerator which is instantiated to generate new tests
    :param get_kwargs: function which returns kwargs for test_gen based on the current topology definition
    """
    test_num = 0

    for t in topos:

        runner, features, possible_args = init(t, test_num)

        ok, min_subsets, runner, features, possible_args = check_base_case(runner, features, possible_args, lambda num: init(t, num))

        if not ok:
            test_num = runner.test_num
            continue

        kwargs = get_kwargs(t)
        generator = test_gen(features, possible_args, **kwargs)
        generator.generate()
        args = generator.next_test()

        while args:
            runner.set_router_args(args)
            cur_features = [f for f in features if args[f] != -1]
            res = runner.run_test(cur_features, args)

            if res:
                find_minimal_subsets(runner, cur_features, min_subsets)

            args = generator.next_test()

        test_num = runner.test_num


def generate_random_baseline_tests(topos, tests_per_topo, path, system, allowed_features=None):
    """
    Generates random baseline tests
    :param topos: Topology definitions used to generate tests
    :param tests_per_topo: Number of tests generated per topology
    :param path: Path where the generated tests are saved
    :param system: System to use for testing
    :param allowed_features: Optional restriction on allowed configuration features
    """
    test_gen = RandomBaselineGenerator

    def init(t, num):
        return random_generator.init(path, t, system, num, allowed_features)

    def get_kwargs(t):
        return {'num_tests': tests_per_topo}

    generate_tests(topos, init, test_gen, get_kwargs)


def generate_metha_tests(topos, path, system, test_gen, get_kwargs, allowed_features=None):
    """
    Generates Metha tests
    :param topos: Topology definitions used to generate tests
    :param path: Path where the generated tests are saved
    :param system: System to use for testing
    :param test_gen: TestGenerator to use to genenerate tests
    :param get_kwargs: Function which returns additonaly kwargs to be passed to test_gen based on the current topology
    :param allowed_features: Optional restriction on allowed configuration features
    """
    def init(t, num):
        return system.init_runner(path, t, num, allowed_features)

    generate_tests(topos, init, test_gen, get_kwargs)
