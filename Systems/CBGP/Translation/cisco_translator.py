from RouterConfiguration.Cisco import cisco_config_features
from Systems.CBGP.Configuration.cbgp_config_features import *


def next_filter():
    return cisco_config_features.RouteMapFeatures.CONTINUE


def AS_regex(AS):
    return f'_{AS.num}_'


def get_extra_comms():
    return []


def get_router_features(router, neighbour_filters):
    features = [(router, cisco_config_features.BGPFeatures.DEFAULT_LOCAL_PREFERENCE, None),
                (router, cisco_config_features.BGPFeatures.ALWAYS_COMPARE_MED, None),
                (router, cisco_config_features.BGPFeatures.DETERMINISTIC_MED, None),
                (router, cisco_config_features.RouterFeatures.STATIC_ROUTE, None)]

    for neighbour in router.bgp_neighbours:

        features.append((router, cisco_config_features.BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN, neighbour.address))
        features.append((router, cisco_config_features.BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT, neighbour.address))
        features.append((router, cisco_config_features.BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF, neighbour.address))

        features.append((router, cisco_config_features.RouteMapFeatures.SET_IP_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)))
        features.append((router, cisco_config_features.RouteMapFeatures.SET_IP_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)))

        for i in range(10, 40, 10):
            features.append((router, cisco_config_features.RouteMapFeatures.MATCH_FEATURE_BGP_OUT, (neighbour_filters[neighbour, 'out'], i)))
            features.append((router, cisco_config_features.RouteMapFeatures.SET_FEATURE_BGP_OUT, (neighbour_filters[neighbour, 'out'], i)))
            features.append((router, cisco_config_features.RouteMapFeatures.MATCH_FEATURE_BGP_IN, (neighbour_filters[neighbour, 'in'], i)))
            features.append((router, cisco_config_features.RouteMapFeatures.SET_FEATURE_BGP_IN, (neighbour_filters[neighbour, 'in'], i)))
            features.append((router, cisco_config_features.RouteMapFeatures.ROUTE_MAP_DENY, (neighbour_filters[neighbour, 'out'], i)))
            features.append((router, cisco_config_features.RouteMapFeatures.ROUTE_MAP_DENY, (neighbour_filters[neighbour, 'in'], i)))

    for interface in router.interfaces:
        features.append((router, cisco_config_features.OSPFFeatures.INTERFACE_OSPF_COST, interface))

    return features


