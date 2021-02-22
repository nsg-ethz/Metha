import logging
import os
import pprint

import yaml
from jnpr.junos import Device
from jnpr.junos.factory import FactoryLoader
from jnpr.junos.utils.config import Config
from lxml import etree

from GNS3.Nodes.base_node import GNS3Node
from settings import GNS_SERVER_HOST

logger = logging.getLogger('network-testing')

rt_yml = """
RouteTable2:
  rpc: get-route-information
  args_key: destination
  item: route-table/rt 
  key: rt-destination
  view: RouteTableView

RouteTableView:
  groups:
    entry: rt-entry
  fields_entry:
    # fields taken from the group 'entry'
    protocol: protocol-name
    via: nh/via | nh/nh-local-interface
    age: { age/@seconds : int }
    nexthop: nh/to
    preference: preference
    metric: metric | med
"""

globals().update(FactoryLoader().load(yaml.load(rt_yml, Loader=yaml.FullLoader)))


class PyEZNode(GNS3Node):

    def __init__(self, node_id, port, name, config=None):

        super().__init__(node_id, port, name)
        self.pyez_connection = None
        self.initial_config = os.path.abspath(config)
        self.detailed_ospf = False

        self.netmiko_node['device_type'] = 'juniper_junos_telnet'
        self.netmiko_node['username'] = 'root'
        self.netmiko_node['password'] = 'rootPW'
        self.netmiko_node['default_enter'] = '\r\n'

        self.pyez_node = {
            'host': GNS_SERVER_HOST,
            'mode': 'telnet',
            'port': self.port,
            'user': 'root',
            'password': 'rootPW'
        }

        self.init_commands = [
            f'delete chassis auto-image-upgrade',
            f'set system root-authentication encrypted-password "$6$5e4bMlUm$PbzLjZviqrGsMEXwmt.URYuW/O6Cy4leZ.c31f2/AIxVuAP1FbuycJJuRq7vCKhO5lURlWPOyXLL91ZX0n2B7."',
            f'set system host-name {self.name}',
            f'commit'
        ]

    def __del__(self):
        if self.pyez_connection is not None:
            self.pyez_connection.close()

    def init_router(self):
        super().init_router()
        self.pyez_connection = Device(**self.pyez_node).open()

        if self.initial_config is not None:
            self.send_config_from_file(self.initial_config)

    def read_routing_table(self):
        routes = RouteTable2(self.pyez_connection)
        routes.get(table='inet.0')

        return routes.items()

    def send_config(self, configs):

        logger.debug(f'Send config {pprint.pformat(configs)} to router {self.name}')

        with Config(self.pyez_connection) as cu:
            cu.load('\n'.join(configs), format='set')
            cu.commit()

    def send_config_from_file(self, path):

        with open(path) as f:
            with Config(self.pyez_connection) as cu:
                cu.load(f.read(), format='set')
                cu.commit()

    # def clear_routing_table(self):
        # return self.pyez_connection.rpc.clear_ospf_database_information()

    def write_config(self, path):
        config = self.pyez_connection.rpc.get_config(options={'format': 'set'})
        config = etree.tostring(config, encoding='unicode', pretty_print=True)

        config = '\n'.join(config.splitlines()[1:-1])

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f'{path}{self.name}.set', 'w') as f:
            f.write(config)
