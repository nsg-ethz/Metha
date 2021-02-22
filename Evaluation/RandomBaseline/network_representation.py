import random
import os

from utils import *
from network_features import *
from NetworkRepresentation import topology, routers
from NetworkRepresentation.Cisco7200 import Cisco7200Router
from NetworkRepresentation.topology import Topology


def get_random_network():
    """
    Generate a random network
    :return: Network object with a random address as well as prefix
    """
    prefix = random.randint(0, 32)
    address = random.randint(0x80000000, 0xdfffffff)
    return topology.Network(mask_address(address, prefix), prefix)


class RandomRouter(Cisco7200Router):

    """
    Special router class which ignores semantic constraints on resources such as prefix lists, and instead generates
    them at random
    """

    def __init__(self, name, router_id, topo, router_type, protocols=None):
        super().__init__(name, router_id, topo, router_type, protocols)

    def init_resources(self):
        """
        Initiate resources without any measure to ensure that for example prefix lists reference IPs which are used
        somewhere in the network
        """
        for i in random.sample(range(1, 200), 3):

            perm = random.choice([' permit ', ' deny '])
            comm = routers.CommunityList(i, perm)
            n = random.randint(1, 3)
            for j in range(n):
                c = random.choice([f'{random.randint(1, 65535)}:{random.randint(1, 65535)}',
                                   'internet', 'local-as', 'no-advertise', 'no-export'])
                comm.comms.append(c)

            self.comm_lists.append(comm)

        for i in random.sample(range(0, 200), 3):
            pre = routers.PrefixList(f'prefix_list_{i}')
            for j in range(3):
                seq = j + 1
                perm = random.choice([' permit ', ' deny '])
                pre.perm[seq] = perm
                net = get_random_network()
                pre.prefix[seq] = net
                val = random.randint(net.prefix, 32)
                pre.eq[seq] = random.choice([' le ' + str(val), ' ge ' + str(val), '',
                                             ' ge ' + str(val) + ' le ' + str(random.randint(val, 32))])

            self.prefix_lists.append(pre)

        for i in random.sample(range(1, 200), 3):
            perm = random.choice([' permit ', ' deny '])
            regex = f'_{random.randint(1, 65535)}_'
            as_path_list = routers.ASPathList(i, regex, perm)

            self.as_path_lists.append(as_path_list)

        for i in random.sample(range(0, 200), 3):
            rm = routers.RouteMap(f'map_in_{i}')
            for j in range(3):
                seq = j + 1
                rm.perm[seq] = ' permit '
                rm.fixed_match_features[seq] = random.choice(self.feature_list.match_features_in)
                self.bgp_in_route_maps.append(rm)

        for i in random.sample(range(0, 200), 3):
            rm = routers.RouteMap(f'map_out_{i}')
            for j in range(3):
                seq = j + 1
                rm.perm[seq] = ' permit '
                rm.fixed_match_features[seq] = random.choice(self.feature_list.match_features_out)
                self.bgp_out_route_maps.append(rm)

    def get_possible_args(self, allowed_features=None):

        return {}

    def get_random_args(self, allowed_features=None):

        return {}


class RandomTopology(Topology):

    """
    Topology which ensures no semantic consistency on the network, instead things like interface IPs, OSPF areas, and
    BGP ASes are assigned at random
    """

    def __init__(self, num_nodes, links, router_types, name='random-topology'):
        """
        Initialize a random topology with the given physical layout
        :param num_nodes: Number of nodes in the topology
        :param links: Links between the nodes as list of pairs
        :param router_types: Router type for each node in the topology
        :param name: Optional name for the topology
        """
        super().__init__(0, num_ases=0, num_areas=0, links=[], ospf_areas=[], ases=[], router_types=[], name=name)
        self.routers = []
        self.ASes = [topology.AutonomousSystem(i) for i in random.sample(range(1, 65536), num_nodes)]
        self.ospf_areas = [topology.OSPFArea(i) for i in random.sample(range(0, 0xffffffff), len(links))]
        self.links = {}

        for n in range(num_nodes):
            router = RandomRouter('Router' + str(n),
                                  random.randint(0x80000000, 0xdfffffff),
                                  self,
                                  router_types[n])
            self.routers.append(router)
            router.AS = random.choice(self.ASes + [None])
            if router.AS is None and Protocols.BGP in router.enabled_protocols:
                router.enabled_protocols.remove(Protocols.BGP)

        for l in links:
            i = l[0]
            j = l[1]

            self.routers[i].neighbours.append(self.routers[j])
            self.routers[j].neighbours.append(self.routers[i])

            iface1 = self.routers[i].get_next_interface()
            iface2 = self.routers[j].get_next_interface()
            iface1.prefix = random.randint(0, 31)
            iface1.address = mask_address(random.randint(0x80000000, 0xdfffffff), iface1.prefix)
            iface1.area = random.choice(self.ospf_areas + [None])
            iface2.prefix = random.randint(0, 31)
            iface2.address = mask_address(random.randint(0x80000000, 0xdfffffff), iface2.prefix)
            iface2.area = random.choice(self.ospf_areas + [None])

            self.links[i, j] = (iface1, iface2)
            k = random.randint(0, 1)

            if k == 0:
                self.routers[i].bgp_neighbours.append(
                    topology.BGPNeighbour(
                        random.randint(0x80000000, 0xdfffffff),
                        random.choice(self.ASes),
                        iface1,
                        'BGP',
                        random.randint(0x80000000, 0xdfffffff)
                    ))
                self.routers[j].bgp_neighbours.append(
                    topology.BGPNeighbour(
                        random.randint(0x80000000, 0xdfffffff),
                        random.choice(self.ASes),
                        iface2,
                        'BGP',
                        random.randint(0x80000000, 0xdfffffff)
                    ))

        for AS in self.ASes:
            num_networks = random.randint(0, 3)
            for i in range(0, num_networks):
                network = get_random_network()
                AS.networks.append(network)

        for area in self.ospf_areas:
            num_networks = random.randint(0, 3)
            for i in range(0, num_networks):
                network = get_random_network()
                area.networks.append(network)

        for router in self.routers:
            if Protocols.BGP in router.enabled_protocols and router.enable_filters:
                router.init_resources()

    def to_batfish_json(self, path):
        """
        Generates a Batfish layer 1 topology JSON file corresponding to this topology. This is necessary since without
        guaranteed matching IPs at interfaces Batfish is unable to infer the topology layout from config files.
        :param path: Path where the topology file will be saved
        """
        edges = []

        for (i, j) in self.links:
            (iface1, iface2) = self.links[i, j]
            node1 = {'hostname': self.routers[i].name, 'interfaceName': iface1.name}
            node2 = {'hostname': self.routers[j].name, 'interfaceName': iface2.name}
            edges.append({'node1': node1, 'node2': node2})

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f'{path}layer1_topology.json', 'w') as f:
            json.dump({'edges': edges}, f, indent=4, separators=(',', ': '))


