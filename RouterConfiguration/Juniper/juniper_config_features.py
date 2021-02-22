from enum import Enum, auto


class ProtocolIndependentFeatures(Enum):
    STATIC_ROUTE = auto()


class OSPFFeatures(Enum):
    AREA_RANGE = auto()
    AREA_LABEL_SWITCHED_PATH = auto()
    EXPORT = auto()  # ni
    EXTERNAL_PREFERENCE = auto()
    IMPORT = auto()  # ni
    NO_RFC_1583 = auto()
    REFERENCE_BANDWIDTH = auto()
    RIB_GROUP = auto()  # ni
    TRAFFIC_ENGINEERING = auto()  # ni
    NSSA_DEFAULT_LSA = auto()
    NSSA_NO_SUMMARIES = auto()
    STUB_NO_SUMMARIES = auto()
    STUB_DEFAULT_METRIC = auto()
    INTERFACE_LDP_SYNCHRONIZATION = auto()
    INTERFACE_LINK_PROTECTION = auto()
    INTERFACE_METRIC = auto()
    INTERFACE_PASSIVE = auto()
    INTERFACE_PRIORITY = auto()
    INTERFACE_TE_METRIC = auto()
    REDISTRIBUTE_DIRECT = auto()
    REDISTRIBUTE_STATIC = auto()
    REDISTRIBUTE_BGP = auto()


class BGPFeatures(Enum):
    ACCEPTED_PREFIX_LIMIT = auto()
    ADVERTISE_EXTERNAL = auto()
    ADVERTISE_INACTIVE = auto()
    ADVERTISE_PEER_AS = auto()
    AS_OVERRIDE = auto()
    CLUSTER = auto()
    DAMPING = auto()
    ENFORCE_FIRST_AS = auto()
    EXPORT = auto()  # ni
    IMPORT = auto()  # ni
    LOCAL_AS = auto()
    METRIC_OUT = auto()
    MULTIHOP = auto()
    NO_CLIENT_REFLECT = auto()
    PASSIVE = auto()
    PATH_SELECTION = auto()
    REMOVE_PRIVATE = auto()
    TCP_MSS = auto()
    ADD_PATH = auto()
    LOOPS = auto()
    PREFIX_LIMIT = auto()
    RIB_GROUP = auto()  # ni
    REDISTRIBUTE_DIRECT = auto()
    REDISTRIBUTE_STATIC = auto()
    REDISTRIBUTE_OSPF = auto()

    LOCAL_PREFERENCE = auto()
    NEIGHBOUR_POLICY_EXPORT = auto()
    NEIGHBOUR_POLICY_IMPORT = auto()


