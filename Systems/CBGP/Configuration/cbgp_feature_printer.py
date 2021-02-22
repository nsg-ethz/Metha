import os

from Systems.CBGP.Configuration import cbgp_feature_args
from Systems.CBGP.Configuration.cbgp_config_features import *
from utils import *

feature_config = {
    GlobalFeatures.LOCAL_PREF: lambda pref: f'bgp options local-pref {pref}',
    GlobalFeatures.MED: lambda med: f'bgp options med {med}',

    RouterFeatures.NEXT_HOP: lambda router, neighbour, next_hop: f'bgp router {int_to_ip(router.router_id)} '
                                                                 f'peer {int_to_ip(neighbour.address)} '
                                                                 f'next-hop {int_to_ip(next_hop)}',
    RouterFeatures.NEXT_HOP_SELF: lambda router, neighbour: f'bgp router {int_to_ip(router.router_id)} '
                                                            f'peer {int_to_ip(neighbour.address)} next-hop-self',
    RouterFeatures.IGP_WEIGHT: lambda router, iface, cost: f'net node {int_to_ip(router.router_id)} '
                                                           f'iface {int_to_ip(iface.address)}/{iface.prefix}\n'
                                                           f' igp-weight {cost}\n exit',
    RouterFeatures.STATIC_ROUTE: lambda router, _, net, iface: f'net node {int_to_ip(router.router_id)} route add '
                                                               f'--oif={int_to_ip(iface.address)}/{iface.prefix}'
                                                               f' {int_to_ip(net.address)}/{net.prefix} 0',

    FilterFeatures.ACTION_ACCEPT: lambda: f'action "accept"',
    FilterFeatures.ACTION_DENY: lambda: f'action "deny"',
    FilterFeatures.ACTION_CALL: lambda rm: f'action "call {rm}"',
    FilterFeatures.ACTION_JUMP: lambda rm: f'action "jump {rm}"',
    FilterFeatures.ACTION_LOCAL_PREF: lambda pref: f'action "local-pref {pref}"',
    FilterFeatures.ACTION_METRIC: lambda metric: f'action "metric {metric}"',
    FilterFeatures.ACTION_METRIC_INTERNAL: lambda: f'action "metric internal"',
    FilterFeatures.ACTION_COMMUNITY_ADD: lambda comm: f'action "community add {comm}"',
    FilterFeatures.ACTION_COMMUNITY_STRIP: lambda: f'action "community strip"',
    FilterFeatures.ACTION_COMMUNITY_REMOVE: lambda comm: f'action "community remove {comm}"',
    FilterFeatures.ACTION_AS_PATH_PREPEND: lambda n: f'action "as-path prepend {n}"',
    FilterFeatures.ACTION_AS_PATH_REMOVE_PRIVATE: lambda: f'action "as-path remove-private"',
    FilterFeatures.ACTION_RED_COMMUNITY_ADD: lambda comm: f'action "red-community add {comm}"',
    FilterFeatures.MATCH_ANY: lambda: f'match "any"',
    FilterFeatures.MATCH_COMMUNITY: lambda comm: f'match "community is {comm}"',
    FilterFeatures.MATCH_NEXT_HOP: lambda next_hop: f'match "next-hop is {int_to_ip(next_hop)}"',
    FilterFeatures.MATCH_NEXT_HOP_IN: lambda next_hop: f'match "next-hop in {next_hop}"',
    FilterFeatures.MATCH_PREFIX: lambda prefix: f'match "prefix is {prefix}"',
    FilterFeatures.MATCH_PREFIX_IN: lambda prefix: f'match "prefix in {prefix}"',
    FilterFeatures.MATCH_PATH: lambda AS: f'match "path .*{AS.num}.*"',
    FilterFeatures.FILTER_MATCH_IN: lambda feature, *args: feature_config[feature](*args),
    FilterFeatures.FILTER_ACTION_IN: lambda feature, *args: feature_config[feature](*args),
    FilterFeatures.FILTER_MATCH_OUT: lambda feature, *args: feature_config[feature](*args),
    FilterFeatures.FILTER_ACTION_OUT: lambda feature, *args: feature_config[feature](*args)
}


