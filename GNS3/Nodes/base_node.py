from netmiko import ConnectHandler

from GNS3 import send_request
from settings import GNS_SERVER_HOST


class GNS3Node:

    def __init__(self, node_id, port, name):
        self.node_id = node_id
        self.port = port
        self.name = name
        self.delay = 1
        self.command_max_loops = 500
        self.config_max_loops = 150

        self.netmiko_node = {
            'host': GNS_SERVER_HOST,
            'port': self.port,
            'global_delay_factor': self.delay,
            'timeout': 150
        }
        self.init_commands = []
        self.initial_config = None
        self.detailed_ospf = True

    def link_id(self):
        return self.node_id

    def init_router(self):
        telnet = ConnectHandler(**self.netmiko_node)

        telnet.enable()
        telnet.send_config_set(
            self.init_commands,
            cmd_verify=False,
            delay_factor=self.delay,
            max_loops=self.config_max_loops
        )
        telnet.disconnect()

    def start(self, pid):
        send_request('POST', f'/v2/projects/{pid}/nodes/{self.node_id}/start')

    def read_routing_table(self):
        raise NotImplementedError

    def clear_routing_table(self):
        pass

    def send_config(self, configs):
        raise NotImplementedError

    def send_config_from_file(self, path):
        raise NotImplementedError

    def write_config(self, path):
        raise NotImplementedError

    def parse_routing_table(self, srt, adj):
        raise NotImplementedError
