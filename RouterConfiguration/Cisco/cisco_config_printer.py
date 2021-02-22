import os

from RouterConfiguration.Cisco.cisco_config_features import *
from utils import *
from network_features import *


def route_map_deny(rm, seq):
    rm.perm[seq] = 'deny'
    return f'{rm} {rm.perm[seq]} {seq}'


def route_map_permit(rm, seq):
    rm.perm[seq] = 'permit'
    return f'{rm} {rm.perm[seq]} {seq}'


feature_config = {
    RouterFeatures.STATIC_ROUTE: lambda network, interface: f'ip route {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)} {interface}',

    OSPFFeatures.INTERFACE_OSPF_COST: lambda interface, cost: f' ip ospf cost {cost}',
    OSPFFeatures.INTERFACE_OSPF_PRIORITY: lambda interface, priority: f' ip ospf priority {priority}',
    OSPFFeatures.AUTO_COST: lambda bandwidth: f' auto-cost reference-bandwidth {bandwidth}',
    OSPFFeatures.NO_COMPATIBLE_RFC1583: lambda: ' no compatible rfc1583',
    OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE: lambda always, metric, metric_type: f' default-information originate {always}{metric}{metric_type}',
    OSPFFeatures.DEFAULT_METRIC: lambda metric: f' default-metric {metric}',
    OSPFFeatures.DISTANCE: lambda dist: f' distance {dist}',
    OSPFFeatures.REDISTRIBUTE_CONNECTED: lambda subnets: f' redistribute connected {subnets}',
    OSPFFeatures.REDISTRIBUTE_STATIC: lambda subnets: f' redistribute static {subnets}',
    OSPFFeatures.REDISTRIBUTE_BGP: lambda asn, subnets: f' redistribute bgp {asn}{subnets}',
    OSPFFeatures.MAX_METRIC: lambda external, stub, summary: f' max-metric router-lsa {external}{stub}{summary}',
    OSPFFeatures.AREA_FILTER_LIST: lambda area, filter_list, dir: f' area {area} filter-list prefix {filter_list}{dir}',
    OSPFFeatures.AREA_RANGE: lambda area, network, advertise, cost: f' area {area} range {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)}{advertise}{cost}',
    OSPFFeatures.NSSA_STUB_DEFAULT_COST: lambda area, cost: f' area {area} default-cost {cost}',
    OSPFFeatures.NSSA_NO_REDISTRIBUTION: lambda area: f' area {area} nssa no-redistribution',
    OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE: lambda area, metric, metric_type: f' area {area} nssa default-information-originate{metric}{metric_type}',
    OSPFFeatures.NSSA_NO_SUMMARY: lambda area: f' area {area} nssa no-summary',
    OSPFFeatures.NSSA_ONLY: lambda area: f' area {area} nssa nssa-only',
    OSPFFeatures.STUB_NO_SUMMARY: lambda area: f' area {area} stub no-summary',

    BGPFeatures.ALWAYS_COMPARE_MED: lambda: ' bgp always-compare-med',
    BGPFeatures.BESTPATH_COMPARE_ROUTERID: lambda: ' bgp bestpath compare-routerid',
    BGPFeatures.BESTPATH_MED_CONFED: lambda missing_as_worst: f' bgp bestpath med confed {missing_as_worst}',
    BGPFeatures.BESTPATH_MED_MISSING: lambda: ' bgp bestpath med missing-as-worst',
    BGPFeatures.NO_CLIENT_TO_CLIENT_REFLECTION: lambda: ' no bgp client-to-client reflection',
    BGPFeatures.DEFAULT_LOCAL_PREFERENCE: lambda preference: f' bgp default local-preference {preference}',
    BGPFeatures.DETERMINISTIC_MED: lambda: ' bgp deterministic-med',
    BGPFeatures.MAXAS_LIMIT: lambda limit: f' bgp maxas-limit {limit}',
    BGPFeatures.DEFAULT_INFORMATION_ORIGINATE: lambda: ' default-information originate',
    BGPFeatures.ADDITIONAL_PATHS_INSTALL: lambda: ' bgp additional-paths install',
    BGPFeatures.AUTO_SUMMARY: lambda: ' auto-summary',
    BGPFeatures.BGP_DAMPENING: lambda route_map: f' bgp dampening {route_map or ""}',
    BGPFeatures.DISTANCE_BGP: lambda external, internal, local: f' distance bgp {external} {internal} {local}',
    BGPFeatures.REDISTRIBUTE_CONNECTED: lambda route_map: f' redistribute connected {route_map or ""}',
    BGPFeatures.REDISTRIBUTE_STATIC: lambda route_map: f' redistribute static {route_map or ""}',
    BGPFeatures.REDISTRIBUTE_OSPF: lambda route_map: f' redistribute ospf {route_map or ""}',
    BGPFeatures.SYNCHRONIZATION: lambda: ' synchronization',
    BGPFeatures.TABLE_MAP: lambda use_filter, route_map: f' table-map {route_map.name}{use_filter}',
    BGPFeatures.AGGREGATE_ADDRESS: lambda network, as_set, summary: f' aggregate-address {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)}{as_set}{summary}',
    BGPFeatures.ADDITIONAL_PATHS: lambda options: f' bgp additional-paths {options}',
    BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX: lambda neighbour, max_prefix: f' neighbor {int_to_ip(neighbour)} maximum-prefix {max_prefix}',
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN: lambda neighbour, route_map: f' neighbor {int_to_ip(neighbour)}{route_map} in',
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT: lambda neighbour, route_map: f' neighbor {int_to_ip(neighbour)}{route_map} out',
    BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF: lambda neighbour: f' neighbor {int_to_ip(neighbour)} next-hop-self',
    BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST: lambda neighbour, options: f' neighbor {int_to_ip(neighbour)} capability orf prefix-list {options}',
    BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE: lambda neighbour, route_map: f' neighbor {int_to_ip(neighbour)} default-originate {route_map or ""}',
    BGPFeatures.NEIGHBOUR_ROUTE_REFLECTOR_CLIENT: lambda neighbour: f' neighbor {int_to_ip(neighbour)} route-reflector-client',
    BGPFeatures.NEIGHBOUR_WEIGHT: lambda neighbour, weight: f' neighbor {int_to_ip(neighbour)} weight {weight}',

    RouteMapFeatures.MATCH_INTERFACE: lambda rm, seq, interface: f' match interface {interface}',
    RouteMapFeatures.MATCH_IP_PREFIX_LIST: lambda rm, seq, prefix_list: f' match ip address prefix-list {prefix_list}',
    RouteMapFeatures.MATCH_IP_NEXT_HOP: lambda rm, seq, access_list: f' match ip next-hop {access_list}',
    RouteMapFeatures.SET_INTERFACE: lambda rm, seq, interface: f' set interface {interface}',
    RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP: lambda rm, seq, ip: f' set ip default next-hop {int_to_ip(ip)}',
    RouteMapFeatures.SET_IP_NEXT_HOP: lambda rm, seq, ip: f' set ip next-hop {int_to_ip(ip)}',
    RouteMapFeatures.SET_METRIC: lambda rm, seq, metric: f' set metric {metric}',
    RouteMapFeatures.CONTINUE: lambda rm, seq: f' continue',
    RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST: lambda rm, seq, as_path: f' match as-path {as_path}',
    RouteMapFeatures.MATCH_COMMUNITY_LIST: lambda rm, seq, community, exact: f' match community {community} {exact}',
    RouteMapFeatures.SET_LOCAL_PREFERENCE: lambda rm, seq, preference: f' set local-preference {preference}',
    RouteMapFeatures.SET_AS_PATH_PREPEND: lambda rm, seq, AS: f' set as-path prepend {AS}',
    RouteMapFeatures.SET_COMM_LIST_DELETE: lambda rm, seq, community: f' set comm-list {community} delete',
    RouteMapFeatures.SET_COMMUNITY: lambda rm, seq, community, additive: f' set community {community} {additive}',
    RouteMapFeatures.SET_ORIGIN: lambda rm, seq, origin: f' set origin {origin}',
    RouteMapFeatures.SET_WEIGHT: lambda rm, seq, weight: f' set weight {weight}',
    RouteMapFeatures.SET_METRIC_TYPE_INTERNAL: lambda rm, seq: f' set metric-type internal',
    RouteMapFeatures.MATCH_FEATURE_BGP_OUT: lambda rm, seq, feature, *args: feature_config[feature](rm, seq, *args),
    RouteMapFeatures.MATCH_FEATURE_BGP_IN: lambda rm, seq, feature, *args: feature_config[feature](rm, seq, *args),
    RouteMapFeatures.SET_FEATURE_BGP_OUT: lambda rm, seq, feature, *args: feature_config[feature](rm, seq, *args),
    RouteMapFeatures.SET_FEATURE_BGP_IN: lambda rm, seq, feature, *args: feature_config[feature](rm, seq, *args),
    RouteMapFeatures.ROUTE_MAP_DENY: lambda rm, seq: route_map_deny(rm, seq),
}

