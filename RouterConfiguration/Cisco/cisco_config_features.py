from enum import Enum, auto


class RouterFeatures(Enum):
    STATIC_ROUTE = auto()


class OSPFFeatures(Enum):
    AUTO_COST = auto()
    NO_COMPATIBLE_RFC1583 = auto()
    DEFAULT_INFORMATION_ORIGINATE = auto()
    DEFAULT_METRIC = auto()
    DISTANCE = auto()
    REDISTRIBUTE_CONNECTED = auto()
    REDISTRIBUTE_STATIC = auto()
    REDISTRIBUTE_BGP = auto()
    MAX_METRIC = auto()
    AREA_FILTER_LIST = auto()
    AREA_RANGE = auto()
    NSSA_NO_REDISTRIBUTION = auto()
    NSSA_DEFAULT_INFORMATION_ORIGINATE = auto()
    NSSA_NO_SUMMARY = auto()
    NSSA_ONLY = auto()
    NSSA_STUB_DEFAULT_COST = auto()
    STUB_NO_SUMMARY = auto()
    INTERFACE_OSPF_COST = auto()
    INTERFACE_OSPF_PRIORITY = auto()


class BGPFeatures(Enum):
    ALWAYS_COMPARE_MED = auto()
    BESTPATH_COMPARE_ROUTERID = auto()
    BESTPATH_MED_CONFED = auto()
    BESTPATH_MED_MISSING = auto()
    NO_CLIENT_TO_CLIENT_REFLECTION = auto()
    DEFAULT_LOCAL_PREFERENCE = auto()
    DETERMINISTIC_MED = auto()
    MAXAS_LIMIT = auto()
    DEFAULT_INFORMATION_ORIGINATE = auto()  # causes some problems for batfish, shows up under address family
    ADDITIONAL_PATHS_INSTALL = auto()
    AUTO_SUMMARY = auto()
    BGP_DAMPENING = auto()
    DISTANCE_BGP = auto()
    REDISTRIBUTE_CONNECTED = auto()
    REDISTRIBUTE_STATIC = auto()
    REDISTRIBUTE_OSPF = auto()  # not supported
    SYNCHRONIZATION = auto()
    TABLE_MAP = auto()
    AGGREGATE_ADDRESS = auto()
    ADDITIONAL_PATHS = auto()
    NEIGHBOUR_MAXIMUM_PREFIX = auto()
    NEIGHBOUR_ROUTE_MAP_IN = auto()
    NEIGHBOUR_ROUTE_MAP_OUT = auto()
    NEIGHBOUR_NEXT_HOP_SELF = auto()
    NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST = auto()
    NEIGHBOUR_DEFAULT_ORIGINATE = auto()
    # NEIGHBOUR_PREFIX_LIST = auto()
    NEIGHBOUR_ROUTE_REFLECTOR_CLIENT = auto()
    NEIGHBOUR_WEIGHT = auto()


class RouteMapFeatures(Enum):
    ROUTE_MAP_DENY = auto()
    MATCH_FEATURE_BGP_OUT = auto()
    MATCH_FEATURE_BGP_IN = auto()
    SET_FEATURE_BGP_OUT = auto()
    SET_FEATURE_BGP_IN = auto()
    CONTINUE = auto()
    MATCH_AS_NUMBER = auto()
    MATCH_AS_PATH_ACCESS_LIST = auto()
    MATCH_AS = auto()
    MATCH_COMMUNITY_LIST = auto()
    MATCH_EXTCOMMUNITY = auto()
    MATCH_INTERFACE = auto()
    MATCH_IP_ACCESS_LIST = auto()
    MATCH_IP_NEXT_HOP = auto()
    MATCH_IP_PREFIX_LIST = auto()
    MATCH_IP_ROUTE_SOURCE = auto()
    MATCH_LENGTH = auto()
    MATCH_POLICY_LIST = auto()
    MATCH_ROUTE_TYPE = auto()
    MATCH_SOURCE_PROTOCOL = auto()
    MATCH_TAG = auto()
    SET_AS_PATH_PREPEND = auto()
    SET_AS_PATH_TAG = auto()
    SET_COMM_LIST_DELETE = auto()
    SET_COMMUNITY = auto()
    SET_COMMUNITY_ADDITIVE = auto()
    SET_COMMUNITY_LIST_ADDITIVE = auto()
    SET_COMMUNITY_LIST = auto()
    SET_COMMUNITY_NONE = auto()
    SET_EXTCOMM_LIST = auto()
    SET_EXTCOMMUNITY = auto()
    SET_INTERFACE = auto()
    SET_IP_DEFAULT_NEXT_HOP = auto()
    SET_IP_DF = auto()
    SET_IP_PRECEDENCE = auto()
    SET_LOCAL_PREFERENCE = auto()
    SET_METRIC_EIGRP = auto()
    SET_METRIC = auto()
    SET_METRIC_TYPE_INTERNAL = auto()
    SET_MPLS_LABEL = auto()
    SET_NEXT_HOP_PEER_ADDRESS = auto()
    SET_IP_NEXT_HOP = auto()
    SET_NLRI = auto()
    SET_ORIGIN = auto()
    SET_TAG = auto()
    SET_TRAFFIC_INDEX = auto()
    SET_WEIGHT = auto()


