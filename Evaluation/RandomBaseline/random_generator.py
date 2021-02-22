import random

from Evaluation.RandomBaseline import random_feature_args, network_representation
from test_generator import TestGenerationEngine
from test_runner import TestRunner


class RandomBaselineGenerator(TestGenerationEngine):
    def __init__(self, features, possible_args, num_tests):
        super().__init__(features, possible_args)
        self.num_tests = num_tests

    def generate(self):
        """
        Random generation does not require any pre-initialization
        """
        pass

    def next_test(self):
        """
        Generates the next random tests
        :return: Dict mapping router feature triplets to appropriate parameters
        """
        if self.index < self.num_tests:
            args = {(router, f, arg): random.choices([-1, random_feature_args.get_random_args()[f]])[0]
                    for (router, f, arg) in self.features}
            self.index = self.index + 1
            return args
        else:
            return None


class RandomTestRunner(TestRunner):
    def __init__(self, path, topo, system, router_features=None):
        """

        :param path: Subdirectory where all tests and results are saved
        :param topo: The topology which is being tested
        :param system: The system under test
        :param router_features: Features of the different routers in triplet format
        """
        super().__init__(path, topo, system, router_features)

    def run_test(self, cur_features, cur_args=None):
        """
        Runs tests like the regular TestRunner, the only difference is that a Batfish layer 1 topology file is created
        first to ensure that Batfish uses the correct physical topology
        :param cur_features: Features used by the current test
        :param cur_args: Arguments to the features, if not provided the last arguments will be used
        """
        self.topo.to_batfish_json(f'{self.path}test{self.test_num}/')
        super().run_test(cur_features, cur_args)


def init(path, t, system, num, allowed_features=None):
    """
    Init function for the random baseline, uses the RandomTopology instead of the regular topology type which does
    not enforce any semantic rules
    :param path: Directory where tests are generated
    :param t: Keyword arguments passed to the random topology
    :param system: System used, only tested with Batfish
    :param num: number of tests to generate
    :param allowed_features: optional restriction on allowed features
    :return: Test runner, list of all possible router feature triplets, as well as possible boundary value
        arguments to these triplets (unused in the case of the random baseline, however it is still returned for
        consistency with other init functions)
    """
    topo = network_representation.RandomTopology(**t)
    router_features = [f for r in topo.routers for f in r.get_supported_features(allowed_features)]
    runner = RandomTestRunner(path, topo, system, router_features)
    runner.test_num = num
    possible_args = {f: r.get_possible_args(allowed_features)[f] for r in topo.routers for f in r.get_possible_args(allowed_features)}

    return runner, router_features, possible_args