feature_disable = {
    RouterFeatures.STATIC_ROUTE: lambda network, interface: f'no ip route {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)} {interface}',

    OSPFFeatures.INTERFACE_OSPF_COST: lambda interface, cost: f'no ip ospf cost',
    OSPFFeatures.INTERFACE_OSPF_PRIORITY: lambda interface, priority: f'no ip ospf priority',
    OSPFFeatures.AUTO_COST: lambda bandwidth: f'no auto-cost reference-bandwidth {bandwidth}',
    OSPFFeatures.NO_COMPATIBLE_RFC1583: lambda: 'compatible rfc1583',
    OSPFFeatures.DEFAULT_INFORMATION_ORIGINATE: lambda always, metric, metric_type: f'no default-information originate',
    OSPFFeatures.DEFAULT_METRIC: lambda metric: f'no default-metric {metric}',
    OSPFFeatures.DISTANCE: lambda dist: f'no distance {dist}',
    OSPFFeatures.REDISTRIBUTE_CONNECTED: lambda subnets: f'no redistribute connected',
    OSPFFeatures.REDISTRIBUTE_STATIC: lambda subnets: f'no redistribute static',
    OSPFFeatures.REDISTRIBUTE_BGP: lambda asn, subnets: f'no redistribute bgp {asn}',
    OSPFFeatures.MAX_METRIC: lambda external, stub, summary: f'no max-metric router-lsa',
    OSPFFeatures.AREA_FILTER_LIST: lambda area, filter_list, dir: f'no area {area} filter-list prefix {filter_list}{dir}',
    OSPFFeatures.AREA_RANGE: lambda area, network, advertise, cost: f'no area {area} range {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)}',
    OSPFFeatures.NSSA_STUB_DEFAULT_COST: lambda area, cost: f'no area {area} default-cost',
    OSPFFeatures.NSSA_NO_REDISTRIBUTION: lambda area: f'no area {area} nssa no-redistribution',
    OSPFFeatures.NSSA_DEFAULT_INFORMATION_ORIGINATE: lambda area, metric, metric_type: f'no area {area} nssa default-information-originate',
    OSPFFeatures.NSSA_NO_SUMMARY: lambda area: f'no area {area} nssa no-summary',
    OSPFFeatures.NSSA_ONLY: lambda area: f'no area {area} nssa nssa-only',
    OSPFFeatures.STUB_NO_SUMMARY: lambda area: f'no area {area} stub no-summary',

    BGPFeatures.ALWAYS_COMPARE_MED: lambda: 'no bgp always-compare-med',
    BGPFeatures.BESTPATH_COMPARE_ROUTERID: lambda: 'no bgp bestpath compare-routerid',
    BGPFeatures.BESTPATH_MED_CONFED: lambda missing_as_worst: f'no bgp bestpath med confed {missing_as_worst}\n',
    BGPFeatures.BESTPATH_MED_MISSING: lambda: 'no bgp bestpath med missing-as-worst',
    BGPFeatures.NO_CLIENT_TO_CLIENT_REFLECTION: lambda: ' bgp client-to-client reflection',
    BGPFeatures.DEFAULT_LOCAL_PREFERENCE: lambda preference: f'no bgp default local-preference',
    BGPFeatures.DETERMINISTIC_MED: lambda: 'no bgp deterministic-med',
    BGPFeatures.MAXAS_LIMIT: lambda limit: f'no bgp maxas-limit',
    BGPFeatures.DEFAULT_INFORMATION_ORIGINATE: lambda: 'no default-information originate',
    BGPFeatures.ADDITIONAL_PATHS_INSTALL: lambda: 'no bgp additional-paths install',
    BGPFeatures.AUTO_SUMMARY: lambda: 'no auto-summary',
    BGPFeatures.BGP_DAMPENING: lambda route_map: f'no bgp dampening',
    BGPFeatures.DISTANCE_BGP: lambda external, internal, local: f'no distance bgp',
    BGPFeatures.REDISTRIBUTE_CONNECTED: lambda route_map: f'no redistribute connected',
    BGPFeatures.REDISTRIBUTE_STATIC: lambda route_map: f'no redistribute static',
    BGPFeatures.REDISTRIBUTE_OSPF: lambda route_map: f'no redistribute ospf',
    BGPFeatures.SYNCHRONIZATION: lambda: 'no synchronization',
    BGPFeatures.TABLE_MAP: lambda use_filter, route_map: f'no table-map',
    BGPFeatures.AGGREGATE_ADDRESS: lambda network, as_set, summary: f'no aggregate-address {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)}',
    BGPFeatures.ADDITIONAL_PATHS: lambda options: f'no bgp additional-paths',
    BGPFeatures.NEIGHBOUR_MAXIMUM_PREFIX: lambda neighbour, max_prefix: f'no neighbor {int_to_ip(neighbour)} maximum-prefix {max_prefix}',
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_IN: lambda neighbour, route_map: f'no neighbor {int_to_ip(neighbour)}{route_map} in',
    BGPFeatures.NEIGHBOUR_ROUTE_MAP_OUT: lambda neighbour, route_map: f'no neighbor {int_to_ip(neighbour)}{route_map} out',
    BGPFeatures.NEIGHBOUR_NEXT_HOP_SELF: lambda neighbour: f'no neighbor {int_to_ip(neighbour)} next-hop-self',
    BGPFeatures.NEIGHBOUR_CAPABILITY_ORF_PREFIX_LIST: lambda neighbour, options: f'no neighbor {int_to_ip(neighbour)} capability orf prefix-list {options}',
    BGPFeatures.NEIGHBOUR_DEFAULT_ORIGINATE: lambda neighbour, route_map: f'no neighbor {int_to_ip(neighbour)} default-originate',
    BGPFeatures.NEIGHBOUR_ROUTE_REFLECTOR_CLIENT: lambda neighbour: f'no neighbor {int_to_ip(neighbour)} route-reflector-client',
    BGPFeatures.NEIGHBOUR_WEIGHT: lambda neighbour, weight: f'no neighbor {int_to_ip(neighbour)} weight',

    RouteMapFeatures.MATCH_INTERFACE: lambda rm, seq, interface: f'no match interface {interface}',
    RouteMapFeatures.MATCH_IP_PREFIX_LIST: lambda rm, seq, prefix_list: f'no match ip address prefix-list {prefix_list}',
    RouteMapFeatures.MATCH_IP_NEXT_HOP: lambda rm, seq, access_list: f'no match ip next-hop {access_list}',
    RouteMapFeatures.SET_INTERFACE: lambda rm, seq, interface: f'no set interface {interface}',
    RouteMapFeatures.SET_IP_DEFAULT_NEXT_HOP: lambda rm, seq, ip: f'no set ip default next-hop {int_to_ip(ip)}',
    RouteMapFeatures.SET_IP_NEXT_HOP: lambda rm, seq, ip: f'no set ip next-hop {int_to_ip(ip)}',
    RouteMapFeatures.SET_METRIC: lambda rm, seq, metric: f'no set metric {metric}',
    RouteMapFeatures.MATCH_AS_PATH_ACCESS_LIST: lambda rm, seq, as_path: f'no match as-path {as_path}',
    RouteMapFeatures.MATCH_COMMUNITY_LIST: lambda rm, seq, community, exact: f'no match community {community}',
    RouteMapFeatures.SET_LOCAL_PREFERENCE: lambda rm, seq, preference: f'no set local-preference {preference}',
    RouteMapFeatures.SET_AS_PATH_PREPEND: lambda rm, seq, AS: f'no set as-path prepend {AS}',
    RouteMapFeatures.SET_COMM_LIST_DELETE: lambda rm, seq, community: f'no set comm-list {community} delete',
    RouteMapFeatures.SET_COMMUNITY: lambda rm, seq, community, additive: f'no set community {community}{additive}',
    RouteMapFeatures.SET_ORIGIN: lambda rm, seq, origin: f'no set origin {origin}',
    RouteMapFeatures.SET_WEIGHT: lambda rm, seq, weight: f'no set weight {weight}',
    RouteMapFeatures.SET_METRIC_TYPE_INTERNAL: lambda rm, seq: f'no set metric-type internal',
    RouteMapFeatures.MATCH_FEATURE_BGP_OUT: lambda rm, seq, feature, *args: feature_disable[feature](rm, seq, *args),
    RouteMapFeatures.MATCH_FEATURE_BGP_IN: lambda rm, seq, feature, *args: feature_disable[feature](rm, seq, *args),
    RouteMapFeatures.SET_FEATURE_BGP_OUT: lambda rm, seq, feature, *args: feature_disable[feature](rm, seq, *args),
    RouteMapFeatures.SET_FEATURE_BGP_IN: lambda rm, seq, feature, *args: feature_disable[feature](rm, seq, *args),
    RouteMapFeatures.ROUTE_MAP_DENY: lambda rm, seq: route_map_permit(rm, seq),
}

