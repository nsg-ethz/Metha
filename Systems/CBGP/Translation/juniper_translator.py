from RouterConfiguration.Juniper import juniper_config_features
from Systems.CBGP.Configuration.cbgp_config_features import *
from Systems.CBGP.Configuration.cbgp_feature_args import get_possible_args


def next_filter():
    return juniper_config_features.PolicyFeatures.THEN_NEXT_TERM


def AS_regex(AS):
    return f'.*{AS.num}.*'


def get_extra_comms():
    return []  # return [f'* : *']


def get_router_features(router, neighbour_filters):
    features = [(router, juniper_config_features.BGPFeatures.LOCAL_PREFERENCE, None),
                (router, juniper_config_features.BGPFeatures.PATH_SELECTION, None),
                (router, juniper_config_features.ProtocolIndependentFeatures.STATIC_ROUTE, None)]

    for neighbour in router.bgp_neighbours:

        features.append((router, juniper_config_features.BGPFeatures.NEIGHBOUR_POLICY_EXPORT, neighbour))
        features.append((router, juniper_config_features.BGPFeatures.NEIGHBOUR_POLICY_IMPORT, neighbour))

        features.append((router, juniper_config_features.PolicyFeatures.THEN_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)))
        features.append((router, juniper_config_features.PolicyFeatures.THEN_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)))

        for i in range(10, 40, 10):
            features.append((router, juniper_config_features.PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT, (neighbour_filters[neighbour, 'out'], i)))
            features.append((router, juniper_config_features.PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT, (neighbour_filters[neighbour, 'out'], i)))
            features.append((router, juniper_config_features.PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN, (neighbour_filters[neighbour, 'in'], i)))
            features.append((router, juniper_config_features.PolicyFeatures.POLICY_SET_FEATURE_BGP_IN, (neighbour_filters[neighbour, 'in'], i)))

    for interface in router.interfaces:
        features.append((router, juniper_config_features.OSPFFeatures.INTERFACE_METRIC, interface))

    return features


