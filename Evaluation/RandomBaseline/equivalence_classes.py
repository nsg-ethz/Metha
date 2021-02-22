from Evaluation import coverage
from RouterConfiguration.Cisco.cisco_config_features import RouterFeatures, OSPFFeatures, BGPFeatures, RouteMapFeatures


def get_extra_equiv_class(feature):
    """
    Checks whether this feature requires a special equivalence class for the random baseline
    :param feature: feature for which we are generating equivalence classes
    :return: True if the feature requires a special equivalence class, False otherwise
    """
    extra = [
        RouterFeatures.STATIC_ROUTE,

        OSPFFeatures.AREA_FILTER_LIST,
        OSPFFeatures.AREA_RANGE,

        BGPFeatures.BGP_DAMPENING,
        BGPFeatures.REDISTRIBUTE_CONNECTED,
        BGPFeatures.REDISTRIBUTE_STATIC,
        BGPFeatures.REDISTRIBUTE_OSPF,
        BGPFeatures.TABLE_MAP,
        BGPFeatures.AGGREGATE_ADDRESS,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT,
        BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE,

        RouteMapFeatures.MATCH_INTERFACE,
        RouteMapFeatures.MATCH_IP_PREFIX_LIST,
        RouteMapFeatures.SET_INTERFACE,
        RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP,
        RouteMapFeatures.SET_IP_NEXT_HOP,
        RouteMapFeatures.SET_METRIC,
        RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST,
        RouteMapFeatures.MATCH_COMMUNITY_LIST,
        RouteMapFeatures.SET_AS_PATH_PREPEND,
        RouteMapFeatures.SET_COMM_LIST_DELETE,
        RouteMapFeatures.SET_COMMUNITY,
        RouteMapFeatures.SET_ORIGIN,

    ]

    return feature in extra


def get_equiv_class(router, feature, args):
    """
    Generates the equivalence class for features for which get_extra_equiv_class evaluates to true
    :param router: router for the current configuration feature
    :param feature: configuration feature
    :param args: optional additional argument to the feature such as a bgp neighbour
    :return: an equivalence class in the form of an integer
    """
    if args == -1:
        return -1

    def static_route(net, iface):
        for (n, i) in router.get_possible_args()[feature]:
            if n.address == net.address and n.prefix == net.prefix and i.name == iface:
                return coverage.get_index_from_args(router, feature, (n, i))
        return len(router.get_possible_args()[feature])

    def ospf_filter_list(prefix_list, dir):
        for pl in router.prefix_lists:
            if pl.name == prefix_list:
                return coverage.get_index_from_args(router, feature, (pl, dir))
        return len(router.get_possible_args()[feature])

    def ospf_area_range(net, adv, cost):
        for (n, a, c) in router.get_possible_args()[feature]:
            if n.address == net.address and n.prefix == net.prefix:
                return coverage.get_index_from_args(router, feature, (n, adv, cost))
        return len(router.get_possible_args()[feature])

    def check_resource(res, res_list):
        if res is None:
            return router.get_possible_args()[feature].index((res,))
        else:
            for r in res_list:
                if r.name == res:
                    return coverage.get_index_from_args(router, feature, (r,))
            return len(router.get_possible_args()[feature])

    def check_possible_args(arg):
        if arg in router.get_possible_args()[feature]:
            return coverage.get_index_from_args(router, feature, arg)
        return len(router.get_possible_args()[feature])

    def bgp_table_map(route_map):
        if route_map is None:
            return router.get_possible_args()[feature].index(route_map)
        else:
            for rm in router.bgp_in_route_maps:
                if rm.name == route_map.name:
                    return coverage.get_index_from_args(router, feature, (rm,))
            return len(router.get_possible_args()[feature])

    def match_community(comm, exact):
        for c in router.comm_lists:
            if c.name == comm:
                return coverage.get_index_from_args(router, feature, (c, exact))
        return len(router.get_possible_args()[feature])

    def bgp_aggregate_address(net, as_set, summary):
        for (n, a, s) in router.get_possible_args()[feature]:
            if n.address == net.address and n.prefix == net.prefix:
                return coverage.get_index_from_args(router, feature, (n, as_set, summary))
        return len(router.get_possible_args()[feature])

    def set_as_path(as_num):
        for (AS,) in router.get_possible_args()[feature]:
            if AS.num == as_num:
                return coverage.get_index_from_args(router, feature, (AS,))
        return len(router.get_possible_args()[feature])

    eq = {
        RouterFeatures.STATIC_ROUTE: static_route,

        OSPFFeatures.AREA_FILTER_LIST: ospf_filter_list,
        OSPFFeatures.AREA_RANGE: ospf_area_range,

        BGPFeatures.BGP_DAMPENING: lambda rm: check_resource(rm, router.bgp_in_route_maps),
        BGPFeatures.REDISTRIBUTE_CONNECTED: lambda rm: check_resource(rm, router.bgp_out_route_maps),
        BGPFeatures.REDISTRIBUTE_STATIC: lambda rm: check_resource(rm, router.bgp_out_route_maps),
        BGPFeatures.REDISTRIBUTE_OSPF: lambda rm: check_resource(rm, router.bgp_out_route_maps),
        BGPFeatures.TABLE_MAP: lambda s, rm: bgp_table_map(rm),
        BGPFeatures.AGGREGATE_ADDRESS: bgp_aggregate_address,
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN: lambda rm: check_resource(rm, router.bgp_in_route_maps),
        BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT: lambda rm: check_resource(rm, router.bgp_out_route_maps),
        BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE: lambda rm: check_resource(rm, router.bgp_out_route_maps),

        RouteMapFeatures.MATCH_INTERFACE: lambda iface: check_resource(iface, router.interfaces),
        RouteMapFeatures.MATCH_IP_PREFIX_LIST: lambda prefix_list: check_resource(prefix_list, router.prefix_lists),
        RouteMapFeatures.SET_INTERFACE: lambda iface: check_resource(iface, router.interfaces),
        RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP: lambda address: check_possible_args((address,)),
        RouteMapFeatures.SET_IP_NEXT_HOP: lambda address: check_possible_args((address,)),
        RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST: lambda as_path_list: check_resource(as_path_list,
                                                                                        router.as_path_lists),
        RouteMapFeatures.MATCH_COMMUNITY_LIST: lambda comm_list, exact: match_community(comm_list, exact),
        RouteMapFeatures.SET_AS_PATH_PREPEND: set_as_path,
        RouteMapFeatures.SET_COMM_LIST_DELETE: lambda comm_list: check_resource(comm_list, router.comm_lists),
        RouteMapFeatures.SET_COMMUNITY: lambda comm, add: check_possible_args((comm, add)),
        RouteMapFeatures.SET_ORIGIN: lambda origin: check_possible_args((origin,)),
    }

    return eq[feature](*args) if feature in eq else coverage.get_index_from_args(router, feature, args)