filter_config = [RouteMapFeatures.ROUTE_MAP_DENY]
bgp_af_features = [BGPFeatures.ADDITIONAL_PATHS]


def config_mode(router, feature, arg):

    mode = {
        RouterFeatures: lambda router: (),
        OSPFFeatures: lambda router: (f'router ospf {router.ospf_proc}',),
        BGPFeatures: lambda router: (f'router bgp {router.AS}',)
    }

    if feature in interface_features:
        return f'interface {arg.name}',
    elif feature in filter_config:
        return ()
    elif feature in bgp_af_features:
        return f'router bgp {router.AS}', f'address-family ipv4'
    elif type(feature) == RouteMapFeatures:
        rm, seq = arg
        return f'{rm} {rm.perm[seq]} {seq}',
    else:
        return mode[type(feature)](router)


def exit_config_mode(feature):

    mode = {
        RouterFeatures: [],
        OSPFFeatures: [f'exit'],
        BGPFeatures: [f'exit'],
        RouteMapFeatures: [f'exit']
    }

    if feature in filter_config:
        return []
    elif feature in bgp_af_features:
        return [f'exit-address-family', f'exit']
    else:
        return mode[type(feature)]


def generate_maps_lists_config(router):
    config = []

    for route_map in router.bgp_in_route_maps:
        for seq in route_map.perm:
            config.append(f'{route_map} {route_map.perm[seq]} {seq}')

            if seq in route_map.match_features:
                feature, *args = route_map.match_features[seq]
                config.append(feature_config[feature](route_map, seq, *args))

            if seq in route_map.set_features:
                feature, *args = route_map.set_features[seq]
                config.append(feature_config[feature](route_map, seq, *args))

    for route_map in router.bgp_out_route_maps:
        for seq in route_map.perm:
            config.append(f'{route_map} {route_map.perm[seq]} {seq}')

            if seq in route_map.match_features:
                feature, *args = route_map.match_features[seq]
                config.append(feature_config[feature](route_map, seq, *args))

            if seq in route_map.set_features:
                feature, *args = route_map.set_features[seq]
                config.append(feature_config[feature](route_map, seq, *args))

    for prefix_list in router.prefix_lists:
        for seq in prefix_list.perm:
            config.append(f'ip prefix-list {prefix_list} seq {seq} {prefix_list.perm[seq]} '
                          f'{int_to_ip(prefix_list.prefix[seq].address)}/'
                          f'{prefix_list.prefix[seq].prefix}{prefix_list.eq[seq]}')

    for comm_list in router.comm_lists:
        comms = ' '.join(comm_list.comms)
        config.append(f'ip community-list {comm_list.name} {comm_list.perm} {comms}')

    for as_path_list in router.as_path_lists:
        config.append(f'ip as-path access-list {as_path_list.name} {as_path_list.perm} {as_path_list.regex}')

    for access_list in router.access_lists:
        config.append(f'access-list {access_list.num} {access_list.perm} {int_to_ip(access_list.net.address)} {int_to_lower_mask(access_list.net.prefix)}')

    return config


