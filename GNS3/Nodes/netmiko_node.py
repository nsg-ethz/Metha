import logging
import os

from netmiko import NetmikoTimeoutException, ConnectHandler

from GNS3.Nodes.base_node import GNS3Node

logger = logging.getLogger('network-testing')


class NetmikoNode(GNS3Node):

    def __init__(self, node_id, port, name, read_config, read_routes, clear_routes):
        super().__init__(node_id, port, name)
        self.port = port
        self.name = name
        self.telnet_connection = None
        self.delay = 1
        self.command_max_loops = 500
        self.config_max_loops = 150
        self.read_config = read_config
        self.read_routes = read_routes
        self.clear_routes = clear_routes

    def __del__(self):
        if self.telnet_connection is not None:
            self.telnet_connection.disconnect()

    def init_router(self):
        super().init_router()
        self.telnet_connection = ConnectHandler(**self.netmiko_node)
        self.telnet_connection.enable()

        if self.initial_config is not None:
            self.send_config_from_file(self.initial_config)

    def read_routing_table(self):
        try:
            return self.telnet_connection.send_command(
                self.read_routes,
                use_textfsm=True,
                delay_factor=self.delay,
                max_loops=self.command_max_loops
            )
        except NetmikoTimeoutException:
            self.command_max_loops += 50
            logger.info(f'Retry reading routing table with {self.command_max_loops} max loops')
            self.telnet_connection.disconnect()
            self.telnet_connection = ConnectHandler(**self.netmiko_node)
            return self.read_routing_table()

    def clear_routing_table(self):
        try:
            return self.telnet_connection.send_command(
                self.clear_routes,
                delay_factor=self.delay,
                max_loops=self.command_max_loops
            )
        except NetmikoTimeoutException:
            self.command_max_loops += 50
            logger.info(f'Retry clearing routing table with {self.command_max_loops} max loops')
            self.telnet_connection.disconnect()
            self.telnet_connection = ConnectHandler(**self.netmiko_node)
            return self.clear_routing_table()

    def send_config(self, configs):
        try:
            return self.telnet_connection.send_config_set(
                configs,
                cmd_verify=False,
                delay_factor=self.delay,
                max_loops=self.config_max_loops
            )
        except NetmikoTimeoutException:
            self.config_max_loops += 50
            logger.info(f'Retry configuration with {self.config_max_loops} max loops')
            self.telnet_connection.disconnect()
            self.telnet_connection = ConnectHandler(**self.netmiko_node)
            return self.send_config(configs)

    def send_config_from_file(self, path):
        try:
            return self.telnet_connection.send_config_from_file(
                path,
                cmd_verify=False,
                delay_factor=self.delay,
                max_loops=self.config_max_loops
            )
        except NetmikoTimeoutException:
            self.config_max_loops += 50
            logger.info(f'Retry configuration with {self.config_max_loops} max loops')
            self.telnet_connection.disconnect()
            self.telnet_connection = ConnectHandler(**self.netmiko_node)
            return self.send_config_from_file(path)

    def write_config(self, path):
        try:
            config = self.telnet_connection.send_command(
                self.read_config,
                delay_factor=self.delay,
                max_loops=self.command_max_loops
            )

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(f'{path}{self.name}.cfg', 'w') as f:
                f.write(config)
        except NetmikoTimeoutException:
            self.command_max_loops += 50
            logger.info(f'Retry writing config with {self.command_max_loops} max loops')
            self.telnet_connection.disconnect()
            self.telnet_connection = ConnectHandler(**self.netmiko_node)
            self.write_config(path)
