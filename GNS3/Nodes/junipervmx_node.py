import json

from GNS3 import send_request, gns3_parser
from GNS3.Nodes.pyez_node import PyEZNode
from settings import GNS_ROUTER_PATH


class JuniperVMXNode(PyEZNode):

    def __init__(self, name, gp, config=None):

        with open(f'{GNS_ROUTER_PATH}/juniper-vmx-vcp.json') as f:
            router_conf = json.load(f)
        router_conf['name'] = f'{name}-vcp'
        param = json.dumps(router_conf)
        jdata_vcp = send_request('POST', f'/v2/projects/{gp.pid}/nodes', param, True)

        with open(f'{GNS_ROUTER_PATH}/juniper-vmx-vfp.json') as f:
            router_conf = json.load(f)
        router_conf['name'] = f'{name}-vfp'
        param = json.dumps(router_conf)
        jdata_vfp = send_request('POST', f'/v2/projects/{gp.pid}/nodes', param, True)
        gp.link_nodes((jdata_vfp['node_id'], 1, 0), (jdata_vcp['node_id'], 1, 0))
        gp.sleep_time = 220

        super().__init__(jdata_vcp['node_id'], jdata_vcp['console'], name, config)
        self.vcp_id = jdata_vcp['node_id']
        self.vfp_id = jdata_vfp['node_id']
        self.delay = 4
        self.netmiko_node['global_delay_factor'] = self.delay
        self.netmiko_node['timeout'] = 300

    def link_id(self):
        return self.vfp_id

    def start(self, pid):
        send_request('POST', f'/v2/projects/{pid}/nodes/{self.vcp_id}/start')
        send_request('POST', f'/v2/projects/{pid}/nodes/{self.vfp_id}/start')

    def parse_routing_table(self, srt, adj):
        return gns3_parser.junos_to_pd(srt, self.name, adj)
