import glob
import http.client
import logging
import time
import concurrent.futures
import pandas as pd

from GNS3.router_types import *
from GNS3 import send_request
from GNS3.router_types_config import interface_name, get_interfaces, get_router_id, adapter_offset, \
    get_hostname, get_config_type, config_extensions, node_types
from settings import GNS_SERVER_HOST, GNS_SERVER_PORT, GNS_NUM_UNCHANGED, GNS_SLEEP_TIME
from utils import *

logger = logging.getLogger('network-testing')
counter = 0


def get_routing_tables(nodes):
    """
    Reads the routing tables of GNS3 nodes
    :param nodes: List of GNS3 nodes for which to read the routing table
    :return: Dictionary of routing tables indexed by node name
    """
    routes = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_node = {
            executor.submit(nodes[node].read_routing_table): node for node in nodes
        }
        for future in concurrent.futures.as_completed(future_to_node):
            node = future_to_node[future]
            table = future.result(timeout=10)
            routes[node] = table

        executor.shutdown(wait=True)

    return routes


class GNS3Project:
    def __init__(self, name):
        """
        Creates a new GNS3 project and initializes it
        :param name: Name of the project
        """
        conn = http.client.HTTPConnection(GNS_SERVER_HOST, GNS_SERVER_PORT)
        param = json.dumps({"name": name})
        conn.request('GET', '/v2/projects')
        r = conn.getresponse()
        data = r.read()
        jdata = json.loads(data)
        for entry in jdata:
            if entry['name'] == name:
                conn.request('DELETE', f"/v2/projects/{entry['project_id']}")
                conn.getresponse()
        conn.request("POST", "/v2/projects", param)
        r = conn.getresponse()
        data = r.read()
        jdata = json.loads(data)
        self.pid = jdata['project_id']
        conn.close()
        self.nodes = {}
        self.sleep_time = 20

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    def __del__(self):
        self.delete()

    def delete(self):
        """
        Deletes the GNS3 project from the server, including any local files
        :return: HTTP status of the request
        """
        return send_request('DELETE', f'/v2/projects/{self.pid}')

    def create_node(self, name, router_type, config=None):
        """
        Creates a new GNS3 node and initializes it
        :param name: Name of the node
        :param router_type: Router type of the node, indicates the router image used
        :param config: Optional initial config for the router
        :return: Node object representing the newly created node
        """
        node = node_types[router_type](name, self, config)
        self.nodes[node.name] = node
        return node

    def link_nodes(self, link1, link2):
        """
        Links two GNS3 nodes
        :param link1: Triplet of node id, adapter, and port specifying the first node for the link
        :param link2: Triplet of node id, adapter, and port specifying the second node for the link
        :return: HTTP request status
        """
        nid1, adapter1, port1 = link1
        nid2, adapter2, port2 = link2
        param = json.dumps({'nodes': [{'adapter_number': adapter1, 'node_id': nid1, 'port_number': port1},
                                      {'adapter_number': adapter2, 'node_id': nid2, 'port_number': port2}]})
        return send_request('POST', f'/v2/projects/{self.pid}/links', param)

    def start_nodes(self):
        """
        Start all nodes of this project
        """
        for node in self.nodes:
            self.nodes[node].start(self.pid)

        time.sleep(self.sleep_time)

        for node in self.nodes:
            self.nodes[node].init_router()

    def generate_routing_table(self, adj):
        """
        Continually read the routing tables of all nodes in this project until convergence
        :param adj: Adjacency information
        :return: Final dict of routing table dataframes, indexed by node name
        """
        routes = []

        for i in range(GNS_NUM_UNCHANGED):
            routes.append(pd.DataFrame(
                columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol",
                         "Metric",
                         "Admin_Distance", "Tag"]))

        for i in range(GNS_NUM_UNCHANGED):
            route = get_routing_tables(self.nodes)
            for node in self.nodes:
                routes[i] = routes[i].append(self.nodes[node].parse_routing_table(route[node], adj),
                                             ignore_index=True)
            time.sleep(GNS_SLEEP_TIME)

        conv_counter = 0

        while not all(r.equals(routes[0]) for r in routes) and conv_counter < 100:
            routes[:-1] = routes[1:]
            routes[-1] = pd.DataFrame(
                columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol",
                         "Metric",
                         "Admin_Distance", "Tag"])
            route = get_routing_tables(self.nodes)
            for node in self.nodes:
                routes[-1] = routes[-1].append(self.nodes[node].parse_routing_table(route[node], adj),
                                               ignore_index=True)
            time.sleep(GNS_SLEEP_TIME)
            conv_counter = conv_counter + 1

        logger.info(f'Converged after reading {conv_counter} additional times')

        return routes[-1]