def generate_feature_config(feature_list):
    config = []
    filters = {}

    for router, feature, arg in feature_list:
        if feature_list[router, feature, arg] == -1:
            continue

        args = cbgp_feature_args.get_possible_args(router)[feature][feature_list[router, feature, arg]]

        if feature in global_features:
            config.append(feature_config[feature](*args))
        elif feature in router_features:
            config.append(feature_config[feature](router, arg, *args))
        else:
            neighbour, direction, seq = arg
            if feature == FilterFeatures.FILTER_MATCH_IN or feature == FilterFeatures.FILTER_MATCH_OUT:
                filter_type = 'm'
            else:
                filter_type = 'a'
            if (router, neighbour, direction) not in filters:
                filters[router, neighbour, direction] = {}
            if seq not in filters[router, neighbour, direction]:
                filters[router, neighbour, direction][seq] = {}
            filters[router, neighbour, direction][seq][filter_type] = feature_config[feature](*args)

    for (router, neighbour, direction) in filters:
        config.append(
            f'bgp router {int_to_ip(router.router_id)} peer {int_to_ip(neighbour.address)} filter {direction}')
        for seq in sorted(filters[router, neighbour, direction]):
            config.append(' add-rule')
            if 'm' in filters[router, neighbour, direction][seq]:
                config.append(f'  {filters[router, neighbour, direction][seq]["m"]}')
            else:
                config.append(f'  match "any"')
            if 'a' in filters[router, neighbour, direction][seq]:
                config.append(f'  {filters[router, neighbour, direction][seq]["a"]}')
            else:
                config.append(f'  action "accept"')
            config.append('  exit')
        config.append(' exit')

    return '\n'.join(config)


def translate_topology(topology):
    config = []
    for router in topology.routers:
        config.append(f'net add node {int_to_ip(router.router_id)}\n')

    for i, j in topology.links:
        config.append(f'net add link-ptp {int_to_ip(topology.routers[i].router_id)} '
                      f'{int_to_ip(topology.links[i, j][0].address)}/{topology.links[i, j][0].prefix} '
                      f'{int_to_ip(topology.routers[j].router_id)} '
                      f'{int_to_ip(topology.links[i, j][1].address)}/{topology.links[i, j][1].prefix}\n')

    for AS in topology.ASes:
        config.append(f'net add domain {AS.num} igp\n')

    for router in topology.routers:
        config.append(f'net node {int_to_ip(router.router_id)} domain {router.AS.num}\n')

        for interface in router.interfaces:
            if interface.area is not None:
                config.append(f'net node {int_to_ip(router.router_id)} '
                              f'iface {int_to_ip(interface.address)}/{interface.prefix}\n'
                              f' igp-weight 1\n exit\n')

    for router in topology.routers:
        for neighbour in router.bgp_neighbours:
            if neighbour.AS != router.AS:
                config.append(f'net node {int_to_ip(router.router_id)} route add '
                              f'--oif={int_to_ip(neighbour.interface.address)}/{neighbour.interface.prefix} '
                              f'{int_to_ip(neighbour.address)}/32 0\n')

    for router in topology.routers:
        config.append(f'bgp add router {router.AS.num} {int_to_ip(router.router_id)}\n')

    for router in topology.routers:
        for neighbour in router.bgp_neighbours:
            config.append(f'bgp router {int_to_ip(router.router_id)}\n'
                          f' add peer {neighbour.AS} {int_to_ip(neighbour.address)}\n'
                          f' peer {int_to_ip(neighbour.address)} up\n'
                          f' exit\n')

    for router in topology.routers:
        for net in router.AS.networks:
            config.append(
                f'bgp router {int_to_ip(router.router_id)} add network {int_to_ip(net.address)}/{net.prefix}\n')

    return ''.join(config)


def generate_cbgp_config(path, topo, feature_list):
    config = [translate_topology(topo), generate_feature_config(feature_list)]

    for AS in topo.ASes:
        config.append(f'net domain {AS.num} compute')

    config.append('sim run\n')

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(f'{path}cbgp_config.txt', 'w') as f:
        f.write('\n'.join(config))
