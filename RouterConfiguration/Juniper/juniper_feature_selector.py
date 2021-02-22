import itertools
import random

from RouterConfiguration.Juniper.juniper_config_features import *
from utils import filter_optional


def get_possible_args(router, allowed_features=None):
    static_route = list(itertools.product(
        router.static_routes, router.interfaces
    ))
    ospf_area_range = list(itertools.product(  # TODO
        random.sample(list(router.topology.network_list()), k=3),
        ['', 'override-metric 1', ' override-metric 200', 'override-metric 16777215'],
        ['', 'restrict']
    ))
    ospf_area_label_switched_path = list(itertools.product(
        ['paths'], [1, 100, 65535]
    ))
    ospf_nssa_default_lsa = list(itertools.product(
        [1, 100, 16777215], ['', 'metric-type 1', 'metric-type 2'], ['', 'type-7']
    ))
    ospf_nssa_no_summaries = [
        ()
    ]
    ospf_stub_default_metric = [
        (1,), (100,), (16777215,)
    ]
    ospf_stub_no_summaries = [
        ()
    ]
    ospf_external_preference = [
        (0,), (100,), (4294967295,)
    ]
    ospf_no_rfc_1583 = [
        ()
    ]
    ospf_reference_bandwidth = [
        (9600,), (1000000000,), (1000000000000,)
    ]
    ospf_interface_ldp_synchronization = [
        ('', 'disable')
    ]
    ospf_interface_link_protection = [
        ()
    ]
    ospf_interface_metric = [
        (1,), (100,), (65535,)
    ]
    ospf_interface_passive = [
        ()
    ]
    ospf_interface_priority = [
        (0,), (100,), (255,)
    ]
    ospf_interface_te_metric = [
        (1,), (100,), (65535,)
    ]
    ospf_redistribute_direct = [
        ()
    ]
    ospf_redistribute_static = [
        ()
    ]
    ospf_redistribute_bgp = [
        ()
    ]
    ospf_export = [
        ()
    ]
    ospf_import = [
        ()
    ]
    bgp_accepted_prefix_limit = [
        (1,), (10,), (4294967295,)
    ]
    bgp_advertise_external = [
        ('IBGP',)
    ]
    bgp_advertise_inactive = [
        ()
    ]
    bgp_advertise_peer_as = [
        ()
    ]
    bgp_as_override = [
        ('EBGP',)
    ]
    bgp_cluster = []
    bgp_damping = [
        ()
    ]
    bgp_enforce_first_as = [
        ()
    ]
    bgp_local_as = list(itertools.product(
        [AS for AS in router.topology.ASes if AS != router.AS],
        ['', ' alias ', ' private ']
    ))
    bgp_metric_out = []
    bgp_multihop = []
    bgp_no_client_reflect = [
        ()
    ]
    bgp_passive = [
        ()
    ]
    bgp_path_selection = [
        (' always-compare-med ',), (' external-router-id ',)
    ]
    bgp_remove_private = [
        ()
    ]
    bgp_tcp_mss = [
        (2048,), (4096,)
    ]
    bgp_add_path = list(itertools.product(
        ['IBGP'],
        ['receive', 'send path-count 2', 'send path-count 6']
        # 'send prefix-policy add-path-policy']
    ))
    bgp_loops = [
        (1,), (5,), (10,)
    ]
    bgp_prefix_limit = [
        (1,), (10,), (4294967295,)
    ]
    bgp_redistribute_direct = [
        ()
    ]
    bgp_redistribute_static = [
        ()
    ]
    bgp_redistribute_ospf = [
        ()
    ]
    bgp_import = [
        ()
    ]
    bgp_export = [
        ()
    ]
    bgp_local_preference = [
        (0,), (50,), (4294967295,)
    ]
    policy_as_path = []
    policy_as_path_group = []
    policy_community = []
    policy_condition = []
    policy_policy_statement = []
    policy_prefix_list = []
    policy_invert_match = []
    policy_members = []
    policy_apply_path = []
    policy_from_area = [
        (area,) for area in router.topology.ospf_areas
    ]
    policy_from_as_path = [
        (as_path,) for as_path in router.as_path_lists
    ]
    policy_from_as_path_group = []
    policy_from_color = [
        (0,), (1000,)  # , (4294967295,)
    ]
    policy_from_community = [
        (comm,) for comm in router.comm_lists
    ]
    policy_from_family = [
        ('inet',)
    ]
    policy_from_instance = []
    policy_from_interface = [
        (interface,) for interface in router.interfaces
    ]
    policy_from_level = []
    policy_from_local_preference = [
        (0,), (1000,), (4294967295,)
    ]
    policy_from_metric = [
        (1,), (100,), (65535,)
    ]
    policy_from_neighbour = [
        (neighbour,) for neighbour in router.bgp_neighbours
    ]
    policy_from_origin = [
        ('igp',), ('egp',), ('incomplete',)
    ]
    policy_from_policy = []
    policy_from_prefix_list = [
        (prefix_list,) for prefix_list in router.prefix_lists
    ]
    policy_from_prefix_list_filter = list(itertools.product(
        router.prefix_lists, ['exact', 'longer', 'orlonger']
    ))
    policy_from_protocol = [
        ('direct',), ('static',), ('ospf',), ('bgp',)
    ]
    policy_from_rib = []
    policy_from_route_filter = list(itertools.product(
        [], ['address-mask {mask}', 'exact', 'longer', 'orlonger', 'prefix-length-range {range}', 'through', 'upto']
    ))
    policy_from_route_type = [
        ('external',), ('internal',)
    ]
    policy_from_source_address_filter = []
    policy_from_tag = [
        (0,), (100,)  # , (4294967295,)
    ]
    policy_to_level = []
    policy_to_rib = []
    policy_then_accept = [
        ()
    ]
    policy_then_as_path_expand = [
        (1,), (16,), (32,)
    ]
    policy_then_as_path_prepend = [
        (as_path,) for as_path in router.topology.ASes
    ]
    policy_then_color = list(itertools.product(
        ['', 'add'], [0, 1000, 4294967295]
    ))
    policy_then_color2 = list(itertools.product(
        ['', 'add'], [0, 1000, 4294967295]
    ))
    policy_then_community_add = [
        (comm,) for comm in router.comm_lists
    ]
    policy_then_community_delete = [
        (comm,) for comm in router.comm_lists
    ]
    policy_then_community_set = [
        (comm,) for comm in router.comm_lists
    ]
    policy_then_cos_next_hop_map = []
    policy_then_default_action_accept = [
        ()
    ]
    policy_then_default_action_reject = [
        ()
    ]
    policy_then_external = [
        (1,), (2,)
    ]
    policy_then_forwarding_class = []
    policy_then_install_nexthop = []
    policy_then_local_preference = [
        (0,), (1000,), (4294967295,)
    ]
    policy_then_metric = [
        (1,), (100,), (65535,)
    ]
    policy_then_metric_add = [
        (1,), (100,), (65535,)
    ]
    policy_then_metric_expression = []
    policy_then_metric_igp = [
        (-65535,), (-100,), (100,), (65535,)
    ]
    policy_then_metric2 = [
        (1,), (100,), (65535,)
    ]
    policy_then_metric2_expression = []
    policy_then_next_hop = [
                               (r.router_id,) for r in router.topology.routers
                           ] + [('peer-address',)]
    policy_then_next_hop_self = [
        ()
    ]
    policy_then_next_policy = []
    policy_then_next_term = []
    policy_then_origin = [
        ('igp',), ('egp',), ('incomplete',)
    ]
    policy_then_preference = [
        (0,), (1000,), (4294967295,)
    ]
    policy_then_priority = [
        ('low',), ('medium',), ('high',)
    ]
    policy_then_reject = [
        ()
    ]
    policy_then_tag = [
        (0,), (100,) # , (4294967295,)
    ]

    possible_args = {
        ProtocolIndependentFeatures.STATIC_ROUTE: static_route,

        OSPFFeatures.AREA_RANGE: ospf_area_range,
        OSPFFeatures.AREA_LABEL_SWITCHED_PATH: ospf_area_label_switched_path,
        OSPFFeatures.NSSA_DEFAULT_LSA: ospf_nssa_default_lsa,
        OSPFFeatures.NSSA_NO_SUMMARIES: ospf_nssa_no_summaries,
        OSPFFeatures.STUB_DEFAULT_METRIC: ospf_stub_default_metric,
        OSPFFeatures.STUB_NO_SUMMARIES: ospf_stub_no_summaries,
        OSPFFeatures.EXTERNAL_PREFERENCE: ospf_external_preference,
        OSPFFeatures.NO_RFC_1583: ospf_no_rfc_1583,
        OSPFFeatures.REFERENCE_BANDWIDTH: ospf_reference_bandwidth,
        OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION: ospf_interface_ldp_synchronization,
        OSPFFeatures.INTERFACE_LINK_PROTECTION: ospf_interface_link_protection,
        OSPFFeatures.INTERFACE_METRIC: ospf_interface_metric,
        OSPFFeatures.INTERFACE_PASSIVE: ospf_interface_passive,
        OSPFFeatures.INTERFACE_PRIORITY: ospf_interface_priority,
        OSPFFeatures.INTERFACE_TE_METRIC: ospf_interface_te_metric,
        OSPFFeatures.REDISTRIBUTE_DIRECT: ospf_redistribute_direct,
        OSPFFeatures.REDISTRIBUTE_STATIC: ospf_redistribute_static,
        OSPFFeatures.REDISTRIBUTE_BGP: ospf_redistribute_bgp,
        OSPFFeatures.EXPORT: ospf_export,
        OSPFFeatures.IMPORT: ospf_import,

        BGPFeatures.ACCEPTED_PREFIX_LIMIT: bgp_accepted_prefix_limit,
        BGPFeatures.ADVERTISE_EXTERNAL: bgp_advertise_external,
        BGPFeatures.ADVERTISE_INACTIVE: bgp_advertise_inactive,
        BGPFeatures.ADVERTISE_PEER_AS: bgp_advertise_peer_as,
        BGPFeatures.AS_OVERRIDE: bgp_as_override,
        BGPFeatures.CLUSTER: bgp_cluster,
        BGPFeatures.DAMPING: bgp_damping,
        BGPFeatures.ENFORCE_FIRST_AS: bgp_enforce_first_as,
        BGPFeatures.LOCAL_AS: bgp_local_as,
        BGPFeatures.METRIC_OUT: bgp_metric_out,
        BGPFeatures.MULTIHOP: bgp_multihop,
        BGPFeatures.NO_CLIENT_REFLECT: bgp_no_client_reflect,
        BGPFeatures.PASSIVE: bgp_passive,
        BGPFeatures.PATH_SELECTION: bgp_path_selection,
        BGPFeatures.REMOVE_PRIVATE: bgp_remove_private,
        BGPFeatures.TCP_MSS: bgp_tcp_mss,
        BGPFeatures.ADD_PATH: bgp_add_path,
        BGPFeatures.LOOPS: bgp_loops,
        BGPFeatures.PREFIX_LIMIT: bgp_prefix_limit,
        BGPFeatures.REDISTRIBUTE_DIRECT: bgp_redistribute_direct,
        BGPFeatures.REDISTRIBUTE_STATIC: bgp_redistribute_static,
        BGPFeatures.REDISTRIBUTE_OSPF: bgp_redistribute_ospf,
        BGPFeatures.IMPORT: bgp_import,
        BGPFeatures.EXPORT: bgp_export,
        BGPFeatures.LOCAL_PREFERENCE: bgp_local_preference,

        PolicyFeatures.AS_PATH: policy_as_path,
        PolicyFeatures.AS_PATH_GROUP: policy_as_path_group,
        PolicyFeatures.COMMUNITY: policy_community,
        PolicyFeatures.CONDITION: policy_condition,
        PolicyFeatures.POLICY_STATEMENT: policy_policy_statement,
        PolicyFeatures.PREFIX_LIST: policy_prefix_list,
        PolicyFeatures.INVERT_MATCH: policy_invert_match,
        PolicyFeatures.MEMBERS: policy_members,
        PolicyFeatures.APPLY_PATH: policy_apply_path,
        PolicyFeatures.FROM_AREA: policy_from_area,
        PolicyFeatures.FROM_AS_PATH: policy_from_as_path,
        PolicyFeatures.FROM_AS_PATH_GROUP: policy_from_as_path_group,
        PolicyFeatures.FROM_COLOR: policy_from_color,
        PolicyFeatures.FROM_COMMUNITY: policy_from_community,
        PolicyFeatures.FROM_FAMILY: policy_from_family,
        PolicyFeatures.FROM_INSTANCE: policy_from_instance,
        PolicyFeatures.FROM_INTERFACE: policy_from_interface,
        PolicyFeatures.FROM_LEVEL: policy_from_level,
        PolicyFeatures.FROM_LOCAL_PREFERENCE: policy_from_local_preference,
        PolicyFeatures.FROM_METRIC: policy_from_metric,
        PolicyFeatures.FROM_NEIGHBOUR: policy_from_neighbour,
        PolicyFeatures.FROM_ORIGIN: policy_from_origin,
        PolicyFeatures.FROM_POLICY: policy_from_policy,
        PolicyFeatures.FROM_PREFIX_LIST: policy_from_prefix_list,
        PolicyFeatures.FROM_PREFIX_LIST_FILTER: policy_from_prefix_list_filter,
        PolicyFeatures.FROM_PROTOCOL: policy_from_protocol,
        PolicyFeatures.FROM_RIB: policy_from_rib,
        PolicyFeatures.FROM_ROUTE_FILTER: policy_from_route_filter,
        PolicyFeatures.FROM_ROUTE_TYPE: policy_from_route_type,
        PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER: policy_from_source_address_filter,
        PolicyFeatures.FROM_TAG: policy_from_tag,
        PolicyFeatures.TO_LEVEL: policy_to_level,
        PolicyFeatures.TO_RIB: policy_to_rib,
        PolicyFeatures.THEN_ACCEPT: policy_then_accept,
        PolicyFeatures.THEN_AS_PATH_EXPAND: policy_then_as_path_expand,
        PolicyFeatures.THEN_AS_PATH_PREPEND: policy_then_as_path_prepend,
        PolicyFeatures.THEN_COLOR: policy_then_color,
        PolicyFeatures.THEN_COLOR2: policy_then_color2,
        PolicyFeatures.THEN_COMMUNITY_ADD: policy_then_community_add,
        PolicyFeatures.THEN_COMMUNITY_DELETE: policy_then_community_delete,
        PolicyFeatures.THEN_COMMUNITY_SET: policy_then_community_set,
        PolicyFeatures.THEN_COS_NEXT_HOP_MAP: policy_then_cos_next_hop_map,
        PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT: policy_then_default_action_accept,
        PolicyFeatures.THEN_DEFAULT_ACTION_REJECT: policy_then_default_action_reject,
        PolicyFeatures.THEN_EXTERNAL: policy_then_external,
        PolicyFeatures.THEN_FORWARDING_CLASS: policy_then_forwarding_class,
        PolicyFeatures.THEN_INSTALL_NEXTHOP: policy_then_install_nexthop,
        PolicyFeatures.THEN_LOCAL_PREFERENCE: policy_then_local_preference,
        PolicyFeatures.THEN_METRIC: policy_then_metric,
        PolicyFeatures.THEN_METRIC_ADD: policy_then_metric_add,
        PolicyFeatures.THEN_METRIC_EXPRESSION: policy_then_metric_expression,
        PolicyFeatures.THEN_METRIC_IGP: policy_then_metric_igp,
        PolicyFeatures.THEN_METRIC2: policy_then_metric2,
        PolicyFeatures.THEN_METRIC2_EXPRESSION: policy_then_metric2_expression,
        PolicyFeatures.THEN_NEXT_HOP: policy_then_next_hop,
        PolicyFeatures.THEN_NEXT_HOP_SELF: policy_then_next_hop_self,
        PolicyFeatures.THEN_NEXT_POLICY: policy_then_next_policy,
        PolicyFeatures.THEN_NEXT_TERM: policy_then_next_term,
        PolicyFeatures.THEN_ORIGIN: policy_then_origin,
        PolicyFeatures.THEN_PREFERENCE: policy_then_preference,
        PolicyFeatures.THEN_PRIORITY: policy_then_priority,
        PolicyFeatures.THEN_REJECT: policy_then_reject,
        PolicyFeatures.THEN_TAG: policy_then_tag
    }

    match_ospf_out = [
        (feature, *args) for feature in filter_optional(match_features_ospf_out, allowed_features) for args in possible_args[feature]
    ]
    match_ospf_in = [
        (feature, *args) for feature in filter_optional(match_features_ospf_in, allowed_features) for args in possible_args[feature]
    ]
    set_ospf_out = [
        (feature, *args) for feature in filter_optional(set_features_ospf_out, allowed_features) for args in possible_args[feature]
    ]
    set_ospf_in = [
        (feature, *args) for feature in filter_optional(set_features_ospf_in, allowed_features) for args in possible_args[feature]
    ]
    match_bgp_out = [
        (feature, *args) for feature in filter_optional(match_features_bgp_out, allowed_features) for args in possible_args[feature]
    ]
    match_bgp_in = [
        (feature, *args) for feature in filter_optional(match_features_bgp_in, allowed_features) for args in possible_args[feature]
    ]
    set_bgp_out = [
        (feature, *args) for feature in filter_optional(set_features_bgp_out, allowed_features) for args in possible_args[feature]
    ]
    set_bgp_in = [
        (feature, *args) for feature in filter_optional(set_features_bgp_in, allowed_features) for args in possible_args[feature]
    ]
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_OUT] = match_ospf_out
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_IN] = match_ospf_in
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_OSPF_OUT] = set_ospf_out
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_OSPF_IN] = set_ospf_in
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT] = match_bgp_out
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN] = match_bgp_in
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT] = set_bgp_out
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_BGP_IN] = set_bgp_in

    return possible_args


