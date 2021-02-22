import itertools
import random

from RouterConfiguration.Cisco.cisco_config_features import *
from utils import filter_optional


def get_possible_args(router, allowed_features=None):
    static_route = list(itertools.product(
        router.static_routes, router.interfaces
    ))
    interface_ospf_cost = [
        (1,), (100,), (65535,)
    ]
    interface_ospf_priority = [
        (0,), (10,), (255,)
    ]
    ospf_auto_cost = [
        (1,), (1000,), (4294967,)
    ]
    ospf_no_compatible_rfc1583 = [
        ()
    ]
    ospf_default_originate = list(itertools.product(
        ['', ' always '], ['', ' metric 1', ' metric 100', ' metric 1677214'],
        ['', ' metric-type 1', ' metric-type 2']
    ))
    ospf_default_metric = [
        (1,), (100,), (1677214,)
    ]
    ospf_distance = [
        (10,), (100,), (255,)
    ]
    ospf_redistribute_connected = [
        (' subnets ',),  ('',)
    ]
    ospf_redistribute_static = [
        (' subnets ',),  ('',)
    ]
    ospf_redistribute_bgp = [
        (router.AS, ' subnets '),  (router.AS, '')
    ]
    ospf_max_metric = list(itertools.product(
        ['', ' external-lsa 1', ' external-lsa 1000', ' external-lsa 16777215'], ['', ' include-stub '],
        ['', ' summary-lsa 1', ' summary-lsa 1000', ' summary-lsa 16777215']
    ))
    ospf_area_filter_list = list(itertools.product(
        router.prefix_lists, [' in ', ' out ']
    ))
    ospf_area_range = list(itertools.product(
        router.topology.networks[router], ['', ' advertise ', ' not-advertise '],
        ['', ' cost 1', ' cost 100', ' cost 16777215']
    ))
    ospf_nssa_stub_area_default_cost = [
        (1,), (100,), (16777215,)
    ]
    ospf_nssa_area_no_redistribution = [
        ()
    ]
    ospf_nssa_area_default_information_originate = list(itertools.product(
        ['', ' metric 1', ' metric 100', ' metric 1677214'],
        ['', ' metric-type 1 ', ' metric-type 2 ']
    ))
    ospf_nssa_area_no_summary = [
        ()
    ]
    ospf_nssa_area_nssa_only = [
        ()
    ]
    ospf_stub_area_no_summary = [
        ()
    ]
    bgp_always_compare_med = [
        ()
    ]
    bgp_bestpath_compare_routerid = [
        ()
    ]
    bgp_bestpath_med_confed = [
        ('',), (' missing-as-worst ',)
    ]
    bgp_bestpath_med_missing = [
        ()
    ]
    bgp_no_client_to_client_reflection = [
        ()
    ]
    bgp_default_local_preference = [
        (0,), (50,), (4294967295,)
    ]
    bgp_deterministic_med = [
        ()
    ]
    bgp_maxas_limit = [
        (1,), (10,), (254,)
    ]
    bgp_default_information_originate = [
        ()
    ]
    bgp_additional_paths_install = [
        ()
    ]
    bgp_auto_summary = [
        ()
    ]
    bgp_dampening = [
        (route_map,) for route_map in router.bgp_in_route_maps + [None]
    ]
    bgp_distance = list(itertools.product(
        [1, 100, 255], repeat=3)
    )
    bgp_redistribute_connected = [
        (None,),  *[(route_map,) for route_map in router.bgp_out_route_maps]
    ]
    bgp_redistribute_static = [
        (None,),  *[(route_map,) for route_map in router.bgp_out_route_maps]
    ]
    bgp_redistribute_ospf = [
        (None,),  *[(route_map,) for route_map in router.bgp_out_route_maps]
    ]
    bgp_synchronization = [
        ()
    ]
    bgp_table_map = [
        ('', route_map) for route_map in router.bgp_in_route_maps
    ]
    bgp_aggregate_address = list(itertools.product(
        router.topology.networks[router], ['', ' as-set '], ['', ' summary-only ']
    ))
    bgp_additional_paths = [
        (' send ',), (' receive ',), (' send receive ',)
    ]
    bgp_neighbour_maximum_prefix = [
        (1,), (100,), (10000,)
    ]
    bgp_neighbour_route_map_in = [
        (rm,) for rm in router.bgp_in_route_maps
    ]
    bgp_neighbour_route_map_out = [
        (rm,) for rm in router.bgp_out_route_maps
    ]
    bgp_neighbour_next_hop_self = [
        ()
    ]
    bgp_neighbour_capability_orf_prefix_list = [
        (' receive ',), (' send ',), (' both ',)
    ]
    bgp_neighbour_default_originate = [
        (route_map,) for route_map in router.bgp_out_route_maps + [None]
    ]
    bgp_neighbour_route_reflector_client = [
        ()
    ]
    bgp_neighbour_weight = [
        (0,), (1000,), (65535,)
    ]

    match_interface = [
        (interface,) for interface in router.interfaces
    ]
    match_ip_address = [
        (prefix_list,) for prefix_list in router.prefix_lists
    ]
    set_interface = [
        (interface,) for interface in router.interfaces
    ]
    set_ip_default_next_hop = [
        (neighbour.address,) for neighbour in router.bgp_neighbours
    ]
    set_ip_next_hop = [
        (neighbour.address,) for neighbour in router.bgp_neighbours
    ]
    set_metric = [
        (1000,), (294967295,), (-294967295,), (-1000,)
    ]
    match_as_path = [
        (as_path_list,) for as_path_list in router.as_path_lists
    ]
    match_community = list(itertools.product(
        router.comm_lists, ['', 'exact']
    ))
    set_local_preference = [
        (0,), (50,), (4294967295,)
    ]
    set_as_path = [
        (AS,) for AS in router.topology.ASes
    ]
    set_comm_list_delete = [
        (comm_list,) for comm_list in router.comm_lists
    ]
    set_community = list(itertools.product(
        [comm for (AS, comm) in router.topology.communities if AS == router.AS], ['', 'additive']
    )) + [('no-export', ''), ('no-advertise', ''), ('internet', ''), ('local-as', ''), ('none', '')]
    set_origin = [
        ('igp',), ('incomplete',), *[(f'egp {AS}',) for AS in router.topology.ASes]
    ]
    set_weight = [
        (0,), (1000,), (65535,)
    ]
    route_map_deny = [
        ()
    ]

    possible_args = {
        RouterFeatures.STATIC_ROUTE: static_route,

        OSPFFeatures.INTERFACE_OSPF_COST: interface_ospf_cost,
        OSPFFeatures.INTERFACE_OSPF_PRIORITY: interface_ospf_priority,
        OSPFFeatures.AUTO_COST: ospf_auto_cost,
        OSPFFeatures.NO_COMPATIBLE_RFC1583: ospf_no_compatible_rfc1583,
        OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE: ospf_default_originate,
        OSPFFeatures.DEFAULT_METRIC: ospf_default_metric,
        OSPFFeatures.DISTANCE: ospf_distance,
        OSPFFeatures.REDISTRIBUTE_CONNECTED: ospf_redistribute_connected,
        OSPFFeatures.REDISTRIBUTE_STATIC: ospf_redistribute_static,
        OSPFFeatures.REDISTRIBUTE_BGP: ospf_redistribute_bgp,
        OSPFFeatures.MAX_METRIC: ospf_max_metric,
        OSPFFeatures.AREA_FILTER_LIST: ospf_area_filter_list,
        OSPFFeatures.AREA_RANGE: ospf_area_range,
        OSPFFeatures.NSSA_STUB_DEFAULT_COST: ospf_nssa_stub_area_default_cost,
        OSPFFeatures.NSSA_NO_REDISTRIBUTION: ospf_nssa_area_no_redistribution,
        OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE: ospf_nssa_area_default_information_originate,
        OSPFFeatures.NSSA_NO_SUMMARY: ospf_nssa_area_no_summary,
        OSPFFeatures.NSSA_ONLY: ospf_nssa_area_nssa_only,
        OSPFFeatures.STUB_NO_SUMMARY: ospf_stub_area_no_summary,

        BGPFeatures.ALWAYS_COMPARE_MED: bgp_always_compare_med,
        BGPFeatures.BESTPATH_COMPARE_ROUTERID: bgp_bestpath_compare_routerid,
        BGPFeatures.BESTPATH_MED_CONFED: bgp_bestpath_med_confed,
        BGPFeatures.BESTPATH_MED_MISSING: bgp_bestpath_med_missing,
        BGPFeatures.NO_CLIENT_TO_CLIENT_REFLECTION: bgp_no_client_to_client_reflection,
        BGPFeatures.DEFAULT_LOCAL_PREFERENCE: bgp_default_local_preference,
        BGPFeatures.DETERMINISTIC_MED: bgp_deterministic_med,
        BGPFeatures.MAXAS_LIMIT: bgp_maxas_limit,
        BGPFeatures.DEFAULT_INFORMATION_ORIGINATE: bgp_default_information_originate,
        BGPFeatures.ADDITIONAL_PATHS_INSTALL: bgp_additional_paths_install,
        BGPFeatures.AUTO_SUMMARY: bgp_auto_summary,
        BGPFeatures.BGP_DAMPENING: bgp_dampening,
        BGPFeatures.DISTANCE_BGP: bgp_distance,
        BGPFeatures.REDISTRIBUTE_CONNECTED: bgp_redistribute_connected,
        BGPFeatures.REDISTRIBUTE_STATIC: bgp_redistribute_static,
        BGPFeatures.REDISTRIBUTE_OSPF: bgp_redistribute_ospf,
        BGPFeatures.SYNCHRONIZATION: bgp_synchronization,
        BGPFeatures.TABLE_MAP: bgp_table_map,
        BGPFeatures.AGGREGATE_ADDRESS: bgp_aggregate_address,
        BGPFeatures.ADDITIONAL_PATHS: bgp_additional_paths,
        BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX: bgp_neighbour_maximum_prefix,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN: bgp_neighbour_route_map_in,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT: bgp_neighbour_route_map_out,
        BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF: bgp_neighbour_next_hop_self,
        BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST: bgp_neighbour_capability_orf_prefix_list,
        BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE: bgp_neighbour_default_originate,
        BGPFeatures.NEIGHBOUR_ROUTE_REFLECTOR_CLIENT: bgp_neighbour_route_reflector_client,
        BGPFeatures.NEIGHBOUR_WEIGHT: bgp_neighbour_weight,

        RouteMapFeatures.MATCH_INTERFACE: match_interface,
        RouteMapFeatures.MATCH_IP_PREFIX_LIST: match_ip_address,
        RouteMapFeatures.SET_INTERFACE: set_interface,
        RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP: set_ip_default_next_hop,
        RouteMapFeatures.SET_IP_NEXT_HOP: set_ip_next_hop,
        RouteMapFeatures.SET_METRIC: set_metric,
        RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST: match_as_path,
        RouteMapFeatures.MATCH_COMMUNITY_LIST: match_community,
        RouteMapFeatures.SET_LOCAL_PREFERENCE: set_local_preference,
        RouteMapFeatures.SET_AS_PATH_PREPEND: set_as_path,
        RouteMapFeatures.SET_COMM_LIST_DELETE: set_comm_list_delete,
        RouteMapFeatures.SET_COMMUNITY: set_community,
        RouteMapFeatures.SET_ORIGIN: set_origin,
        RouteMapFeatures.SET_WEIGHT: set_weight,
        RouteMapFeatures.ROUTE_MAP_DENY: route_map_deny,
    }

    match_features_bgp_out = [
        (feature, *args) for feature in filter_optional(match_features_out, allowed_features) for args in possible_args[feature]
    ]
    match_features_bgp_in = [
        (feature, *args) for feature in filter_optional(match_features_in, allowed_features) for args in possible_args[feature]
    ]
    set_features_bgp_out = [
        (feature, *args) for feature in filter_optional(set_features_out, allowed_features) for args in possible_args[feature]
    ]
    set_features_bgp_in = [
        (feature, *args) for feature in filter_optional(set_features_in, allowed_features) for args in possible_args[feature]
    ]
    possible_args[RouteMapFeatures.MATCH_FEATURE_BGP_OUT] = match_features_bgp_out
    possible_args[RouteMapFeatures.MATCH_FEATURE_BGP_IN] = match_features_bgp_in
    possible_args[RouteMapFeatures.SET_FEATURE_BGP_OUT] = set_features_bgp_out
    possible_args[RouteMapFeatures.SET_FEATURE_BGP_IN] = set_features_bgp_in

    return possible_args


