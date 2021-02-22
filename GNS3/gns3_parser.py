import logging
import pprint

import pandas as pd


def junos_to_pd(srt, name, adj):
    """
    Parses Junos routing table received from the YAML format specified in gns3_interface.py
    :param srt: Source routing table in YAML format
    :param name: Name of the router
    :param adj: Adjacency information
    :return: Routing table as pandas dataframe
    """

    logger = logging.getLogger('network-testing')
    logger.debug(f'Parsing routing table {pprint.pformat(srt)}')

    rt = pd.DataFrame(
        columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol", "Metric",
                 "Admin_Distance", "Tag"])

    protocols = {
        'Local': 'local',
        'Direct': 'connected',
        'Static': 'static',
        'OSPF': 'ospf',
        'BGP': 'bgp'
    }

    default_dist = {
        'Direct': 0,
        'Static': 1,
        'OSPF': 110
    }

    for (address, properties) in srt:

        if address == '224.0.0.5/32':
            continue

        route = dict(properties)
        protocol = protocols[route['protocol']]
        next_hop = None
        interface = 'dynamic'
        next_ip = 'AUTO/NONE(-1l)' if not route['nexthop'] else route['nexthop']
        if route['via'] is None and route['nexthop'] is None:
            interface = 'null_interface'
            protocol = 'aggregate'
            next_ip = 'AUTO/NONE(-1l)'
        elif route['protocol'] == 'OSPF':
            if route['via'] in adj[name]:
                next_hop = adj[name][route['via']]
        elif route['protocol'] == 'BGP':
            if route['nexthop'] in adj[name]:
                next_hop = adj[name][route['nexthop']]
            elif route['nexthop'] in adj:
                next_hop = adj[route['nexthop']]
        elif route['protocol'] == 'Static' or route['protocol'] == 'Direct':
            interface = route['via']

        res = {
            'Node': name,
            'VRF': 'default',
            'Network': address,
            'Next_Hop': next_hop,
            'Next_Hop_IP': next_ip,
            'Next_Hop_Interface': interface,
            'Protocol': protocol,
            'Metric': int(route['metric']) if route['metric'] else 0,
            'Admin_Distance': int(route['preference']) if route['preference'] else default_dist[route['protocol']],
            'Tag': None
        }
        rt = rt.append(res, ignore_index=True)

    return rt


def textfsm_to_pd(srt, name, adj):
    """
    Parses routing table in textfsm format as returned by netmiko
    :param srt: Source routing table
    :param name: Name of the router
    :param adj: Adjacency information
    :return: Routing table as pandas dataframe
    """

    logger = logging.getLogger('network-testing')
    logger.debug(f'Parsing routing table {pprint.pformat(srt)}')

    rt = pd.DataFrame(
        columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol", "Metric",
                 "Admin_Distance", "Tag"])

    protocols = {
        'C': 'connected',
        'S': 'static',
        'O': 'ospf',
        'B': 'bgp',
        'R': 'rip',
        'D': 'eigrp',
        'i': 'isis'
    }

    default_dist = {
        'C': 0,
        'S': 1,
        'O': 110
    }

    for route in srt:
        protocol = protocols[route['protocol']] + route['type']
        next_hop = None
        interface = 'dynamic'
        next_ip = 'AUTO/NONE(-1l)' if not route['nexthop_ip'] else route['nexthop_ip']
        if route['nexthop_if'] == 'Null0':
            interface = 'null_interface'
            if route['protocol'] != 'S':
                protocol = 'aggregate'
            next_ip = 'AUTO/NONE(-1l)'
        elif route['protocol'] == 'O':
            next_hop = adj[name][route['nexthop_if']]
        elif route['protocol'] == 'B':
            if route['nexthop_ip'] in adj[name]:
                next_hop = adj[name][route['nexthop_ip']]
            elif route['nexthop_ip'] in adj:
                next_hop = adj[route['nexthop_ip']]
        elif route['protocol'] == 'S' or route['protocol'] == 'C':
            interface = route['nexthop_if']

        res = {
            'Node': name,
            'VRF': 'default',
            'Network': route['network'] + '/' + route['mask'],
            'Next_Hop': next_hop,
            'Next_Hop_IP': next_ip,
            'Next_Hop_Interface': interface,
            'Protocol': protocol,
            'Metric': int(route['metric']) if route['metric'] else 0,
            'Admin_Distance': int(route['distance']) if route['distance'] else default_dist[route['protocol']],
            'Tag': None
        }
        rt = rt.append(res, ignore_index=True)

    return rt