def filter_unsupported(feature_list):
    unsupported_features = [
        OSPFFeatures.AREA_FILTER_LIST,
        BGPFeatures.REDISTRIBUTE_OSPF,
        BGPFeatures.DEFAULT_INFORMATION_ORIGINATE,
        BGPFeatures.ADDITIONAL_PATHS,
        BGPFeatures.ADDITIONAL_PATHS_INSTALL,
        RouteMapFeatures.MATCH_INTERFACE,
        RouteMapFeatures.SET_INTERFACE,
        RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP,
        RouteMapFeatures.SET_METRIC_TYPE_INTERNAL,
        RouteMapFeatures.MATCH_IP_NEXT_HOP,
        RouteMapFeatures.CONTINUE,
        BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF,
        BGPFeatures.BGP_DAMPENING,
        BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST,
        # BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE  # unsupported by NV
    ]

    faulty_features = [
        OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE,
        OSPFFeatures.DISTANCE,
        OSPFFeatures.MAX_METRIC,
        OSPFFeatures.AREA_RANGE,
        OSPFFeatures.REDISTRIBUTE_STATIC,
        # BGPFeatures.REDISTRIBUTE_CONNECTED,
        BGPFeatures.AGGREGATE_ADDRESS,
        BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE,
        BGPFeatures.DISTANCE_BGP,
        BGPFeatures.BESTPATH_MED_CONFED,
        # OSPFFeatures.INTERFACE_OSPF_COST,
        OSPFFeatures.INTERFACE_OSPF_PRIORITY,
        OSPFFeatures.DEFAULT_METRIC,
        # OSPFFeatures.REDISTRIBUTE_CONNECTED,
        BGPFeatures.BESTPATH_MED_MISSING,
        BGPFeatures.AUTO_SUMMARY,
        BGPFeatures.MAXAS_LIMIT,
        BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX
    ]
    faulty_features = []

    return list(filter(lambda f: f not in unsupported_features + faulty_features, feature_list))


feature_type = {
    'RouterFeatures': RouterFeatures,
    'OSPFFeatures': OSPFFeatures,
    'BGPFeatures': BGPFeatures,
    'RouteMapFeatures': RouteMapFeatures
}

# Features by Protocols
static_features = filter_unsupported([
    RouterFeatures.STATIC_ROUTE,
    OSPFFeatures.REDISTRIBUTE_STATIC,
    BGPFeatures.REDISTRIBUTE_STATIC
])
ospf_features = filter_unsupported(list(OSPFFeatures) + [BGPFeatures.REDISTRIBUTE_OSPF])
bgp_features = filter_unsupported(list(BGPFeatures) + [OSPFFeatures.REDISTRIBUTE_BGP])

interface_features = filter_unsupported([OSPFFeatures.INTERFACE_OSPF_COST, OSPFFeatures.INTERFACE_OSPF_PRIORITY])

area_features = filter_unsupported([OSPFFeatures.AREA_RANGE, OSPFFeatures.AREA_FILTER_LIST])
nssa_features = filter_unsupported([
    OSPFFeatures.NSSA_ONLY,
    OSPFFeatures.NSSA_NO_SUMMARY,
    OSPFFeatures.NSSA_NO_REDISTRIBUTION,
    OSPFFeatures.NSSA_STUB_DEFAULT_COST,
    OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE
])
stub_features = filter_unsupported([OSPFFeatures.STUB_NO_SUMMARY, OSPFFeatures.NSSA_STUB_DEFAULT_COST])