class PolicyFeatures(Enum):
    AS_PATH = auto()
    AS_PATH_GROUP = auto()
    COMMUNITY = auto()
    CONDITION = auto()
    POLICY_STATEMENT = auto()
    PREFIX_LIST = auto()
    INVERT_MATCH = auto()
    MEMBERS = auto()
    APPLY_PATH = auto()
    FROM_AREA = auto()
    FROM_AS_PATH = auto()
    FROM_AS_PATH_GROUP = auto()
    FROM_COLOR = auto()
    FROM_COMMUNITY = auto()
    FROM_FAMILY = auto()
    FROM_INSTANCE = auto()
    FROM_INTERFACE = auto()
    FROM_LEVEL = auto()
    FROM_LOCAL_PREFERENCE = auto()
    FROM_METRIC = auto()
    FROM_NEIGHBOUR = auto()
    FROM_ORIGIN = auto()
    FROM_POLICY = auto()
    FROM_PREFIX_LIST = auto()
    FROM_PREFIX_LIST_FILTER = auto()
    FROM_PROTOCOL = auto()
    FROM_RIB = auto()
    FROM_ROUTE_FILTER = auto()
    FROM_ROUTE_TYPE = auto()
    FROM_SOURCE_ADDRESS_FILTER = auto()
    FROM_TAG = auto()
    TO_LEVEL = auto()
    TO_RIB = auto()
    THEN_ACCEPT = auto()
    THEN_AS_PATH_EXPAND = auto()
    THEN_AS_PATH_PREPEND = auto()
    THEN_COLOR = auto()
    THEN_COLOR2 = auto()
    THEN_COMMUNITY_ADD = auto()
    THEN_COMMUNITY_DELETE = auto()
    THEN_COMMUNITY_SET = auto()
    THEN_COS_NEXT_HOP_MAP = auto()
    THEN_DEFAULT_ACTION_ACCEPT = auto()
    THEN_DEFAULT_ACTION_REJECT = auto()
    THEN_EXTERNAL = auto()
    THEN_FORWARDING_CLASS = auto()
    THEN_INSTALL_NEXTHOP = auto()
    THEN_LOCAL_PREFERENCE = auto()
    THEN_METRIC = auto()
    THEN_METRIC_ADD = auto()
    THEN_METRIC_EXPRESSION = auto()
    THEN_METRIC_IGP = auto()
    THEN_METRIC2 = auto()
    THEN_METRIC2_EXPRESSION = auto()
    THEN_NEXT_HOP = auto()
    THEN_NEXT_HOP_SELF = auto()
    THEN_NEXT_POLICY = auto()
    THEN_NEXT_TERM = auto()
    THEN_ORIGIN = auto()
    THEN_PREFERENCE = auto()
    THEN_PRIORITY = auto()
    THEN_REJECT = auto()
    THEN_TAG = auto()
    POLICY_MATCH_FEATURE_BGP_OUT = auto()
    POLICY_MATCH_FEATURE_BGP_IN = auto()
    POLICY_MATCH_FEATURE_OSPF_OUT = auto()
    POLICY_MATCH_FEATURE_OSPF_IN = auto()
    POLICY_SET_FEATURE_BGP_OUT = auto()
    POLICY_SET_FEATURE_BGP_IN = auto()
    POLICY_SET_FEATURE_OSPF_OUT = auto()
    POLICY_SET_FEATURE_OSPF_IN = auto()

    FROM_NEXT_HOP = auto()


def filter_unsupported(feature_list):
    unsupported_features = [
        OSPFFeatures.TRAFFIC_ENGINEERING,
        OSPFFeatures.RIB_GROUP,
        OSPFFeatures.AREA_LABEL_SWITCHED_PATH,
        OSPFFeatures.INTERFACE_TE_METRIC,
        OSPFFeatures.INTERFACE_LINK_PROTECTION,
        OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION,
        BGPFeatures.RIB_GROUP,
        BGPFeatures.MULTIHOP,
        BGPFeatures.CLUSTER,
        BGPFeatures.METRIC_OUT,
        BGPFeatures.LOCAL_AS,
        BGPFeatures.DAMPING,
        PolicyFeatures.FROM_POLICY,
        PolicyFeatures.FROM_AS_PATH_GROUP,
        PolicyFeatures.FROM_INSTANCE,
        PolicyFeatures.FROM_LEVEL,
        PolicyFeatures.FROM_RIB,
        PolicyFeatures.TO_LEVEL,
        PolicyFeatures.TO_RIB,
        PolicyFeatures.THEN_COS_NEXT_HOP_MAP,
        PolicyFeatures.THEN_FORWARDING_CLASS,
        PolicyFeatures.THEN_INSTALL_NEXTHOP,
        PolicyFeatures.THEN_METRIC_EXPRESSION,
        PolicyFeatures.THEN_METRIC2_EXPRESSION,
        PolicyFeatures.THEN_NEXT_POLICY,
        PolicyFeatures.THEN_NEXT_TERM,
        PolicyFeatures.FROM_ROUTE_FILTER,
        PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER,
        BGPFeatures.LOCAL_PREFERENCE,
        BGPFeatures.NEIGHBOUR_POLICY_IMPORT,
        BGPFeatures.NEIGHBOUR_POLICY_EXPORT,
        PolicyFeatures.FROM_NEXT_HOP
    ]

    faulty_features = [
        # BGPFeatures.AS_OVERRIDE,
        OSPFFeatures.AREA_RANGE,
        OSPFFeatures.EXTERNAL_PREFERENCE,
        OSPFFeatures.INTERFACE_PRIORITY
    ]

    return list(filter(lambda f: f not in unsupported_features + faulty_features, feature_list))


