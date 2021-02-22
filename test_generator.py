import random

import pict_model_generator


def translate_args(row_features):
    """
    Translates arguments which are specified as index in the list of possible values to actual parameter values
    :param row_features: row dictionary mapping (router, feature, arg) triplets to parameter indices
    :return: row_features where the indices are replaced by the value of the possible arguments for the particular
        feature at the specific index
    """
    args = {}

    for (router, feature, arg) in row_features:
        if row_features[router, feature, arg] == -1:
            args[router, feature, arg] = -1
        else:
            args[router, feature, arg] = router.get_possible_args()[feature][row_features[router, feature, arg]]

    return args


class TestGenerationEngine:

    """
    General test generation engine for use with Metha
    """

    def __init__(self, features, possible_args):
        self.index = 0
        self.features = features
        self.possible_args = possible_args

    def generate(self):
        """
        Performs initial preprocessing steps to test generation where applicable
        """
        raise NotImplementedError

    def next_test(self):
        """
        Generates the next test and returns it as a mapping of (router, feature, arg) triplets to parameter values
        """
        raise NotImplementedError


class RandomTestGenerator(TestGenerationEngine):

    """
    Random test generator. This is used for the semantic Metha baseline in the Metha paper.
    """

    def __init__(self, features, possible_args, num_tests):
        """

        :param features: (router, feature, arg) triplets used by this generator
        :param possible_args: boundary values for all features
        :param num_tests: number of tests to generate
        """
        super().__init__(features, possible_args)
        self.num_tests = num_tests

    def generate(self):
        """
        No preprocessing necessary for random generation
        """
        pass

    def next_test(self):
        """
        Randomly assigns parameter values from the entire parameter space
        :return: Argument dictionary or None if we generated all tests
        """
        if self.index < self.num_tests:
            args = {(router, f, arg): random.choices([-1, router.get_random_args()[f]], weights=[10, 1])[0] for
                    (router, f, arg) in self.features}
            self.index = self.index + 1
            return args
        else:
            return None


class BoundedTestGenerator(TestGenerationEngine):

    """
    Test generator which randomly assigns parameter values from the boundary value space.
    Corresponds to bounded Metha in the Metha paper.
    """

    def __init__(self, features, possible_args, num_tests):
        """

        :param features: (router, feature, arg) triplets used by this generator
        :param possible_args: possible boundary values for all features
        :param num_tests: number of tests to generate
        """
        super().__init__(features, possible_args)
        self.num_tests = num_tests

    def generate(self):
        """
        No preprocessing necessary, tests are generated at random
        """
        pass

    def next_test(self):
        """
        Randomly assigns parameter values from the boundary value space and returns the assignment
        :return: Argument dictionary assigning values to all features or None if all tests have been generated
        """
        if self.index < self.num_tests:
            row_features = {(router, f, arg): random.choices([-1, random.randrange(0, len(self.possible_args[f]))],
                                                             weights=[10, 1])[0]
                            for (router, f, arg) in self.features}
            args = translate_args(row_features)
            self.index = self.index + 1
            return args
        else:
            return None


class CombinatorialTestGenerator(TestGenerationEngine):

    """
    Combinatorial test generator. Corresponds to full Metha in the Metha paper.
    """

    def __init__(self, features, possible_args, pict_model, pict_output):
        """

        :param features: (router, feature, arg) triplets used by this generator
        :param possible_args: possible boundary values for all features
        :param pict_model: location where the PICT model is saved to disk
        :param pict_output: location where the PICT output is saved to disk
        """
        super().__init__(features, possible_args)
        self.str_features = None
        self.pict_matrix = None
        self.pict_model = pict_model
        self.pict_output = pict_output

    def generate(self):
        """
        Generate the PICT model according to self.features and self.possible_args, call PICT and read output
        """
        possible_values = pict_model_generator.generate_model(self.features, self.possible_args)
        self.str_features = pict_model_generator.write_model(self.pict_model, possible_values)
        self.pict_matrix = pict_model_generator.call_pict(self.pict_model, self.pict_output)

    def next_test(self):
        """
        Get the next test from the PICT results
        :return: Parameter values assignment for all features or None if the entire PICT matrix has been processed
        """
        if self.index < len(self.pict_matrix.index):
            row = self.pict_matrix.iloc[self.index]
            row_features = {f: int(row[self.str_features[f]]) for f in self.features}
            args = translate_args(row_features)
            self.index = self.index + 1
            return args
        else:
            return None