def generate_ospf_config(router):
    config = ['router ospf ' + str(router.ospf_proc), f' router-id {int_to_ip(router.router_id)}']

    for area in router.ospf_areas:

        for net in area.networks:
            config.append(f' network {int_to_ip(net.address)} {int_to_lower_mask(net.prefix)} area {area}')

        if area.type == OSPF_Area_Type.NSSA:
            config.append(' area ' + str(area) + ' nssa')
        elif area.type == OSPF_Area_Type.STUB:
            config.append(' area ' + str(area) + ' stub')

    return config


def generate_bgp_config(router):
    config = [f'router bgp {router.AS.num}', f' bgp router-id {int_to_ip(router.router_id)}']

    for neighbour in router.bgp_neighbours:
        config.append(f' neighbor {int_to_ip(neighbour.address)} remote-as {neighbour.AS.num}')
        config.append(f' neighbor {int_to_ip(neighbour.address)} update-source {neighbour.interface.name}')
        config.append(f' neighbor {int_to_ip(neighbour.address)} advertisement-interval 0')

    config.append(' address-family ipv4')
    for net in router.AS.networks:
        config.append(f'  network {int_to_ip(net.address)} mask {int_to_upper_mask(net.prefix)}')

    for neighbour in router.bgp_neighbours:
        config.append(f'  neighbor {int_to_ip(neighbour.address)} activate')

    config.append(' exit-address-family')

    return config


def get_base_config(router):

    config = [f'hostname {router.name}', 'interface loopback 0',
              f' ip address {int_to_ip(router.router_id)} {int_to_upper_mask(32)}']

    for interface in router.interfaces:
        if interface.address is not None:
            config.append(f'interface {interface.name}')
            config.append(' ip address ' + int_to_ip(interface.address) + ' ' + int_to_upper_mask(interface.prefix))
            if interface.area is not None:
                config.append(f' ip ospf {router.ospf_proc} area {interface.area}')

    for network, interface in router.fixed_static_routes:
        config.append(f'ip route {int_to_ip(network.address)} {int_to_upper_mask(network.prefix)} {interface.name}')

    if Protocols.OSPF in router.enabled_protocols or Protocols.BGP in router.enabled_protocols:
        config.extend(generate_ospf_config(router))
    if Protocols.BGP in router.enabled_protocols:
        config.extend(generate_bgp_config(router))
        config.extend(generate_maps_lists_config(router))

    return config


def write_config(router, path):
    config = get_base_config(router)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(f'{path}{router.name}.cfg', 'w') as f:
        f.write('\n'.join(config))