feature_type = {
    'ProtocolIndependentFeatures': ProtocolIndependentFeatures,
    'OSPFFeatures': OSPFFeatures,
    'BPGFeatures': BGPFeatures,
    'PolicyFeatures': PolicyFeatures
}


interface_features = filter_unsupported([
    OSPFFeatures.INTERFACE_PRIORITY, OSPFFeatures.INTERFACE_TE_METRIC, OSPFFeatures.INTERFACE_PASSIVE,
    OSPFFeatures.INTERFACE_METRIC, OSPFFeatures.INTERFACE_LINK_PROTECTION,
    OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION
])

area_features = filter_unsupported([OSPFFeatures.AREA_RANGE, OSPFFeatures.AREA_LABEL_SWITCHED_PATH])
nssa_features = filter_unsupported([OSPFFeatures.NSSA_NO_SUMMARIES, OSPFFeatures.NSSA_DEFAULT_LSA])
stub_features = filter_unsupported([OSPFFeatures.STUB_NO_SUMMARIES, OSPFFeatures.STUB_DEFAULT_METRIC])

static_router_features = filter_unsupported([ProtocolIndependentFeatures.STATIC_ROUTE])
ospf_router_features = filter_unsupported([f for f in OSPFFeatures if f not in
                                           interface_features + area_features + nssa_features + stub_features])
bgp_router_features = filter_unsupported(list(BGPFeatures))

redistribute_static = filter_unsupported([OSPFFeatures.REDISTRIBUTE_STATIC, BGPFeatures.REDISTRIBUTE_STATIC])
redistribute_connected = filter_unsupported([OSPFFeatures.REDISTRIBUTE_DIRECT, BGPFeatures.REDISTRIBUTE_DIRECT])
redistribute_ospf = filter_unsupported([BGPFeatures.REDISTRIBUTE_OSPF])
redistribute_bgp = filter_unsupported([OSPFFeatures.REDISTRIBUTE_BGP])

filter_req_features = filter_unsupported([OSPFFeatures.EXPORT, OSPFFeatures.IMPORT, BGPFeatures.IMPORT, BGPFeatures.EXPORT])

router_features = filter_unsupported(ospf_router_features + bgp_router_features + list(ProtocolIndependentFeatures))

neighbour_features = []

