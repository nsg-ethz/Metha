import os

from GNS3.ConfigParsers import cisco_ios, juniper_junos
from GNS3.Nodes.cisco7200_node import Cisco7200Node
from GNS3.Nodes.junipervmx_node import JuniperVMXNode
from GNS3.router_types import RouterTypes
from NetworkRepresentation.Cisco7200 import Cisco7200Router
from NetworkRepresentation.JuniperVMX import JuniperVMXRouter

config_extensions = ['.cfg', '.set']


def get_config_type(file):
    extensions = {
        '.cfg': RouterTypes.Cisco7200,
        '.set': RouterTypes.JuniperVMX
    }

    name, ext = os.path.splitext(file)
    return extensions[ext]


interface_name = {
    RouterTypes.Cisco7200: lambda adapter, port: f'FastEthernet{adapter}/{port}',
    RouterTypes.JuniperVMX: lambda adapter, port: f'ge-0/0/{adapter - 2}.{port}'
}

get_interfaces = {
    RouterTypes.Cisco7200: cisco_ios.get_interfaces,
    RouterTypes.JuniperVMX: juniper_junos.get_interfaces
}

get_hostname = {
    RouterTypes.Cisco7200: cisco_ios.get_hostname,
    RouterTypes.JuniperVMX: juniper_junos.get_hostname
}

get_router_id = {
    RouterTypes.Cisco7200: cisco_ios.get_router_id,
    RouterTypes.JuniperVMX: juniper_junos.get_router_id
}

node_types = {
    RouterTypes.Cisco7200: Cisco7200Node,
    RouterTypes.JuniperVMX: JuniperVMXNode
}

adapter_offset = {
    RouterTypes.Cisco7200: 0,
    RouterTypes.JuniperVMX: 2
}

metha_router = {
    RouterTypes.Cisco7200: Cisco7200Router,
    RouterTypes.JuniperVMX: JuniperVMXRouter
}
