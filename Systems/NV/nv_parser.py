import re
import os
import sys
import pprint
import pandas as pd

from utils import *

node_rt_regex = re.compile(r'^Node (?P<node_num>\d)\n---------\n\{ (?P<rt_entries>((\S+.*)\n?)*) \}',
                           re.MULTILINE)

option_regex = re.compile(r'None|Some\((?P<some>.+)\)')
typed_number_regex = re.compile(r'(?P<num>\d+)u\d+')
edge_regex = re.compile(r'(?P<node1>\d+)~(?P<node2>\d+)')
area_id_regex = re.compile(r'areaId=\s*(?P<area_id>\d+)u\d+')
area_type_regex = re.compile(r'areaType=\s*(?P<area_type>\d+)u\d+')
ospf_ad_regex = re.compile(r'ospfAd=\s*(?P<ospf_ad>\d+)u\d+')
weight_regex = re.compile(r'weight=\s*(?P<weight>\d+)u\d+')
ospf_next_hop_regex = re.compile(r'ospfNextHop=\s*None|Some\((?P<ospf_next_hop>\d+~\d+)\)')
bgp_ad_regex = re.compile(r'bgpAd=\s*(?P<bgp_ad>\d+)u\d+')
lp_regex = re.compile(r'lp=\s*(?P<lp>\d+)u\d+')
aslen_regex = re.compile(r'aslen=\s*(?P<aslen>\d+)u\d+')
med_regex = re.compile(r'med=\s*(?P<med>\d+)u\d+')
comms_regex = re.compile(r'comms=\s*(?P<comms>\{\s*(\d+u\d+\s+\|->\s+true\s*)*\s*\})')
bgp_next_hop_regex = re.compile(r'bgpNextHop=\s*None|Some\((?P<bgp_next_hop>\d+~\d+)\)')

rt_entry_regex = re.compile(
    r'^\((?P<address>\d+)u32,'
    r'(?P<prefix>\d+)u6\)'
    r'\s*\|->\s*'
    r'{\s*bgp= (?P<bgp>.+);\s*'
    r'connected= (?P<connected>\S+);\s*'
    r'ospf= (?P<ospf>.+);\s*'
    r'selected= (?P<selected>\S+);\s*'
    r'static= (?P<static>\S+);\s*}',
    re.MULTILINE
)

router_to_node_regex = re.compile(r'router(?P<router>\d+)=(?P<nv_node>\d+)')


def parse_edge(edge_str):
    node1 = int(edge_regex.search(edge_str).group('node1'))
    node2 = int(edge_regex.search(edge_str).group('node2'))

    return node1, node2


def parse_connected(connected_entry):
    opt = option_regex.search(connected_entry)
    if opt.group('some'):
        num = int(typed_number_regex.search(opt.group('some')).group('num'))
        return num
    else:
        return None


def parse_static(static_entry):
    opt = option_regex.search(static_entry)
    if opt.group('some'):
        num = int(typed_number_regex.search(opt.group('some')).group('num'))
        return num
    else:
        return None


def parse_ospf(ospf_entry):
    opt = option_regex.search(ospf_entry)
    if opt.group('some'):
        ospf_str = opt.group('some')
        area_id = int(area_id_regex.search(ospf_str).group('area_id'))
        area_type = int(area_type_regex.search(ospf_str).group('area_type'))
        ospf_ad = int(ospf_ad_regex.search(ospf_str).group('ospf_ad'))
        weight = int(weight_regex.search(ospf_str).group('weight'))
        if ospf_next_hop_regex.search(ospf_str).group('ospf_next_hop'):
            ospf_next_hop = parse_edge(ospf_next_hop_regex.search(ospf_str).group('ospf_next_hop'))
        else:
            ospf_next_hop = None
        return {'area_id': area_id, 'area_type': area_type, 'ospf_ad': ospf_ad, 'weight': weight,
                'ospf_next_hop': ospf_next_hop}
    else:
        return None