match_features_ospf_in = filter_unsupported([
    PolicyFeatures.FROM_AREA,
    PolicyFeatures.FROM_COLOR,
    PolicyFeatures.FROM_FAMILY,
    PolicyFeatures.FROM_INTERFACE,
    PolicyFeatures.FROM_METRIC,
    PolicyFeatures.FROM_NEIGHBOUR,
    PolicyFeatures.FROM_POLICY,
    PolicyFeatures.FROM_PREFIX_LIST,
    PolicyFeatures.FROM_PREFIX_LIST_FILTER,
    PolicyFeatures.FROM_ROUTE_FILTER,
    PolicyFeatures.FROM_ROUTE_TYPE,
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER,
    PolicyFeatures.FROM_TAG
])
match_features_ospf_out = filter_unsupported([
    PolicyFeatures.FROM_AREA,
    PolicyFeatures.FROM_COLOR,
    PolicyFeatures.FROM_FAMILY,
    PolicyFeatures.FROM_INTERFACE,
    PolicyFeatures.FROM_METRIC,
    PolicyFeatures.FROM_NEIGHBOUR,
    PolicyFeatures.FROM_POLICY,
    PolicyFeatures.FROM_PREFIX_LIST,
    PolicyFeatures.FROM_PREFIX_LIST_FILTER,
    PolicyFeatures.FROM_PROTOCOL,
    PolicyFeatures.FROM_ROUTE_FILTER,
    PolicyFeatures.FROM_ROUTE_TYPE,
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER,
    PolicyFeatures.FROM_TAG
])
set_features_ospf_in = filter_unsupported([
    PolicyFeatures.THEN_ACCEPT,
    PolicyFeatures.THEN_COLOR,
    PolicyFeatures.THEN_COLOR2,
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT,
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT,
    PolicyFeatures.THEN_EXTERNAL,
    PolicyFeatures.THEN_METRIC,
    PolicyFeatures.THEN_METRIC_ADD,
    PolicyFeatures.THEN_METRIC_EXPRESSION,
    PolicyFeatures.THEN_METRIC2,
    PolicyFeatures.THEN_METRIC2_EXPRESSION,
    PolicyFeatures.THEN_NEXT_HOP,
    PolicyFeatures.THEN_NEXT_HOP_SELF,
    PolicyFeatures.THEN_NEXT_POLICY,
    PolicyFeatures.THEN_NEXT_TERM,
    PolicyFeatures.THEN_PREFERENCE,
    PolicyFeatures.THEN_PRIORITY,
    PolicyFeatures.THEN_REJECT,
    PolicyFeatures.THEN_TAG
])
set_features_ospf_out = filter_unsupported([
    PolicyFeatures.THEN_ACCEPT,
    PolicyFeatures.THEN_COLOR,
    PolicyFeatures.THEN_COLOR2,
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT,
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT,
    PolicyFeatures.THEN_EXTERNAL,
    PolicyFeatures.THEN_METRIC,
    PolicyFeatures.THEN_METRIC_ADD,
    PolicyFeatures.THEN_METRIC_EXPRESSION,
    PolicyFeatures.THEN_METRIC2,
    PolicyFeatures.THEN_METRIC2_EXPRESSION,
    PolicyFeatures.THEN_NEXT_HOP,
    PolicyFeatures.THEN_NEXT_HOP_SELF,
    PolicyFeatures.THEN_NEXT_POLICY,
    PolicyFeatures.THEN_NEXT_TERM,
    PolicyFeatures.THEN_PREFERENCE,
    PolicyFeatures.THEN_REJECT,
    PolicyFeatures.THEN_TAG
])
match_features_bgp_in = filter_unsupported([
    PolicyFeatures.FROM_AS_PATH,
    PolicyFeatures.FROM_AS_PATH_GROUP,
    PolicyFeatures.FROM_COLOR,
    PolicyFeatures.FROM_COMMUNITY,
    PolicyFeatures.FROM_FAMILY,
    PolicyFeatures.FROM_LOCAL_PREFERENCE,
    PolicyFeatures.FROM_METRIC,
    PolicyFeatures.FROM_NEIGHBOUR,
    PolicyFeatures.FROM_ORIGIN,
    PolicyFeatures.FROM_POLICY,
    PolicyFeatures.FROM_PREFIX_LIST,
    PolicyFeatures.FROM_PREFIX_LIST_FILTER,
    PolicyFeatures.FROM_ROUTE_FILTER,
    PolicyFeatures.FROM_ROUTE_TYPE,
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER,
    PolicyFeatures.FROM_TAG
])
match_features_bgp_out = filter_unsupported([
    PolicyFeatures.FROM_AS_PATH,
    PolicyFeatures.FROM_AS_PATH_GROUP,
    PolicyFeatures.FROM_COLOR,
    PolicyFeatures.FROM_COMMUNITY,
    PolicyFeatures.FROM_FAMILY,
    PolicyFeatures.FROM_LOCAL_PREFERENCE,
    PolicyFeatures.FROM_METRIC,
    PolicyFeatures.FROM_NEIGHBOUR,
    PolicyFeatures.FROM_ORIGIN,
    PolicyFeatures.FROM_POLICY,
    PolicyFeatures.FROM_PREFIX_LIST,
    PolicyFeatures.FROM_PREFIX_LIST_FILTER,
    PolicyFeatures.FROM_PROTOCOL,
    PolicyFeatures.FROM_ROUTE_FILTER,
    PolicyFeatures.FROM_ROUTE_TYPE,
    PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER,
    PolicyFeatures.FROM_TAG
])
set_features_bgp_in = filter_unsupported([
    PolicyFeatures.THEN_ACCEPT,
    PolicyFeatures.THEN_AS_PATH_EXPAND,
    PolicyFeatures.THEN_AS_PATH_PREPEND,
    PolicyFeatures.THEN_COLOR,
    PolicyFeatures.THEN_COLOR2,
    PolicyFeatures.THEN_COMMUNITY_ADD,
    PolicyFeatures.THEN_COMMUNITY_DELETE,
    PolicyFeatures.THEN_COMMUNITY_SET,
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT,
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT,
    PolicyFeatures.THEN_LOCAL_PREFERENCE,
    PolicyFeatures.THEN_METRIC,
    PolicyFeatures.THEN_METRIC_ADD,
    PolicyFeatures.THEN_METRIC_EXPRESSION,
    PolicyFeatures.THEN_METRIC_IGP,
    PolicyFeatures.THEN_METRIC2,
    PolicyFeatures.THEN_METRIC2_EXPRESSION,
    PolicyFeatures.THEN_NEXT_HOP,
    PolicyFeatures.THEN_NEXT_HOP_SELF,
    PolicyFeatures.THEN_NEXT_POLICY,
    PolicyFeatures.THEN_NEXT_TERM,
    PolicyFeatures.THEN_ORIGIN,
    PolicyFeatures.THEN_PREFERENCE,
    PolicyFeatures.THEN_REJECT,
    PolicyFeatures.THEN_TAG
])
set_features_bgp_out = filter_unsupported([
    PolicyFeatures.THEN_ACCEPT,
    PolicyFeatures.THEN_AS_PATH_EXPAND,
    PolicyFeatures.THEN_AS_PATH_PREPEND,
    PolicyFeatures.THEN_COLOR,
    PolicyFeatures.THEN_COLOR2,
    PolicyFeatures.THEN_COMMUNITY_ADD,
    PolicyFeatures.THEN_COMMUNITY_DELETE,
    PolicyFeatures.THEN_COMMUNITY_SET,
    PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT,
    PolicyFeatures.THEN_DEFAULT_ACTION_REJECT,
    PolicyFeatures.THEN_LOCAL_PREFERENCE,
    PolicyFeatures.THEN_METRIC,
    PolicyFeatures.THEN_METRIC_ADD,
    PolicyFeatures.THEN_METRIC_EXPRESSION,
    PolicyFeatures.THEN_METRIC_IGP,
    PolicyFeatures.THEN_METRIC2,
    PolicyFeatures.THEN_METRIC2_EXPRESSION,
    PolicyFeatures.THEN_NEXT_HOP,
    PolicyFeatures.THEN_NEXT_HOP_SELF,
    PolicyFeatures.THEN_NEXT_POLICY,
    PolicyFeatures.THEN_NEXT_TERM,
    PolicyFeatures.THEN_ORIGIN,
    PolicyFeatures.THEN_PREFERENCE,
    PolicyFeatures.THEN_REJECT,
    PolicyFeatures.THEN_TAG
])

filter_ospf_in_features = filter_unsupported([PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_IN, PolicyFeatures.POLICY_SET_FEATURE_OSPF_IN])
filter_ospf_out_features = filter_unsupported([PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_OUT, PolicyFeatures.POLICY_SET_FEATURE_OSPF_OUT])
filter_bgp_in_features = filter_unsupported([PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN, PolicyFeatures.POLICY_SET_FEATURE_BGP_IN])
filter_bgp_out_features = filter_unsupported([PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT, PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT])

filter_features = filter_unsupported(list(PolicyFeatures))

all_features = interface_features + area_features + nssa_features + stub_features + router_features + neighbour_features + filter_features


def enum_from_string(name):

    return feature_type[name]
