from NetworkRepresentation.networks import select_network
from RouterConfiguration.Juniper import juniper_config_features, juniper_feature_selector, juniper_config_printer
from NetworkRepresentation.routers import *


class JuniperVMXRouter(Router):

    def __init__(self, name, router_id, topology, router_type, protocols=None):
        """

        :param name: Name of the router
        :param router_id: ID of the router, 32 bit integer corresponding to an IP address
        :param topology: Topology object to which this router belongs
        :param router_type: Type of the router / router image, enum from router_types.py
        :param protocols: List of protocols to be enabled on this router, if None, all protocols are enabled
        """
        super().__init__(name, router_id, topology, router_type, protocols)
        self.bgp_networks = False

        self.feature_list = juniper_config_features
        self.feature_args = juniper_feature_selector
        self.config_printer = juniper_config_printer
        self.suffix = 'set'

    def init_resources(self):
        """
        Initialize filters and list such as prefix lists and community lists
        """
        for i in range(3):

            comm = CommunityList(f'community_{i}')
            n = random.randint(1, 2)
            for j in range(n):
                string_comms = [f'{AS.num}:{c}' for (AS, c) in self.topology.communities] + ['no-advertise', 'no-export']
                c = random.choice([c for c in string_comms if c not in comm.comms])
                comm.comms.append(c)

            self.comm_lists.append(comm)

            pre = PrefixList(f'prefix_list_{i}')
            for j in range(3):
                seq = j + 1
                net = select_network(self.topology.network_list())
                pre.prefix[seq] = net

            self.prefix_lists.append(pre)

        for i in range(min(3, len(self.topology.ASes))):
            AS = self.topology.ASes[i]  # random.choice(self.topology.ASes)
            regex = f'.*{AS.num}.*'
            as_path_list = ASPathList(f'as_path_{i}', regex)

            self.as_path_lists.append(as_path_list)

        seq = 1
        rm = RouteMap('import-ospf')
        rm.perm[seq] = 'permit'
        self.ospf_in_route_maps.append(rm)
        rm = RouteMap('export-ospf')
        rm.perm[seq] = 'permit'
        self.ospf_out_route_maps.append(rm)
        rm = RouteMap('import-bgp')
        rm.perm[seq] = 'permit'
        self.bgp_in_route_maps.append(rm)
        rm = RouteMap('export-bgp')
        rm.perm[seq] = 'permit'
        self.bgp_out_route_maps.append(rm)

    def get_next_interface(self):
        """
        Returns the next available interface on this router
        :return: Interface object representing an available interface
        """
        adapter = len(self.interfaces) + 2
        port = 0
        name = f'ge-0/0/{adapter - 2}.0'
        interface = Interface(name, adapter, port)
        self.interfaces.append(interface)

        return interface