def parse_bgp(bgp_entry):
    opt = option_regex.search(bgp_entry)
    if opt.group('some'):
        bgp_str = opt.group('some')
        bgp_ad = int(bgp_ad_regex.search(bgp_str).group('bgp_ad'))
        aslen = int(aslen_regex.search(bgp_str).group('aslen'))
        med = int(med_regex.search(bgp_str).group('med'))
        comms = comms_regex.search(bgp_str).group('comms')
        if bgp_next_hop_regex.search(bgp_str).group('bgp_next_hop'):
            bgp_next_hop = parse_edge(bgp_next_hop_regex.search(bgp_str).group('bgp_next_hop'))
        else:
            bgp_next_hop = None
        return {'bgp_ad': bgp_ad, 'aslen': aslen, 'med': med, 'comms': comms, 'bgp_next_hop': bgp_next_hop}
    else:
        return None


def parse_selected(selected_entry):
    opt = option_regex.search(selected_entry)
    if opt.group('some'):
        return int(typed_number_regex.search(opt.group('some')).group('num'))
    else:
        return None


def parse_results(nv_output):
    routing_tables = {}

    for rt in node_rt_regex.finditer(nv_output):
        node = int(rt.group('node_num'))
        routing_tables[node] = []

        for entry in rt_entry_regex.finditer(rt.group('rt_entries')):
            rt_entry = {
                'address': int(entry.group('address')),
                'prefix': int(entry.group('prefix')),
                'bgp': parse_bgp(entry.group('bgp')),
                'connected': parse_connected(entry.group('connected')),
                'ospf': parse_ospf(entry.group('ospf')),
                'static': parse_static(entry.group('static')),
                'selected': parse_selected(entry.group('selected'))
            }

            routing_tables[node].append(rt_entry)

    return routing_tables


def router_to_nv_node_conversion(nv_control):

    conv = {}

    for entry in router_to_node_regex.finditer(nv_control):
        router = int(entry.group('router'))
        node = int(entry.group('nv_node'))

        conv[node] = router

    return conv


def build_rt(srt, conv, adj):
    rt = pd.DataFrame(
        columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol", "Metric",
                 "Admin_Distance", "Tag"])

    for node in srt:
        router = f'Router{conv[node]}'

        for entry in srt[node]:

            next_interface = 'dynamic'
            next_ip = 'AUTO/NONE(-1l)'

            if entry['selected'] == 0:
                protocol = 'connected'
                metric = 0
                ad = entry['connected']
                next_hop = None
            elif entry['selected'] == 1:
                protocol = 'static'
                metric = 0
                ad = entry['static']
                next_hop = None
            elif entry['selected'] == 2:
                protocol = 'ospf'
                metric = entry['ospf']['weight']
                ad = entry['ospf']['ospf_ad']
                next_hop = entry['ospf']['ospf_next_hop'][1] if entry['ospf']['ospf_next_hop'] is not None else None
            elif entry['selected'] == 3:
                protocol = 'bgp'
                metric = entry['bgp']['med']
                ad = entry['bgp']['bgp_ad']
                next_hop = entry['bgp']['bgp_next_hop'][1] if entry['bgp']['bgp_next_hop'] is not None else None
            else:
                raise Exception('Invalid selected protocol in nv table')

            next_hop = f'Router{conv[next_hop]}' if next_hop is not None else None

            res = {
                'Node': router,
                'VRF': 'default',
                'Network': int_to_ip(entry['address']) + '/' + str(entry['prefix']),
                'Next_Hop': next_hop,
                'Next_Hop_IP': next_ip,
                'Next_Hop_Interface': next_interface,
                'Protocol': protocol,
                'Metric': metric,
                'Admin_Distance': ad,
                'Tag': None
            }
            rt = rt.append(res, ignore_index=True)

    return rt


if __name__ == '__main__':
    path = os.path.abspath(sys.argv[1])

    with open(path) as f:
        pprint.pprint(parse_results(f.read()))
