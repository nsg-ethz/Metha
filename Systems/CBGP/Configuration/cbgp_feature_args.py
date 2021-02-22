from Systems.CBGP.Configuration.cbgp_config_features import *
from utils import filter_optional


def get_possible_args(router, allowed_features=None):

    local_pref = [
        (0,), (50,), (4294967295,)
    ]
    med = [
        ('deterministic',), ('always-compare',)
    ]

    if router is None:
        possible_args = {
            GlobalFeatures.LOCAL_PREF: local_pref,
            GlobalFeatures.MED: med,
        }
        return possible_args

    next_hop = [
        (r.router_id,) for r in router.topology.routers
    ]
    next_hop_self = [
        ()
    ]
    igp_weight = [
        (1,), (100,), (65535,)
    ]
    static_route = [
        (net, iface) for net in router.static_routes for iface in router.interfaces
    ]
    action_accept = [
        ()
    ]
    action_deny = [
        ()
    ]
    action_call = []
    action_jump = []
    action_local_pref = [
        (0,), (50,), (4294967295,)
    ]
    action_metric = [
        (0,), (1000,), (65535,)
    ]
    action_metric_internal = [
        ()
    ]
    action_community_add = [
        (f'{AS}:{comm}',) for (AS, comm) in router.topology.communities if AS == router.AS
    ]
    action_community_strip = [
        ()
    ]
    action_community_remove = [
        (f'{AS}:{comm}',) for (AS, comm) in router.topology.communities
    ]
    action_as_path_prepend = [
        (1,), (5,), (10,)
    ]
    action_as_path_remove_private = []
    action_red_community_add = []
    match_any = [
        ()
    ]
    match_community = [
        (f'{AS}:{comm}',) for (AS, comm) in router.topology.communities
    ]
    match_next_hop = list(set([
        (neighbour.address,) for neighbour in router.bgp_neighbours
    ]))
    match_next_hop_in = []
    match_prefix = []
    match_prefix_in = []
    match_path = [
        (AS,) for AS in router.topology.ASes
    ]

    possible_args = {
        GlobalFeatures.LOCAL_PREF: local_pref,
        GlobalFeatures.MED: med,

        RouterFeatures.NEXT_HOP: next_hop,
        RouterFeatures.NEXT_HOP_SELF: next_hop_self,
        RouterFeatures.IGP_WEIGHT: igp_weight,
        RouterFeatures.STATIC_ROUTE: static_route,

        FilterFeatures.ACTION_ACCEPT: action_accept,
        FilterFeatures.ACTION_DENY: action_deny,
        FilterFeatures.ACTION_CALL: action_call,
        FilterFeatures.ACTION_JUMP: action_jump,
        FilterFeatures.ACTION_LOCAL_PREF: action_local_pref,
        FilterFeatures.ACTION_METRIC: action_metric,
        FilterFeatures.ACTION_METRIC_INTERNAL: action_metric_internal,
        FilterFeatures.ACTION_COMMUNITY_ADD: action_community_add,
        FilterFeatures.ACTION_COMMUNITY_STRIP: action_community_strip,
        FilterFeatures.ACTION_COMMUNITY_REMOVE: action_community_remove,
        FilterFeatures.ACTION_AS_PATH_PREPEND: action_as_path_prepend,
        FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE: action_as_path_remove_private,
        FilterFeatures.ACTION_RED_COMMUNITY_ADD: action_red_community_add,
        FilterFeatures.MATCH_ANY: match_any,
        FilterFeatures.MATCH_COMMUNITY: match_community,
        FilterFeatures.MATCH_NEXT_HOP: match_next_hop,
        FilterFeatures.MATCH_NEXT_HOP_IN: match_next_hop_in,
        FilterFeatures.MATCH_PREFIX: match_prefix,
        FilterFeatures.MATCH_PREFIX_IN: match_prefix_in,
        FilterFeatures.MATCH_PATH: match_path
    }

    filter_match_in = [
        (feature, *args) for feature in filter_optional(filter_match_features_in, allowed_features) for args in possible_args[feature]
    ]
    filter_match_out = [
        (feature, *args) for feature in filter_optional(filter_match_features_out, allowed_features) for args in possible_args[feature]
    ]

    filter_action_in = [
        (feature, *args) for feature in filter_optional(filter_action_features_in, allowed_features) for args in possible_args[feature]
    ]
    filter_action_out = [
        (feature, *args) for feature in filter_optional(filter_action_features_out, allowed_features) for args in possible_args[feature]
    ]

    possible_args[FilterFeatures.FILTER_MATCH_IN] = filter_match_in
    possible_args[FilterFeatures.FILTER_ACTION_IN] = filter_action_in
    possible_args[FilterFeatures.FILTER_MATCH_OUT] = filter_match_out
    possible_args[FilterFeatures.FILTER_ACTION_OUT] = filter_action_out

    return possible_args
