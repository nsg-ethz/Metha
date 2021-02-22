import re
import pandas as pd
import logging
import pprint

route_regex = re.compile(r'^(?P<prefix>\S*)\t(?P<gateway>\S*)\t(?P<out_iface>\S*)\t(?P<metric>\S*)\t(?P<type>\S*)',
                         re.MULTILINE)

protocol_translate = {
    'IGP': 'ospf',
    'BGP': 'bgp',
    'STATIC': 'static'
}


def parse_cbgp(srt, name, adj=None):
    """
    Parse the routing table received from C-BGP
    :param srt: Source routing table
    :param name: Name of the router
    :param adj: Adjacency information
    :return: Routing table as pandas dataframe
    """
    logger = logging.getLogger('network-testing')
    logger.info(f'Parsing routing table {pprint.pformat(srt)}')

    rt = pd.DataFrame(
        columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol", "Metric",
                 "Admin_Distance", "Tag"])

    for entry in route_regex.finditer(srt):
        network = entry.group('prefix')
        next_hop = None
        next_ip = 'AUTO/NONE(-1l)'
        next_if = 'dynamic'
        protocol = protocol_translate[entry.group('type')]
        if entry.group('gateway') == '0.0.0.0':
            if protocol == 'static':
                next_if = adj[name]['interfaces'][entry.group('out_iface')]
            else:
                next_ip = entry.group('out_iface')
                iface = adj[name]['interfaces'][next_ip]
                next_hop = adj[name][iface]
        else:
            next_ip = entry.group('gateway')
            if next_ip in adj[name]:
                next_hop = adj[name][next_ip]
            elif next_ip in adj:
                next_hop = adj[next_ip]
        metric = int(entry.group('metric'))
        res = {
            'Node': name,
            'VRF': 'default',
            'Network': network,
            'Next_Hop': next_hop,
            'Next_Hop_IP': next_ip,
            'Next_Hop_Interface': next_if,
            'Protocol': protocol,
            'Metric': metric,
            'Admin_Distance': 0,
            'Tag': None
        }

        rt = rt.append(res, ignore_index=True)

    return rt
