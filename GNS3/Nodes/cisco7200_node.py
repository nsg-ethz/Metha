import os
import json

from GNS3 import send_request, gns3_parser
from GNS3.Nodes.netmiko_node import NetmikoNode
from settings import GNS_ROUTER_PATH, GNS_METHA_SAME_SYSTEM


class Cisco7200Node(NetmikoNode):

    def __init__(self, name, gp, config=None):

        with open(f'{GNS_ROUTER_PATH}/cisco-7200.json') as f:
            router_conf = json.load(f)
        router_conf['name'] = name
        if config is not None and GNS_METHA_SAME_SYSTEM:
            router_conf['properties']['startup_config'] = os.path.abspath(config)
        param = json.dumps(router_conf)
        jdata = send_request('POST', f'/v2/projects/{gp.pid}/nodes', param, True)

        super().__init__(jdata['node_id'], jdata['console'], name, 'show run', 'show ip route', 'clear ip route *')

        if config is not None and not GNS_METHA_SAME_SYSTEM:
            self.initial_config = config

        self.init_commands = ['no logging console', 'no logging monitor']
        self.netmiko_node['device_type'] = 'cisco_ios_telnet'

    def parse_routing_table(self, srt, adj):
        return gns3_parser.textfsm_to_pd(srt, self.name, adj)