def translate_config(feature_list, routers, juniper_features, neighbour_filters, comm_lists, next_hop_acls, as_path_lists):

    router_config = {rf: -1 for rf in juniper_features}

    med_setting = {
        'deterministic': lambda router: (),
        'always-compare': lambda router: ((router, juniper_config_features.BGPFeatures.PATH_SELECTION, None), (' always-compare-med ',))
    }

    translation = {

        GlobalFeatures.LOCAL_PREF: lambda router, pref: ((router, juniper_config_features.BGPFeatures.LOCAL_PREFERENCE, None), (pref,)),
        GlobalFeatures.MED: lambda router, med: med_setting[med](router),

        RouterFeatures.NEXT_HOP: lambda router, neighbour, next_hop: ((router, juniper_config_features.PolicyFeatures.THEN_NEXT_HOP, (neighbour_filters[neighbour, 'out'], 5)), (next_hop,)),
        RouterFeatures.NEXT_HOP_SELF: lambda router, neighbour: ((router, juniper_config_features.PolicyFeatures.THEN_NEXT_HOP_SELF, (neighbour_filters[neighbour, 'out'], 5)), ()),
        RouterFeatures.IGP_WEIGHT: lambda router, interface, cost: ((router, juniper_config_features.OSPFFeatures.INTERFACE_METRIC, interface), (cost,)),
        RouterFeatures.STATIC_ROUTE: lambda router, _, net, interface: ((router, juniper_config_features.ProtocolIndependentFeatures.STATIC_ROUTE, None), (net, interface)),

        FilterFeatures.ACTION_ACCEPT: lambda router, rm, seq:
            (juniper_config_features.PolicyFeatures.THEN_ACCEPT, ()),
        FilterFeatures.ACTION_DENY: lambda router, rm, seq:
            (juniper_config_features.PolicyFeatures.THEN_REJECT, ()),
        FilterFeatures.ACTION_CALL: lambda router, rm, seq: (),
        FilterFeatures.ACTION_JUMP: lambda router, rm, seq: (),
        FilterFeatures.ACTION_LOCAL_PREF: lambda router, rm, seq, pref:
            (juniper_config_features.PolicyFeatures.THEN_LOCAL_PREFERENCE, pref),
        FilterFeatures.ACTION_METRIC: lambda router, rm, seq, metric:
            (juniper_config_features.PolicyFeatures.THEN_METRIC, metric),
        FilterFeatures.ACTION_METRIC_INTERNAL: lambda router, rm, seq:
            (juniper_config_features.PolicyFeatures.THEN_METRIC, 'igp'),  # TODO check
        FilterFeatures.ACTION_COMMUNITY_ADD: lambda router, rm, seq, comm:
            (juniper_config_features.PolicyFeatures.THEN_COMMUNITY_ADD, comm_lists[router, comm]),
        FilterFeatures.ACTION_COMMUNITY_STRIP: lambda router, rm, seq:
            (juniper_config_features.PolicyFeatures.THEN_COMMUNITY_DELETE, comm_lists[router, f'* : *']),
        FilterFeatures.ACTION_COMMUNITY_REMOVE: lambda router, rm, seq, comm:
            (juniper_config_features.PolicyFeatures.THEN_COMMUNITY_DELETE, comm_lists[router, comm]),
        FilterFeatures.ACTION_AS_PATH_PREPEND: lambda router, rm, seq, n:
            (juniper_config_features.PolicyFeatures.THEN_AS_PATH_PREPEND, f'\"{" ".join([str(router.AS.num) for _ in range(n)])}\"'),
        FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE: lambda router, rm, seq: (),
        FilterFeatures.ACTION_RED_COMMUNITY_ADD: lambda router, rm, seq: (),
        FilterFeatures.MATCH_ANY: lambda router, rm, seq: (),
        FilterFeatures.MATCH_COMMUNITY: lambda router, rm, seq, comm:
            (juniper_config_features.PolicyFeatures.FROM_COMMUNITY, comm_lists[router, comm], ''),
        FilterFeatures.MATCH_NEXT_HOP: lambda router, rm, seq, next_hop:
            (juniper_config_features.PolicyFeatures.FROM_NEXT_HOP, next_hop),
        FilterFeatures.MATCH_NEXT_HOP_IN: lambda router, rm, seq, next_hop:
            (juniper_config_features.PolicyFeatures.MATCH_IP_NEXT_HOP, next_hop),
        FilterFeatures.MATCH_PREFIX: lambda router, rm, seq, prefix:
            (juniper_config_features.PolicyFeatures.FROM_PREFIX_LIST, prefix),
        FilterFeatures.MATCH_PREFIX_IN: lambda router, rm, seq, prefix:
            (juniper_config_features.PolicyFeatures.MATCH_IP_ADDRESS, prefix),
        FilterFeatures.MATCH_PATH: lambda router, rm, seq, AS:
            (juniper_config_features.PolicyFeatures.FROM_AS_PATH, as_path_lists[router, AS]),
        FilterFeatures.FILTER_MATCH_OUT: lambda router, rm, seq, feature, *args:
            ((router, juniper_config_features.PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_ACTION_OUT: lambda router, rm, seq, feature, *args:
            ((router, juniper_config_features.PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_MATCH_IN: lambda router, rm, seq, feature, *args:
            ((router, juniper_config_features.PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN, (rm, seq)), translation[feature](router, rm, seq, *args)),
        FilterFeatures.FILTER_ACTION_IN: lambda router, rm, seq, feature, *args:
            ((router, juniper_config_features.PolicyFeatures.POLICY_SET_FEATURE_BGP_IN, (rm, seq)), translation[feature](router, rm, seq, *args))
    }

    for router, feature, arg in feature_list:

        if feature_list[router, feature, arg] == -1:
            continue

        args = get_possible_args(router)[feature][feature_list[router, feature, arg]]

        if feature in global_features:
            for r in routers:
                if translation[feature](r, *args):
                    f, a = translation[feature](r, *args)
                    router_config[f] = a
        elif feature in router_features:
            f, a = translation[feature](router, arg, *args)
            router_config[f] = a
        else:
            neighbour, direction, seq = arg
            if translation[feature](router, neighbour_filters[neighbour, direction], seq, *args):
                f, a = translation[feature](router, neighbour_filters[neighbour, direction], seq, *args)
                router_config[f] = a
            if direction == 'in':
                router_config[router, juniper_config_features.BGPFeatures.NEIGHBOUR_POLICY_IMPORT, neighbour] = (neighbour_filters[neighbour, direction],)
            else:
                router_config[router, juniper_config_features.BGPFeatures.NEIGHBOUR_POLICY_EXPORT, neighbour] = (neighbour_filters[neighbour, direction],)

    return router_config