def generate_topology(path):
    """
    Generates the GNS3 topology file for a given set of configs
    :param path: path where the config files are located, configs are searched for in the folder path/configs/
    """
    configs = [f for ext in config_extensions for f in glob.glob(f'{path}configs/*{ext}')]

    configured_interfaces = {}
    nodes = []
    links = []

    for cpath in configs:
        router_type = get_config_type(cpath)

        with open(cpath) as f:
            config = f.read()
            name = get_hostname[router_type](config)
            nodes.append({'name': name, 'router_type': router_type.name, 'config': cpath})

            for address, mask, adapter, port in get_interfaces[router_type](config):

                address_split = address.split('.')
                mask_split = mask.split('.')

                ma1 = int(address_split[0]) & int(mask_split[0])
                ma2 = int(address_split[1]) & int(mask_split[1])
                ma3 = int(address_split[2]) & int(mask_split[2])
                ma4 = int(address_split[3]) & int(mask_split[3])

                masked_address = str(ma1) + '.' + str(ma2) + '.' + str(ma3) + '.' + str(ma4)

                interface = {
                    'name': name,
                    'adapter': adapter + adapter_offset[router_type],
                    'port': port
                }

                if masked_address in configured_interfaces:
                    links.append({'node1': configured_interfaces[masked_address], 'node2': interface})
                else:
                    configured_interfaces[masked_address] = interface

    with open(path + 'topology.json', 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f, indent=4, separators=(',', ': '))


def build_adjacency_info(topo_file):
    """
    Builds adjacency information from a given topology file as well as associated router configs
    :param topo_file: GNS3 topology file
    :return: Adjacency information
    """
    adj = {'router-ids': {}}
    rtypes = {}
    interfaces = {}

    with open(topo_file) as f:
        topo = json.load(f)
        for node in topo['nodes']:
            router_type = router_type_from_string(node['router_type'])
            rtypes[node['name']] = router_type
            with open(node['config']) as conf_f:
                config = conf_f.read()
                router_id = get_router_id[router_type](config)
                adj[router_id] = node['name']
                adj[node['name']] = {}
                adj[node['name']]['interfaces'] = {}
                adj['router-ids'][node['name']] = router_id

                for address, mask, adapter, port in get_interfaces[router_type](config):
                    i_name = interface_name[router_type](adapter + adapter_offset[router_type], port)
                    adj[node['name']]['interfaces'][address] = i_name
                    interfaces[node['name'], i_name] = address

        for link in topo['links']:
            node1 = link['node1']['name']
            node2 = link['node2']['name']
            rtype1 = rtypes[node1]
            rtype2 = rtypes[node2]
            iface1 = interface_name[rtype1](link['node1']['adapter'], link['node1']['port'])
            iface2 = interface_name[rtype2](link['node2']['adapter'], link['node2']['port'])
            adj[node1][iface1] = node2
            adj[node2][iface2] = node1
            adj[node1][interfaces[node2, iface2]] = node2
            adj[node2][interfaces[node1, iface1]] = node1

    return adj


def setup_gns_from_topology(file_path):
    """
    Set up a GNS3 project from a given GNS3 topology file
    :param file_path: location of the topology file
    :return: GNS3 project descriptor
    """
    global counter

    gp = GNS3Project("fuzzer" + str(counter))
    counter = counter + 1
    nodes = {}

    with open(file_path) as f:
        topo = json.load(f)
        for node in topo['nodes']:
            router_type = router_type_from_string(node['router_type'])
            nodes[node['name']] = gp.create_node(node['name'], router_type, node['config'])
        for link in topo['links']:
            node1 = nodes[link['node1']['name']]
            node2 = nodes[link['node2']['name']]
            link1 = node1.link_id(), link['node1']['adapter'], link['node1']['port']
            link2 = node2.link_id(), link['node2']['adapter'], link['node2']['port']

            gp.link_nodes(link1, link2)
        return gp


def init_gns_from_files(path):
    """
    Run GNS3 from a given set of router configs, builds GNS3 topology as well as adjacency information and
    starts all routers in the GNS3 project
    :param path: path to the configuration files, router configs are located at path/configs/
    :return: GNS3 project descriptor and corresponding adjacency information
    """
    generate_topology(path)
    gp = setup_gns_from_topology(f'{path}topology.json')
    adj = build_adjacency_info(f'{path}topology.json')
    gp.start_nodes()

    return gp, adj

