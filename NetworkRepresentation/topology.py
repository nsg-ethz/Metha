import random
import os

from GNS3.router_types_config import metha_router
from NetworkRepresentation.networks import Network, select_network
from utils import *
from network_features import *


class AutonomousSystem:

    def __init__(self, num):
        self.num = num
        self.networks = []

    def __str__(self):
        return str(self.num)


class OSPFArea:

    def __init__(self, num):
        self.num = num
        self.networks = []
        if not num == 0:
            self.type = random.choices([OSPF_Area_Type.DEFAULT, OSPF_Area_Type.STUB, OSPF_Area_Type.NSSA])
        else:
            self.type = OSPF_Area_Type.DEFAULT

    def __str__(self):
        return str(self.num)


class BGPNeighbour:

    def __init__(self, address, AS, interface, group, router_id):
        self.address = address
        self.AS = AS
        self.interface = interface
        self.group = group
        self.router_id = router_id


class Topology:

    def __init__(self, num_nodes, num_ases, num_areas, links, ospf_areas, ases, router_types, protocols=None,
                 name='test-topology', init_resources=True):
        self.name = name
        self.routers = []
        self.ASes = []
        self.ospf_areas = []
        self.links = {}
        self.networks = {}
        self.communities = []
        if protocols is None:
            protocols = [None] * num_nodes

        for n in range(num_nodes):

            router = metha_router[router_types[n]]('Router' + str(n),
                                                   random.randint(0x80000000, 0xdfffffff),
                                                   self,
                                                   router_types[n],
                                                   protocols[n])
            self.routers.append(router)
            self.networks[router] = [Network(router.router_id, 32)]

        for l in links:
            i = l[0]
            j = l[1]

            self.routers[i].neighbours.append(self.routers[j])
            self.routers[j].neighbours.append(self.routers[i])

            mask = random.randint(16, 31)
            address = mask_address(random.randint(0x80000000, 0xdfffffff), mask)
            self.networks[self.routers[i]].append(Network(address, mask))
            self.networks[self.routers[i]].append(Network(address, mask))
            (ip1, ip2) = (address + 1, address + 2) if not mask == 31 else (address, address + 1)
            iface1 = self.routers[i].get_next_interface()
            iface2 = self.routers[j].get_next_interface()
            iface1.address = ip1
            iface1.prefix = mask
            iface2.address = ip2
            iface2.prefix = mask

            self.links[i, j] = (iface1, iface2)

        for a in range(num_ases):
            AS = AutonomousSystem(a + 1)
            self.ASes.append(AS)
            self.communities.append((AS, 100))

        for a in range(num_areas):
            self.ospf_areas.append(OSPFArea(a))

        for n in range(num_nodes):
            if ases[n] is not None:
                router = self.routers[n]
                router.AS = self.ASes[ases[n]]

        for k, l in enumerate(links):
            i = l[0]
            j = l[1]
            (iface1, iface2) = self.links[i, j]

            if ospf_areas[k] is not None:
                iface1.area = self.ospf_areas[ospf_areas[k]]
                iface2.area = self.ospf_areas[ospf_areas[k]]
                if self.ospf_areas[ospf_areas[k]] not in self.routers[i].ospf_areas:
                    self.routers[i].ospf_areas.append(self.ospf_areas[ospf_areas[k]])
                if self.ospf_areas[ospf_areas[k]] not in self.routers[j].ospf_areas:
                    self.routers[j].ospf_areas.append(self.ospf_areas[ospf_areas[k]])

            if self.routers[i].AS != self.routers[j].AS:
                self.routers[i].bgp_neighbours.append(
                    BGPNeighbour(iface2.address, self.routers[j].AS, iface1, 'EBGP', self.routers[j].router_id))
                self.routers[j].bgp_neighbours.append(
                    BGPNeighbour(iface1.address, self.routers[i].AS, iface2, 'EBGP', self.routers[i].router_id))
            else:
                self.routers[i].bgp_neighbours.append(
                    BGPNeighbour(self.routers[j].router_id, self.routers[j].AS, iface1, 'IBGP',
                                 self.routers[j].router_id))
                self.routers[j].bgp_neighbours.append(
                    BGPNeighbour(self.routers[i].router_id, self.routers[i].AS, iface2, 'IBGP',
                                 self.routers[i].router_id))

        for AS in self.ASes:
            num_networks = random.randint(0, 3)
            as_routers = [router for router in self.routers if router.AS == AS]
            if any(map(lambda router: router.bgp_networks, as_routers)):
                for i in range(0, num_networks):
                    as_nets = [net for router in self.routers if router.AS == AS for net in self.networks[router]]
                    network = select_network(as_nets)
                    AS.networks.append(network)

        for area in self.ospf_areas:
            num_networks = random.randint(0, 3)
            for i in range(0, num_networks):
                area_nets = [net for router in self.routers if area in router.ospf_areas for net in
                             self.networks[router]]
                network = select_network(area_nets)
                area.networks.append(network)

        if init_resources:
            for router in self.routers:
                if Protocols.BGP in router.enabled_protocols and router.enable_filters:
                    router.init_resources()

    def network_list(self):
        return [net for router in self.networks for net in self.networks[router]]

    def to_json(self, path):

        nodes = []
        links = []

        for router in self.routers:
            nodes.append({'name': router.name, 'router_type': router.router_type.name,
                          'config': f'{path}configs/{router.name}.{router.suffix}'})

        for (i, j) in self.links:
            (iface1, iface2) = self.links[i, j]
            node1 = {'name': self.routers[i].name, 'adapter': iface1.adapter, 'port': iface1.port}
            node2 = {'name': self.routers[j].name, 'adapter': iface2.adapter, 'port': iface2.port}
            links.append({'node1': node1, 'node2': node2})

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(f'{path}topology.json', 'w') as f:
            json.dump({'nodes': nodes, 'links': links}, f, indent=4, separators=(',', ': '))

    def get_adjacency_info(self):

        adj = {'router-ids': {}}

        for router in self.routers:
            adj[router.name] = {}
            adj[router.name]['interfaces'] = {}
            adj['router-ids'][router.name] = int_to_ip(router.router_id)

        for (i, j) in self.links:
            (iface1, iface2) = self.links[i, j]
            adj[self.routers[i].name][iface1.name] = self.routers[j].name
            adj[self.routers[i].name]['interfaces'][int_to_ip(iface1.address)] = iface1.name
            adj[self.routers[j].name][iface2.name] = self.routers[i].name
            adj[self.routers[j].name]['interfaces'][int_to_ip(iface2.address)] = iface2.name

        for router in self.routers:
            for neighbour in router.bgp_neighbours:
                adj[router.name][int_to_ip(neighbour.address)] = adj[router.name][neighbour.interface.name]
            adj[int_to_ip(router.router_id)] = router.name

        return adj