def get_random_args(router, allowed_features=None):
    static_route = (random.choice(router.static_routes), random.choice(router.interfaces))
    interface_ospf_cost = (random.randint(1, 65535),)
    interface_ospf_priority = (random.randint(0, 255),)
    ospf_auto_cost = (random.randint(1, 4294967),)
    ospf_no_compatible_rfc1583 = ()
    ospf_default_originate = (random.choice(['', ' always ']),
                              random.choice(['', ' metric ' + str(random.randint(1, 1677214))]),
                              random.choice(['', ' metric-type 1', ' metric-type 2']))
    ospf_default_metric = (random.randint(1, 1677214),)
    ospf_distance = (random.randint(10, 255),)
    ospf_redistribute_connected = (random.choice(['', ' subnets ']),)
    ospf_redistribute_static = (random.choice(['', ' subnets ']),)
    ospf_redistribute_bgp = (router.AS, random.choice(['', ' subnets ']))
    ospf_max_metric = (random.choice(['', ' external-lsa ' + str(random.randint(1, 16777215))]),
                       random.choice(['', ' include-stub ']),
                       random.choice(['', ' summary-lsa ' + str(random.randint(1, 16777215))]))
    ospf_area_filter_list = (random.choice(router.prefix_lists), random.choice([' in ', ' out ']))
    ospf_area_range = (random.choice(router.topology.networks[router]),
                       random.choice(['', ' advertise ', ' not-advertise ']),
                       random.choice(['', ' cost ' + str(random.randint(1, 16777215))]))
    ospf_nssa_stub_area_default_cost = (random.randint(1, 16777215),)
    ospf_nssa_area_no_redistribution = ()
    ospf_nssa_area_default_information_originate = (random.choice(['', ' metric ' + str(random.randint(1, 1677214))]),
                                                    random.choice(['', ' metric-type 1 ', ' metric-type 2 ']))
    ospf_nssa_area_no_summary = ()
    ospf_nssa_area_nssa_only = ()
    ospf_stub_area_no_summary = ()
    bgp_always_compare_med = ()
    bgp_bestpath_compare_routerid = ()
    bgp_bestpath_med_confed = (random.choice(['', ' missing-as-worst ']),)
    bgp_bestpath_med_missing = ()
    bgp_no_client_to_client_reflection = ()
    bgp_default_local_preference = (random.randint(0, 4294967295),)
    bgp_deterministic_med = ()
    bgp_maxas_limit = (random.randint(1, 254),)
    bgp_default_information_originate = ()
    bgp_additional_paths_install = ()
    bgp_auto_summary = ()
    bgp_dampening = (random.choice(router.bgp_in_route_maps + [None]),)
    bgp_distance = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
    bgp_redistribute_connected = (random.choice(router.bgp_out_route_maps + [None]),)
    bgp_redistribute_static = (random.choice(router.bgp_out_route_maps + [None]),)
    bgp_redistribute_ospf = (random.choice(router.bgp_out_route_maps + [None]),)
    bgp_synchronization = ()
    bgp_table_map = ('', random.choice(router.bgp_in_route_maps))
    bgp_aggregate_address = (random.choice(router.topology.networks[router]),
                             random.choice(['', ' as-set ']),
                             random.choice(['', ' summary-only ']))
    bgp_additional_paths = (random.choice([' send ', ' receive ', ' send receive ']))
    bgp_neighbour_maximum_prefix = (random.randint(1, 10000),)
    bgp_neighbour_route_map_in = (random.choice(router.bgp_in_route_maps),)
    bgp_neighbour_route_map_out = (random.choice(router.bgp_in_route_maps),)
    bgp_neighbour_next_hop_self = ()
    bgp_neighbour_capability_orf_prefix_list = (random.choice([' receive ', ' send ', ' both ']),)
    bgp_neighbour_default_originate = (random.choice(router.bgp_out_route_maps + [None]),)
    bgp_neighbour_route_reflector_client = ()
    bgp_neighbour_weight = (random.randint(0, 65535),)

    match_interface = (random.choice(router.interfaces),)
    match_ip_address = (random.choice(router.prefix_lists),)
    set_interface = (random.choice(router.interfaces),)
    set_ip_default_next_hop = (random.choice([neighbour.address for neighbour in router.bgp_neighbours]),)
    set_ip_next_hop = (random.choice([neighbour.address for neighbour in router.bgp_neighbours]),)
    set_metric = (random.randint(-294967295, 294967295),)
    match_as_path = (random.choice(router.as_path_lists),)
    match_community = (random.choice(router.comm_lists), random.choice(['', 'exact']))
    set_local_preference = (random.randint(0, 4294967295),)
    set_as_path = (random.choice(router.topology.ASes),)
    set_comm_list_delete = (random.choice(router.comm_lists),)
    set_community = random.choice([
        (random.choice([f'{AS}:{comm}' for (AS, comm) in router.topology.communities if AS == router.AS]),
         random.choice(['', 'additive'])),
        ('no-export', ''), ('no-advertise', ''), ('internet', ''), ('local-as', ''), ('none', '')])
    set_origin = (random.choice(['igp', 'incomplete', *[f'egp {AS}' for AS in router.topology.ASes]]),)
    set_weight = (random.randint(0, 65535),)
    route_map_deny = ()

    args = {
        RouterFeatures.STATIC_ROUTE: static_route,

        OSPFFeatures.INTERFACE_OSPF_COST: interface_ospf_cost,
        OSPFFeatures.INTERFACE_OSPF_PRIORITY: interface_ospf_priority,
        OSPFFeatures.AUTO_COST: ospf_auto_cost,
        OSPFFeatures.NO_COMPATIBLE_RFC1583: ospf_no_compatible_rfc1583,
        OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE: ospf_default_originate,
        OSPFFeatures.DEFAULT_METRIC: ospf_default_metric,
        OSPFFeatures.DISTANCE: ospf_distance,
        OSPFFeatures.REDISTRIBUTE_CONNECTED: ospf_redistribute_connected,
        OSPFFeatures.REDISTRIBUTE_STATIC: ospf_redistribute_static,
        OSPFFeatures.REDISTRIBUTE_BGP: ospf_redistribute_bgp,
        OSPFFeatures.MAX_METRIC: ospf_max_metric,
        OSPFFeatures.AREA_FILTER_LIST: ospf_area_filter_list,
        OSPFFeatures.AREA_RANGE: ospf_area_range,
        OSPFFeatures.NSSA_STUB_DEFAULT_COST: ospf_nssa_stub_area_default_cost,
        OSPFFeatures.NSSA_NO_REDISTRIBUTION: ospf_nssa_area_no_redistribution,
        OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE: ospf_nssa_area_default_information_originate,
        OSPFFeatures.NSSA_NO_SUMMARY: ospf_nssa_area_no_summary,
        OSPFFeatures.NSSA_ONLY: ospf_nssa_area_nssa_only,
        OSPFFeatures.STUB_NO_SUMMARY: ospf_stub_area_no_summary,

        BGPFeatures.ALWAYS_COMPARE_MED: bgp_always_compare_med,
        BGPFeatures.BESTPATH_COMPARE_ROUTERID: bgp_bestpath_compare_routerid,
        BGPFeatures.BESTPATH_MED_CONFED: bgp_bestpath_med_confed,
        BGPFeatures.BESTPATH_MED_MISSING: bgp_bestpath_med_missing,
        BGPFeatures.NO_CLIENT_TO_CLIENT_REFLECTION: bgp_no_client_to_client_reflection,
        BGPFeatures.DEFAULT_LOCAL_PREFERENCE: bgp_default_local_preference,
        BGPFeatures.DETERMINISTIC_MED: bgp_deterministic_med,
        BGPFeatures.MAXAS_LIMIT: bgp_maxas_limit,
        BGPFeatures.DEFAULT_INFORMATION_ORIGINATE: bgp_default_information_originate,
        BGPFeatures.ADDITIONAL_PATHS_INSTALL: bgp_additional_paths_install,
        BGPFeatures.AUTO_SUMMARY: bgp_auto_summary,
        BGPFeatures.BGP_DAMPENING: bgp_dampening,
        BGPFeatures.DISTANCE_BGP: bgp_distance,
        BGPFeatures.REDISTRIBUTE_CONNECTED: bgp_redistribute_connected,
        BGPFeatures.REDISTRIBUTE_STATIC: bgp_redistribute_static,
        BGPFeatures.REDISTRIBUTE_OSPF: bgp_redistribute_ospf,
        BGPFeatures.SYNCHRONIZATION: bgp_synchronization,
        BGPFeatures.TABLE_MAP: bgp_table_map,
        BGPFeatures.AGGREGATE_ADDRESS: bgp_aggregate_address,
        BGPFeatures.ADDITIONAL_PATHS: bgp_additional_paths,
        BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX: bgp_neighbour_maximum_prefix,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN: bgp_neighbour_route_map_in,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT: bgp_neighbour_route_map_out,
        BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF: bgp_neighbour_next_hop_self,
        BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST: bgp_neighbour_capability_orf_prefix_list,
        BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE: bgp_neighbour_default_originate,
        BGPFeatures.NEIGHBOUR_ROUTE_REFLECTOR_CLIENT: bgp_neighbour_route_reflector_client,
        BGPFeatures.NEIGHBOUR_WEIGHT: bgp_neighbour_weight,

        RouteMapFeatures.MATCH_INTERFACE: match_interface,
        RouteMapFeatures.MATCH_IP_PREFIX_LIST: match_ip_address,
        RouteMapFeatures.SET_INTERFACE: set_interface,
        RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP: set_ip_default_next_hop,
        RouteMapFeatures.SET_IP_NEXT_HOP: set_ip_next_hop,
        RouteMapFeatures.SET_METRIC: set_metric,
        RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST: match_as_path,
        RouteMapFeatures.MATCH_COMMUNITY_LIST: match_community,
        RouteMapFeatures.SET_LOCAL_PREFERENCE: set_local_preference,
        RouteMapFeatures.SET_AS_PATH_PREPEND: set_as_path,
        RouteMapFeatures.SET_COMM_LIST_DELETE: set_comm_list_delete,
        RouteMapFeatures.SET_COMMUNITY: set_community,
        RouteMapFeatures.SET_ORIGIN: set_origin,
        RouteMapFeatures.SET_WEIGHT: set_weight,
        RouteMapFeatures.ROUTE_MAP_DENY: route_map_deny,
    }

    match_features_bgp_out = random.choice([(feature, *args[feature]) for feature in filter_optional(match_features_out, allowed_features)])
    match_features_bgp_in = random.choice([(feature, *args[feature]) for feature in filter_optional(match_features_in, allowed_features)])
    set_features_bgp_out = random.choice([(feature, *args[feature]) for feature in filter_optional(set_features_out, allowed_features)])
    set_features_bgp_in = random.choice([(feature, *args[feature]) for feature in filter_optional(set_features_in, allowed_features)])
    args[RouteMapFeatures.MATCH_FEATURE_BGP_OUT] = match_features_bgp_out
    args[RouteMapFeatures.MATCH_FEATURE_BGP_IN] = match_features_bgp_in
    args[RouteMapFeatures.SET_FEATURE_BGP_OUT] = set_features_bgp_out
    args[RouteMapFeatures.SET_FEATURE_BGP_IN] = set_features_bgp_in

    return args