def get_random_args(router, allowed_features=None):
    static_route = (random.choice(router.static_routes), random.choice(router.interfaces))
    ospf_area_range = (random.choice(list(router.topology.network_list())),
        random.choice(['', f'override-metric {random.randint(1, 16777215)}']),
        random.choice(['', 'restrict']))
    ospf_area_label_switched_path = ('paths', random.randint(1, 65535))
    ospf_nssa_default_lsa = (
        random.randint(1, 16777215),
        random.choice(['', 'metric-type 1', 'metric-type 2']),
        random.choice(['', 'type-7'])
    )
    ospf_nssa_no_summaries = ()
    ospf_stub_default_metric = (random.randint(1, 16777215),)
    ospf_stub_no_summaries = ()
    ospf_external_preference = (random.randint(0, 4294967295),)
    ospf_no_rfc_1583 = ()
    ospf_reference_bandwidth = (random.randint(9600, 1000000000000),)
    ospf_interface_ldp_synchronization = ('', 'disable')
    ospf_interface_link_protection = ()
    ospf_interface_metric = (random.randint(1, 65535),)
    ospf_interface_passive = ()
    ospf_interface_priority = (random.randint(0, 255),)
    ospf_interface_te_metric = (random.randint(1, 65535),)
    ospf_redistribute_direct = ()
    ospf_redistribute_static = ()
    ospf_redistribute_bgp = ()
    ospf_export = ()
    ospf_import = ()
    bgp_accepted_prefix_limit = (random.randint(1, 4294967295),)
    bgp_advertise_external = ('IBGP',)
    bgp_advertise_inactive = ()
    bgp_advertise_peer_as = ()
    bgp_as_override = ('EBGP',)
    bgp_cluster = ()
    bgp_damping = ()
    bgp_enforce_first_as = ()
    bgp_local_as = (
        random.choice([AS for AS in router.topology.ASes if AS != router.AS]),
        random.choice(['', ' alias ', ' private '])
    )
    bgp_metric_out = ()
    bgp_multihop = ()
    bgp_no_client_reflect = ()
    bgp_passive = ()
    bgp_path_selection = (random.choice([' always-compare-med ', ' external-router-id ']),)
    bgp_remove_private = ()
    bgp_tcp_mss = (random.choice([2048, 4096]),)
    bgp_add_path = ('IBGP', random.choice(['receive', f'send path-count {random.randint(2, 6)}']))
    bgp_loops = (random.randint(1, 10),)
    bgp_prefix_limit = (random.randint(1, 4294967295),)
    bgp_redistribute_direct = ()
    bgp_redistribute_static = ()
    bgp_redistribute_ospf = ()
    bgp_import = ()
    bgp_export = ()
    bgp_local_preference = (random.randint(0, 4294967295),)
    policy_as_path = ()
    policy_as_path_group = ()
    policy_community = ()
    policy_condition = ()
    policy_policy_statement = ()
    policy_prefix_list = ()
    policy_invert_match = ()
    policy_members = ()
    policy_apply_path = ()
    policy_from_area = (random.choice(router.topology.ospf_areas),)
    policy_from_as_path = (random.choice(router.as_path_lists),)
    policy_from_as_path_group = ()
    policy_from_color = (random.randint(0, 4294967295),)
    policy_from_community = (random.choice(router.comm_lists),)
    policy_from_family = ('inet',)
    policy_from_instance = ()
    policy_from_interface = (random.choice(router.interfaces),)
    policy_from_level = ()
    policy_from_local_preference = (random.randint(0, 4294967295),)
    policy_from_metric = (random.randint(1, 65535),)
    policy_from_neighbour = (random.choice(router.bgp_neighbours),)
    policy_from_origin = (random.choice(['igp', 'egp', 'incomplete']),)
    policy_from_policy = ()
    policy_from_prefix_list = (random.choice(router.prefix_lists),)
    policy_from_prefix_list_filter = (random.choice(router.prefix_lists), random.choice(['exact', 'longer', 'orlonger']))
    policy_from_protocol = (random.choice(['direct', 'static', 'ospf', 'bgp']))
    policy_from_rib = ()
    policy_from_route_filter = ()
    policy_from_route_type = (random.choice(['external', 'internal']),)
    policy_from_source_address_filter = ()
    policy_from_tag = (random.randint(0, 4294967295),)
    policy_to_level = ()
    policy_to_rib = ()
    policy_then_accept = ()
    policy_then_as_path_expand = (random.randint(1, 32),)
    policy_then_as_path_prepend = (random.choice(router.topology.ASes),)
    policy_then_color = (random.choice(['', 'add']), random.randint(0, 4294967295))
    policy_then_color2 = (random.choice(['', 'add']), random.randint(0, 4294967295))
    policy_then_community_add = (random.choice(router.comm_lists),)
    policy_then_community_delete = (random.choice(router.comm_lists),)
    policy_then_community_set = (random.choice(router.comm_lists),)
    policy_then_cos_next_hop_map = ()
    policy_then_default_action_accept = ()
    policy_then_default_action_reject = ()
    policy_then_external = (random.randint(1, 2),)
    policy_then_forwarding_class = ()
    policy_then_install_nexthop = ()
    policy_then_local_preference = (random.randint(0, 4294967295),)
    policy_then_metric = (random.randint(1, 65535),)
    policy_then_metric_add = (random.randint(1, 65535),)
    policy_then_metric_expression = ()
    policy_then_metric_igp = (random.randint(-65535, 65535),)
    policy_then_metric2 = (random.randint(1, 65535),)
    policy_then_metric2_expression = ()
    policy_then_next_hop = (random.choice(['peer-address', random.choice([r.router_id for r in router.topology.routers])]),)
    policy_then_next_hop_self = ()
    policy_then_next_policy = ()
    policy_then_next_term = ()
    policy_then_origin = (random.choice(['igp', 'egp', 'incomplete']),)
    policy_then_preference = (random.randint(0, 4294967295),)
    policy_then_priority = (random.choice(['low', 'medium', 'high']),)
    policy_then_reject = ()
    policy_then_tag = (random.randint(0, 4294967295),)

    possible_args = {
        ProtocolIndependentFeatures.STATIC_ROUTE: static_route,

        OSPFFeatures.AREA_RANGE: ospf_area_range,
        OSPFFeatures.AREA_LABEL_SWITCHED_PATH: ospf_area_label_switched_path,
        OSPFFeatures.NSSA_DEFAULT_LSA: ospf_nssa_default_lsa,
        OSPFFeatures.NSSA_NO_SUMMARIES: ospf_nssa_no_summaries,
        OSPFFeatures.STUB_DEFAULT_METRIC: ospf_stub_default_metric,
        OSPFFeatures.STUB_NO_SUMMARIES: ospf_stub_no_summaries,
        OSPFFeatures.EXTERNAL_PREFERENCE: ospf_external_preference,
        OSPFFeatures.NO_RFC_1583: ospf_no_rfc_1583,
        OSPFFeatures.REFERENCE_BANDWIDTH: ospf_reference_bandwidth,
        OSPFFeatures.INTERFACE_LDP_SYNCHRONIZATION: ospf_interface_ldp_synchronization,
        OSPFFeatures.INTERFACE_LINK_PROTECTION: ospf_interface_link_protection,
        OSPFFeatures.INTERFACE_METRIC: ospf_interface_metric,
        OSPFFeatures.INTERFACE_PASSIVE: ospf_interface_passive,
        OSPFFeatures.INTERFACE_PRIORITY: ospf_interface_priority,
        OSPFFeatures.INTERFACE_TE_METRIC: ospf_interface_te_metric,
        OSPFFeatures.REDISTRIBUTE_DIRECT: ospf_redistribute_direct,
        OSPFFeatures.REDISTRIBUTE_STATIC: ospf_redistribute_static,
        OSPFFeatures.REDISTRIBUTE_BGP: ospf_redistribute_bgp,
        OSPFFeatures.EXPORT: ospf_export,
        OSPFFeatures.IMPORT: ospf_import,

        BGPFeatures.ACCEPTED_PREFIX_LIMIT: bgp_accepted_prefix_limit,
        BGPFeatures.ADVERTISE_EXTERNAL: bgp_advertise_external,
        BGPFeatures.ADVERTISE_INACTIVE: bgp_advertise_inactive,
        BGPFeatures.ADVERTISE_PEER_AS: bgp_advertise_peer_as,
        BGPFeatures.AS_OVERRIDE: bgp_as_override,
        BGPFeatures.CLUSTER: bgp_cluster,
        BGPFeatures.DAMPING: bgp_damping,
        BGPFeatures.ENFORCE_FIRST_AS: bgp_enforce_first_as,
        BGPFeatures.LOCAL_AS: bgp_local_as,
        BGPFeatures.METRIC_OUT: bgp_metric_out,
        BGPFeatures.MULTIHOP: bgp_multihop,
        BGPFeatures.NO_CLIENT_REFLECT: bgp_no_client_reflect,
        BGPFeatures.PASSIVE: bgp_passive,
        BGPFeatures.PATH_SELECTION: bgp_path_selection,
        BGPFeatures.REMOVE_PRIVATE: bgp_remove_private,
        BGPFeatures.TCP_MSS: bgp_tcp_mss,
        BGPFeatures.ADD_PATH: bgp_add_path,
        BGPFeatures.LOOPS: bgp_loops,
        BGPFeatures.PREFIX_LIMIT: bgp_prefix_limit,
        BGPFeatures.REDISTRIBUTE_DIRECT: bgp_redistribute_direct,
        BGPFeatures.REDISTRIBUTE_STATIC: bgp_redistribute_static,
        BGPFeatures.REDISTRIBUTE_OSPF: bgp_redistribute_ospf,
        BGPFeatures.IMPORT: bgp_import,
        BGPFeatures.EXPORT: bgp_export,
        BGPFeatures.LOCAL_PREFERENCE: bgp_local_preference,

        PolicyFeatures.AS_PATH: policy_as_path,
        PolicyFeatures.AS_PATH_GROUP: policy_as_path_group,
        PolicyFeatures.COMMUNITY: policy_community,
        PolicyFeatures.CONDITION: policy_condition,
        PolicyFeatures.POLICY_STATEMENT: policy_policy_statement,
        PolicyFeatures.PREFIX_LIST: policy_prefix_list,
        PolicyFeatures.INVERT_MATCH: policy_invert_match,
        PolicyFeatures.MEMBERS: policy_members,
        PolicyFeatures.APPLY_PATH: policy_apply_path,
        PolicyFeatures.FROM_AREA: policy_from_area,
        PolicyFeatures.FROM_AS_PATH: policy_from_as_path,
        PolicyFeatures.FROM_AS_PATH_GROUP: policy_from_as_path_group,
        PolicyFeatures.FROM_COLOR: policy_from_color,
        PolicyFeatures.FROM_COMMUNITY: policy_from_community,
        PolicyFeatures.FROM_FAMILY: policy_from_family,
        PolicyFeatures.FROM_INSTANCE: policy_from_instance,
        PolicyFeatures.FROM_INTERFACE: policy_from_interface,
        PolicyFeatures.FROM_LEVEL: policy_from_level,
        PolicyFeatures.FROM_LOCAL_PREFERENCE: policy_from_local_preference,
        PolicyFeatures.FROM_METRIC: policy_from_metric,
        PolicyFeatures.FROM_NEIGHBOUR: policy_from_neighbour,
        PolicyFeatures.FROM_ORIGIN: policy_from_origin,
        PolicyFeatures.FROM_POLICY: policy_from_policy,
        PolicyFeatures.FROM_PREFIX_LIST: policy_from_prefix_list,
        PolicyFeatures.FROM_PREFIX_LIST_FILTER: policy_from_prefix_list_filter,
        PolicyFeatures.FROM_PROTOCOL: policy_from_protocol,
        PolicyFeatures.FROM_RIB: policy_from_rib,
        PolicyFeatures.FROM_ROUTE_FILTER: policy_from_route_filter,
        PolicyFeatures.FROM_ROUTE_TYPE: policy_from_route_type,
        PolicyFeatures.FROM_SOURCE_ADDRESS_FILTER: policy_from_source_address_filter,
        PolicyFeatures.FROM_TAG: policy_from_tag,
        PolicyFeatures.TO_LEVEL: policy_to_level,
        PolicyFeatures.TO_RIB: policy_to_rib,
        PolicyFeatures.THEN_ACCEPT: policy_then_accept,
        PolicyFeatures.THEN_AS_PATH_EXPAND: policy_then_as_path_expand,
        PolicyFeatures.THEN_AS_PATH_PREPEND: policy_then_as_path_prepend,
        PolicyFeatures.THEN_COLOR: policy_then_color,
        PolicyFeatures.THEN_COLOR2: policy_then_color2,
        PolicyFeatures.THEN_COMMUNITY_ADD: policy_then_community_add,
        PolicyFeatures.THEN_COMMUNITY_DELETE: policy_then_community_delete,
        PolicyFeatures.THEN_COMMUNITY_SET: policy_then_community_set,
        PolicyFeatures.THEN_COS_NEXT_HOP_MAP: policy_then_cos_next_hop_map,
        PolicyFeatures.THEN_DEFAULT_ACTION_ACCEPT: policy_then_default_action_accept,
        PolicyFeatures.THEN_DEFAULT_ACTION_REJECT: policy_then_default_action_reject,
        PolicyFeatures.THEN_EXTERNAL: policy_then_external,
        PolicyFeatures.THEN_FORWARDING_CLASS: policy_then_forwarding_class,
        PolicyFeatures.THEN_INSTALL_NEXTHOP: policy_then_install_nexthop,
        PolicyFeatures.THEN_LOCAL_PREFERENCE: policy_then_local_preference,
        PolicyFeatures.THEN_METRIC: policy_then_metric,
        PolicyFeatures.THEN_METRIC_ADD: policy_then_metric_add,
        PolicyFeatures.THEN_METRIC_EXPRESSION: policy_then_metric_expression,
        PolicyFeatures.THEN_METRIC_IGP: policy_then_metric_igp,
        PolicyFeatures.THEN_METRIC2: policy_then_metric2,
        PolicyFeatures.THEN_METRIC2_EXPRESSION: policy_then_metric2_expression,
        PolicyFeatures.THEN_NEXT_HOP: policy_then_next_hop,
        PolicyFeatures.THEN_NEXT_HOP_SELF: policy_then_next_hop_self,
        PolicyFeatures.THEN_NEXT_POLICY: policy_then_next_policy,
        PolicyFeatures.THEN_NEXT_TERM: policy_then_next_term,
        PolicyFeatures.THEN_ORIGIN: policy_then_origin,
        PolicyFeatures.THEN_PREFERENCE: policy_then_preference,
        PolicyFeatures.THEN_PRIORITY: policy_then_priority,
        PolicyFeatures.THEN_REJECT: policy_then_reject,
        PolicyFeatures.THEN_TAG: policy_then_tag
    }

    match_ospf_out = random.choice([
        (feature, *args) for feature in filter_optional(match_features_ospf_out, allowed_features) for args in
        possible_args[feature]
    ])
    match_ospf_in = random.choice([
        (feature, *args) for feature in filter_optional(match_features_ospf_in, allowed_features) for args in
        possible_args[feature]
    ])
    set_ospf_out = random.choice([
        (feature, *args) for feature in filter_optional(set_features_ospf_out, allowed_features) for args in
        possible_args[feature]
    ])
    set_ospf_in = random.choice([
        (feature, *args) for feature in filter_optional(set_features_ospf_in, allowed_features) for args in
        possible_args[feature]
    ])
    match_bgp_out = random.choice([
        (feature, *args) for feature in filter_optional(match_features_bgp_out, allowed_features) for args in
        possible_args[feature]
    ])
    match_bgp_in = random.choice([
        (feature, *args) for feature in filter_optional(match_features_bgp_in, allowed_features) for args in
        possible_args[feature]
    ])
    set_bgp_out = random.choice([
        (feature, *args) for feature in filter_optional(set_features_bgp_out, allowed_features) for args in
        possible_args[feature]
    ])
    set_bgp_in = random.choice([
        (feature, *args) for feature in filter_optional(set_features_bgp_in, allowed_features) for args in
        possible_args[feature]
    ])
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_OUT] = match_ospf_out
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_OSPF_IN] = match_ospf_in
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_OSPF_OUT] = set_ospf_out
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_OSPF_IN] = set_ospf_in
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_BGP_OUT] = match_bgp_out
    possible_args[PolicyFeatures.POLICY_MATCH_FEATURE_BGP_IN] = match_bgp_in
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_BGP_OUT] = set_bgp_out
    possible_args[PolicyFeatures.POLICY_SET_FEATURE_BGP_IN] = set_bgp_in

    return possible_args
