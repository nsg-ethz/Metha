import random

import pandas as pd
from timeit import default_timer as timer

import pict_model_generator
from Evaluation import coverage
from Evaluation.RandomBaseline import random_feature_args, equivalence_classes


def generate_coverage_information(topos, tests_per_topo, path, system, allowed_features=None):
    """
    Generates coverage information for all four test methods: random baseline, Semantic Metha, Bounded Metha, and
    Full Metha
    :param topos: list of topologies, in the form of argument dictionaries, for which coverage information is generated
    :param tests_per_topo: number of tests per topology, this is used by the random selections as stopping criterion.
        Should generally be equal to the number of tests created by combinatorial testing, otherwise there will be a
        mismatch
    :param path: path where generated information is stored
    :param system: system for which the test configs are generated
    :param allowed_features: optional restriction on configuration features which are allowed
    """
    for t in topos:
        topo, runner, features, possible_args = system.init_runner(path, t, 0, allowed_features)

        rows_random_s = []
        rows_random = []
        rows_boundary = []
        rows_combinatorial = []

        for i in range(tests_per_topo):
            args = {(router, f, arg): random.choices([-1, random_feature_args.get_random_args()[f]])[0]
                    for (router, f, arg) in features}
            row_features = {(router, f, arg): equivalence_classes.get_equiv_class(router, f, args[router, f, arg])
                            for (router, f, arg) in features}
            rows_random_s.append(row_features)

        for i in range(tests_per_topo):
            args = {(router, f, arg): random.choices([-1, router.get_random_args()[f]], weights=[10, 1])[0] for
                    (router, f, arg) in features}
            row_features = {(router, f, arg): coverage.get_index_from_args(router, f, args[router, f, arg])
                            for (router, f, arg) in features}
            rows_random.append(row_features)

        for i in range(tests_per_topo):

            row_features = {(router, f, arg): random.choices([-1, random.randrange(0, len(possible_args[f]))],
                                                             weights=[10, 1])[0]
                            for (router, f, arg) in features}
            rows_boundary.append(row_features)

        possible_values = pict_model_generator.generate_model(features, possible_args)
        str_features = pict_model_generator.write_model(f'{path}pict_model_{t["name"]}', possible_values)
        pict_matrix = pict_model_generator.call_pict(f'{path}pict_model_{t["name"]}', f'{path}pict_output_{t["name"]}.csv')

        for i, row in pict_matrix.iterrows():
            row_features = {router_feature: int(row[str_features[router_feature]]) for router_feature in
                            features}
            rows_combinatorial.append(row_features)

        total_random_s, cov_random_s = coverage.get_coverage(features, rows_random_s, possible_args, equivalence_classes.get_extra_equiv_class)
        total_random, cov_random = coverage.get_coverage(features, rows_random, possible_args)
        total_boundary, cov_boundary = coverage.get_coverage(features, rows_boundary, possible_args)
        total_combinatorial, cov_combinatorial = coverage.get_coverage(features, rows_combinatorial, possible_args)

        coverage_random_s = pd.DataFrame(columns=['NumTests', 'Coverage'])
        for i, c in enumerate(cov_random_s):
            cov = {'NumTests': i, 'Coverage': (c / total_random_s) * 100}
            coverage_random_s = coverage_random_s.append(cov, ignore_index=True)

        with open(f'{path}../results/coverage_random_percentage_s.csv', 'w') as f:
            f.write(coverage_random_s.to_csv(index=False))

        coverage_random = pd.DataFrame(columns=['NumTests', 'Coverage'])
        for i, c in enumerate(cov_random):
            cov = {'NumTests': i, 'Coverage': (c / total_random) * 100}
            coverage_random = coverage_random.append(cov, ignore_index=True)

        with open(f'{path}../results/coverage_random_percentage.csv', 'w') as f:
            f.write(coverage_random.to_csv(index=False))

        coverage_boundary = pd.DataFrame(columns=['NumTests', 'Coverage'])
        for i, c in enumerate(cov_boundary):
            cov = {'NumTests': i, 'Coverage': (c / total_random) * 100}
            coverage_boundary = coverage_boundary.append(cov, ignore_index=True)

        with open(f'{path}../results/coverage_boundary_percentage.csv', 'w') as f:
            f.write(coverage_boundary.to_csv(index=False))

        coverage_combinatorial = pd.DataFrame(columns=['NumTests', 'Coverage'])
        for i, c in enumerate(cov_combinatorial):
            cov = {'NumTests': i, 'Coverage': (c / total_random) * 100}
            coverage_combinatorial = coverage_combinatorial.append(cov, ignore_index=True)

        with open(f'{path}../results/coverage_combinatorial_percentage.csv', 'w') as f:
            f.write(coverage_combinatorial.to_csv(index=False))

        with open(f'{path}../results/coverage_random_s_{t["name"]}.txt', 'w') as f:
            for i, c in enumerate(cov_random_s):
                f.write(f'Coverage {i}: {c}/{total_random_s}\n')

        with open(f'{path}../results/coverage_random_{t["name"]}.txt', 'w') as f:
            for i, c in enumerate(cov_random):
                f.write(f'Coverage {i}: {c}/{total_random}\n')

        with open(f'{path}../results/coverage_boundary_{t["name"]}.txt', 'w') as f:
            for i, c in enumerate(cov_boundary):
                f.write(f'Coverage {i}: {c}/{total_boundary}\n')

        with open(f'{path}../results/coverage_combinatorial_{t["name"]}.txt', 'w') as f:
            for i, c in enumerate(cov_combinatorial):
                f.write(f'Coverage {i}: {c}/{total_combinatorial}\n')


def check_pict_runtime(topos, path, system, allowed_features=None):
    """
    Generates a simple benchmark by running PICT on a set of topologies and reporting the time used to generate the
    combinatorial test suite
    :param topos: topology definitions used in dictionary form
    :param path: path to store test information
    :param system: system for which configs are generated
    :param allowed_features: optional restriction on allowed configuration features
    """
    test_num = 0

    for t in topos:
        topo, runner, features, possible_args = system.init_runner(path, t, test_num, allowed_features)

        start = timer()

        possible_values = pict_model_generator.generate_model(features, possible_args)
        str_features = pict_model_generator.write_model(f'{path}pict_model_{t["name"]}', possible_values)
        pict_matrix = pict_model_generator.call_pict(f'{path}pict_model_{t["name"]}', f'{path}pict_output_{t["name"]}.csv')

        end = timer()

        with open(f'{path}../results/PICT_runtime.txt', 'a') as f:
            f.write(f'{t["name"]}: {end - start}\n')

        test_num = runner.test_num
