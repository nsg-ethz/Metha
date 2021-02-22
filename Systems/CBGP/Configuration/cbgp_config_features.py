from enum import Enum, auto


class GlobalFeatures(Enum):
    LOCAL_PREF = auto()
    MED = auto()


class RouterFeatures(Enum):
    NEXT_HOP = auto()
    NEXT_HOP_SELF = auto()
    IGP_WEIGHT = auto()
    STATIC_ROUTE = auto()


class FilterFeatures(Enum):
    ACTION_ACCEPT = auto()
    ACTION_DENY = auto()
    ACTION_CALL = auto()
    ACTION_JUMP = auto()
    ACTION_LOCAL_PREF = auto()
    ACTION_METRIC = auto()
    ACTION_METRIC_INTERNAL = auto()
    ACTION_COMMUNITY_ADD = auto()
    ACTION_COMMUNITY_STRIP = auto()
    ACTION_COMMUNITY_REMOVE = auto()
    ACTION_AS_PATH_PREPEND = auto()
    ACTION_AS_PATH_REMOVE_PRIVATE = auto()
    ACTION_RED_COMMUNITY_ADD = auto()
    MATCH_ANY = auto()
    MATCH_COMMUNITY = auto()
    MATCH_NEXT_HOP = auto()
    MATCH_NEXT_HOP_IN = auto()
    MATCH_PREFIX = auto()
    MATCH_PREFIX_IN = auto()
    MATCH_PATH = auto()
    FILTER_ACTION_IN = auto()
    FILTER_ACTION_OUT = auto()
    FILTER_MATCH_IN = auto()
    FILTER_MATCH_OUT = auto()


def filter_unsupported(feature_list):

    unsupported_features = [
        FilterFeatures.ACTION_CALL,
        FilterFeatures.ACTION_JUMP,
        FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE,
        FilterFeatures.ACTION_RED_COMMUNITY_ADD,
        FilterFeatures.MATCH_NEXT_HOP_IN,
        FilterFeatures.MATCH_PREFIX,
        FilterFeatures.MATCH_PREFIX_IN,
        RouterFeatures.NEXT_HOP,
    ]

    faulty_features = []

    return list(filter(lambda f: f not in unsupported_features + faulty_features, feature_list))


feature_type = {
    'GlobalFeatures': GlobalFeatures,
    'RouterFeatures': RouterFeatures,
    'FilterFeatures': FilterFeatures,
}


filter_action_features_in = filter_unsupported([
    FilterFeatures.ACTION_ACCEPT, FilterFeatures.ACTION_DENY, FilterFeatures.ACTION_CALL,
    FilterFeatures.ACTION_JUMP, FilterFeatures.ACTION_LOCAL_PREF, FilterFeatures.ACTION_METRIC,
    FilterFeatures.ACTION_METRIC_INTERNAL, FilterFeatures.ACTION_COMMUNITY_ADD, FilterFeatures.ACTION_COMMUNITY_STRIP,
    FilterFeatures.ACTION_COMMUNITY_REMOVE, FilterFeatures.ACTION_AS_PATH_PREPEND,
    FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE, FilterFeatures.ACTION_RED_COMMUNITY_ADD
])

filter_action_features_out = filter_unsupported([
    FilterFeatures.ACTION_ACCEPT, FilterFeatures.ACTION_DENY, FilterFeatures.ACTION_CALL,
    FilterFeatures.ACTION_JUMP, FilterFeatures.ACTION_LOCAL_PREF, FilterFeatures.ACTION_METRIC,
    FilterFeatures.ACTION_METRIC_INTERNAL, FilterFeatures.ACTION_COMMUNITY_ADD, FilterFeatures.ACTION_COMMUNITY_STRIP,
    FilterFeatures.ACTION_COMMUNITY_REMOVE, FilterFeatures.ACTION_AS_PATH_PREPEND,
    FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE, FilterFeatures.ACTION_RED_COMMUNITY_ADD
])

filter_match_features_in = filter_unsupported([
    FilterFeatures.MATCH_ANY, FilterFeatures.MATCH_COMMUNITY, FilterFeatures.MATCH_PREFIX, FilterFeatures.MATCH_PREFIX_IN,
    FilterFeatures.MATCH_PATH
])

filter_match_features_out = filter_unsupported([
    FilterFeatures.MATCH_ANY, FilterFeatures.MATCH_COMMUNITY, FilterFeatures.MATCH_NEXT_HOP,
    FilterFeatures.MATCH_NEXT_HOP_IN, FilterFeatures.MATCH_PREFIX, FilterFeatures.MATCH_PREFIX_IN,
    FilterFeatures.MATCH_PATH
])

global_features = filter_unsupported(list(GlobalFeatures))
router_features = filter_unsupported([RouterFeatures.STATIC_ROUTE])
neighbour_features = filter_unsupported([RouterFeatures.NEXT_HOP, RouterFeatures.NEXT_HOP_SELF])
interface_features = filter_unsupported([RouterFeatures.IGP_WEIGHT])

all_features = global_features + router_features + [FilterFeatures.FILTER_MATCH_IN, FilterFeatures.FILTER_MATCH_OUT,
                                                    FilterFeatures.FILTER_ACTION_IN, FilterFeatures.FILTER_ACTION_OUT]


def enum_from_string(name):

    return feature_type[name]
