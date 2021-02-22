import logging

from RouterConfiguration.Cisco.cisco_config_features import *


def get_index_from_args(router, feature, args):
    """
    Generates the index (and thereby equivalence class) for parameter values passed to router feature triplets
    :param router: Router for the current feature
    :param feature: Configuration feature, currently only Cisco configuration features are supported
    :param args: Parameter value used
    :return: index of args in router.get_possible_args()[feature], if it is not present the "middle" value is used as
     default
    """
    if args == -1:
        return -1

    try:
        return router.get_possible_args()[feature].index(args)
    except ValueError:
        if feature == OSPFFeatures.MAX_METRIC:
            (ext, stub, summary) = args
            if ext not in ['', ' external-lsa 1', ' external-lsa 1000', ' external-lsa 16777215']:
                ext = ' external-lsa 1000'
            if summary not in ['', ' summary-lsa 1', ' summary-lsa 1000', ' summary-lsa 16777215']:
                summary = ' summary-lsa 1000'
            return router.get_possible_args()[feature].index((ext, stub, summary))
        elif feature == OSPFFeatures.AREA_RANGE:
            (net, adv, cost) = args
            return router.get_possible_args()[feature].index((net, adv, ' cost 100'))
        elif feature == OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE:
            (metric, t) = args
            return router.get_possible_args()[feature].index((' metric 100', t))
        elif feature == BGPFeatures.DISTANCE_BGP:
            (dist1, dist2, dist3) = args
            if dist1 != 1 and dist1 != 255:
                dist1 = 100
            if dist2 != 1 and dist2 != 255:
                dist2 = 100
            if dist3 != 1 and dist3 != 255:
                dist3 = 100
            return router.get_possible_args()[feature].index((dist1, dist2, dist3))
        elif feature == RouteMapFeatures.SET_METRIC:
            (metric, ) = args
            if metric < 0:
                return 1
            else:
                return 2
        elif feature == RouteMapFeatures.SET_FEATURE_BGP_IN:
            f = args[0]
            a = args[1:]
            return get_index_from_args(router, f, a)
        elif feature == RouteMapFeatures.SET_FEATURE_BGP_OUT:
            f = args[0]
            a = args[1:]
            return get_index_from_args(router, f, a)
        else:
            return 1


def get_coverage(router_features, rows, possible_args, extra_features=lambda feature: False):
    """
    Generates pairwise coverage information for a given set of router feature triplets as well as a list of rows
    containing parameter values
    :param router_features: List of router feature triplets
    :param rows: Rows which each map each router feature triplet to a parameter value
    :param possible_args: A dict mapping containing all possible parameter values for a given feature
    :param extra_features: function which returns True if the given feature should have an extra value representing
        "invalid" configurations. This is used only for the random baseline, in particular to represent for example
        using a route-map which is not actually defined on the router
    :return: The total number of unique pairs in router_features as well as the number of unique pairs covered by rows
    """
    covered_pairs = {(f1, f2): set() for f1 in router_features for f2 in router_features if f1 != f2}

    def num_feature_args(feature):
        if extra_features(feature):
            return len(possible_args[feature]) + 2
        else:
            return len(possible_args[feature]) + 1

    num_pairs = {((r1, f1, arg1), (r2, f2, arg2)): num_feature_args(f1) * num_feature_args(f2)
                 for (r1, f1, arg1) in router_features for (r2, f2, arg2) in router_features if
                 (r1, f1, arg1) != (r2, f2, arg2)}

    coverage = []

    for row in rows:
        for f1 in row:
            for f2 in row:
                if f1 != f2:
                    covered_pairs[f1, f2].add((row[f1], row[f2]))

        covered = 0
        for p in covered_pairs:
            covered = covered + len(covered_pairs[p])

        coverage.append(covered)

    total = 0
    for p in num_pairs:
        total = total + num_pairs[p]

    return total, coverage