def translate_config(feature_list, routers, cisco_features, neighbour_filters, comm_lists, next_hop_acls, as_path_lists):

    router_config = {rf: -1 for rf in cisco_features}

    med_setting = {
        'deterministic': cisco_config_features.BGPFeatures.DETERMINISTIC_MED,
        'always-compare': cisco_config_features.BGPFeatures.ALWAYS_COMPARE_MED
    }

    translation = {

        GlobalFeatures.LOCAL_PREF: lambda router, pref: ((router, cisco_config_features.BGPFeatures.DEFAULT_LOCAL_PREFERENCE, None), (pref,)),
        GlobalFeatures.MED: lambda router, med: ((router, med_setting[med], None), ()),

        RouterFeatures.NEXT_HOP: lambda router, neighbour, next_hop: ((router, cisco_config_features.RouteMapFeatures.SET_IP_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)), (next_hop,)),
        RouterFeatures.NEXT_HOP_SELF: lambda router, neighbour: ((router, cisco_config_features.BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF, neighbour.address), ()),
        RouterFeatures.IGP_WEIGHT: lambda router, interface, cost: ((router, cisco_config_features.OSPFFeatures.INTERFACE_OSPF_COST, interface), (cost,)),
        RouterFeatures.STATIC_ROUTE: lambda router, _, net, interface: ((router, cisco_config_features.RouterFeatures.STATIC_ROUTE, None), (net, interface)),

        FilterFeatures.ACTION_ACCEPT: lambda router, rm, seq: (),
        FilterFeatures.ACTION_DENY: lambda router, rm, seq:
            (cisco_config_features.RouteMapFeatures.ROUTE_MAP_DENY, ()),
        FilterFeatures.ACTION_CALL: lambda router, rm, seq: (),
        FilterFeatures.ACTION_JUMP: lambda router, rm, seq: (),
        FilterFeatures.ACTION_LOCAL_PREF: lambda router, rm, seq, pref:
            (cisco_config_features.RouteMapFeatures.SET_LOCAL_PREFERENCE, pref),
        FilterFeatures.ACTION_METRIC: lambda router, rm, seq, metric:
            (cisco_config_features.RouteMapFeatures.SET_METRIC, metric),
        FilterFeatures.ACTION_METRIC_INTERNAL: lambda router, rm, seq:
            (cisco_config_features.RouteMapFeatures.SET_METRIC_TYPE_INTERNAL,),
        FilterFeatures.ACTION_COMMUNITY_ADD: lambda router, rm, seq, comm:
            (cisco_config_features.RouteMapFeatures.SET_COMMUNITY, comm, 'additive'),
        FilterFeatures.ACTION_COMMUNITY_STRIP: lambda router, rm, seq:
            (cisco_config_features.RouteMapFeatures.SET_COMMUNITY, 'none', ''),
        FilterFeatures.ACTION_COMMUNITY_REMOVE: lambda router, rm, seq, comm:
            (cisco_config_features.RouteMapFeatures.SET_COMM_LIST_DELETE, comm_lists[router, comm]),
        FilterFeatures.ACTION_AS_PATH_PREPEND: lambda router, rm, seq, n:
            (cisco_config_features.RouteMapFeatures.SET_AS_PATH_PREPEND, ' '.join([str(router.AS.num) for _ in range(n)])),
        FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE: lambda router, rm, seq: (),
        FilterFeatures.ACTION_RED_COMMUNITY_ADD: lambda router, rm, seq: (),
        FilterFeatures.MATCH_ANY: lambda router, rm, seq: (),
        FilterFeatures.MATCH_COMMUNITY: lambda router, rm, seq, comm:
            (cisco_config_features.RouteMapFeatures.MATCH_COMMUNITY_LIST, comm_lists[router, comm], ''),
        FilterFeatures.MATCH_NEXT_HOP: lambda router, rm, seq, next_hop:
            (cisco_config_features.RouteMapFeatures.MATCH_IP_NEXT_HOP, next_hop_acls[router, next_hop]),
        FilterFeatures.MATCH_NEXT_HOP_IN: lambda router, rm, seq, next_hop:
            (cisco_config_features.RouteMapFeatures.MATCH_IP_NEXT_HOP, next_hop),
        FilterFeatures.MATCH_PREFIX: lambda router, rm, seq, prefix:
            (cisco_config_features.RouteMapFeatures.MATCH_IP_PREFIX_LIST, prefix),
        FilterFeatures.MATCH_PREFIX_IN: lambda router, rm, seq, prefix:
            (cisco_config_features.RouteMapFeatures.MATCH_IP_PREFIX_LIST, prefix),
        FilterFeatures.MATCH_PATH: lambda router, rm, seq, AS:
            (cisco_config_features.RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST, as_path_lists[router, AS]),
        FilterFeatures.FILTER_MATCH_OUT: lambda router, rm, seq, feature, *args:
            ((router, cisco_config_features.RouteMapFeatures.MATCH_FEATURE_BGP_OUT, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_ACTION_OUT: lambda router, rm, seq, feature, *args:
            ((router, cisco_config_features.RouteMapFeatures.SET_FEATURE_BGP_OUT, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_MATCH_IN: lambda router, rm, seq, feature, *args:
            ((router, cisco_config_features.RouteMapFeatures.MATCH_FEATURE_BGP_IN, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_ACTION_IN: lambda router, rm, seq, feature, *args:
            ((router, cisco_config_features.RouteMapFeatures.SET_FEATURE_BGP_IN, (rm, seq)), translation[feature](router, rm, seq, *args))
    }

    for router, feature, arg in feature_list:

        if feature_list[router, feature, arg] == -1:
            continue

        args = feature_list[router, feature, arg]

        if feature in global_features:
            for r in routers:
                f, a = translation[feature](r, *args)
                router_config[f] = a
        elif feature in router_features:
            f, a = translation[feature](router, arg, *args)
            router_config[f] = a
        else:
            neighbour, direction, seq = arg
            if translation[feature](router, neighbour_filters[neighbour, direction], seq, *args):
                f, a = translation[feature](router, neighbour_filters[neighbour, direction], seq, *args)
                if cisco_config_features.RouteMapFeatures.ROUTE_MAP_DENY in a:
                    f = (router, cisco_config_features.RouteMapFeatures.ROUTE_MAP_DENY, (neighbour_filters[neighbour, direction], seq))
                    a = ()
                    router_config[f] = a
                elif a:
                    router_config[f] = a
            if direction == 'in':
                router_config[router, cisco_config_features.BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN, neighbour.address] = (neighbour_filters[neighbour, direction],)
            else:
                router_config[router, cisco_config_features.BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT, neighbour.address] = (neighbour_filters[neighbour, direction],)

    return router_config