static_router_features = filter_unsupported([RouterFeatures.STATIC_ROUTE])
ospf_router_features = filter_unsupported([
    OSPFFeatures.AUTO_COST,
    OSPFFeatures.NO_COMPATIBLE_RFC1583,
    OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE,
    OSPFFeatures.DEFAULT_METRIC,
    OSPFFeatures.DISTANCE,
    OSPFFeatures.REDISTRIBUTE_CONNECTED,
    OSPFFeatures.REDISTRIBUTE_STATIC,
    OSPFFeatures.REDISTRIBUTE_BGP,
    OSPFFeatures.MAX_METRIC
])
bgp_router_features = filter_unsupported([
    BGPFeatures.ALWAYS_COMPARE_MED,
    BGPFeatures.BESTPATH_COMPARE_ROUTERID,
    BGPFeatures.BESTPATH_MED_CONFED,
    BGPFeatures.BESTPATH_MED_MISSING,
    BGPFeatures.NO_CLIENT_TO_CLIENT_REFLECTION,
    BGPFeatures.DEFAULT_LOCAL_PREFERENCE,
    BGPFeatures.DETERMINISTIC_MED,
    BGPFeatures.MAXAS_LIMIT,
    BGPFeatures.DEFAULT_INFORMATION_ORIGINATE,
    BGPFeatures.ADDITIONAL_PATHS_INSTALL,
    BGPFeatures.AUTO_SUMMARY,
    BGPFeatures.BGP_DAMPENING,
    BGPFeatures.DISTANCE_BGP,
    BGPFeatures.REDISTRIBUTE_CONNECTED,
    BGPFeatures.REDISTRIBUTE_STATIC,
    BGPFeatures.REDISTRIBUTE_OSPF,
    BGPFeatures.SYNCHRONIZATION,
    BGPFeatures.TABLE_MAP,
    BGPFeatures.AGGREGATE_ADDRESS,
    BGPFeatures.ADDITIONAL_PATHS
])

filter_req_features = filter_unsupported([
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT,
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN,
    BGPFeatures.TABLE_MAP])

filter_features = filter_unsupported(list(RouteMapFeatures))

router_features = filter_unsupported(
    ospf_router_features + bgp_router_features + list(RouterFeatures)
)
neighbour_features = filter_unsupported([
    BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE,
    BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST,
    BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF,
    BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX,
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN,
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT,
    BGPFeatures.NEIGHBOUR_ROUTE_REFLECTOR_CLIENT,
    BGPFeatures.NEIGHBOUR_WEIGHT
])

match_features_in = filter_unsupported([
    RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST,
    RouteMapFeatures.MATCH_INTERFACE,
    RouteMapFeatures.MATCH_COMMUNITY_LIST,
    RouteMapFeatures.MATCH_IP_PREFIX_LIST,
    RouteMapFeatures.MATCH_IP_NEXT_HOP
])
set_features_in = filter_unsupported([
    RouteMapFeatures.SET_AS_PATH_PREPEND,
    RouteMapFeatures.SET_COMM_LIST_DELETE,
    RouteMapFeatures.SET_COMMUNITY,
    RouteMapFeatures.SET_ORIGIN,
    RouteMapFeatures.SET_WEIGHT,
    RouteMapFeatures.SET_LOCAL_PREFERENCE,
    RouteMapFeatures.SET_METRIC_TYPE_INTERNAL,
    RouteMapFeatures.SET_INTERFACE,
    RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP,
    RouteMapFeatures.SET_IP_NEXT_HOP,
    RouteMapFeatures.SET_METRIC
])

match_features_out = filter_unsupported([
    RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST,
    RouteMapFeatures.MATCH_INTERFACE,
    RouteMapFeatures.MATCH_COMMUNITY_LIST,
    RouteMapFeatures.MATCH_IP_PREFIX_LIST,
    RouteMapFeatures.MATCH_IP_NEXT_HOP
])
set_features_out = filter_unsupported([
    RouteMapFeatures.SET_AS_PATH_PREPEND,
    RouteMapFeatures.SET_COMM_LIST_DELETE,
    RouteMapFeatures.SET_COMMUNITY,
    RouteMapFeatures.SET_ORIGIN,
    RouteMapFeatures.SET_WEIGHT,
    RouteMapFeatures.SET_LOCAL_PREFERENCE,
    RouteMapFeatures.SET_METRIC_TYPE_INTERNAL,
    RouteMapFeatures.SET_INTERFACE,
    RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP,
    RouteMapFeatures.SET_IP_NEXT_HOP,
    RouteMapFeatures.SET_METRIC
])

filter_ospf_in_features = filter_unsupported([])
filter_ospf_out_features = filter_unsupported([])
filter_bgp_in_features = filter_unsupported([RouteMapFeatures.SET_FEATURE_BGP_IN, RouteMapFeatures.ROUTE_MAP_DENY])
filter_bgp_out_features = filter_unsupported([RouteMapFeatures.SET_FEATURE_BGP_OUT, RouteMapFeatures.ROUTE_MAP_DENY])

all_features = interface_features + area_features + nssa_features + stub_features + router_features + neighbour_features + filter_features


def enum_from_string(name):

    return feature_type[name]
