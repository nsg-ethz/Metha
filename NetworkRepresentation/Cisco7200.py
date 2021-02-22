from NetworkRepresentation.networks import select_network
from RouterConfiguration.Cisco import cisco_config_features, cisco_feature_selector, cisco_config_printer
from NetworkRepresentation.routers import *


class Cisco7200Router(Router):

    def __init__(self, name, router_id, topology, router_type, protocols=None):
        """

        :param name: Name of the router
        :param router_id: ID of the router, 32 bit integer corresponding to an IP address
        :param topology: Topology object to which this router belongs
        :param router_type: Type of the router / router image, enum from router_types.py
        :param protocols: List of protocols to be enabled on this router, if None, all protocols are enabled
        """

        super().__init__(name, router_id, topology, router_type, protocols)

        self.feature_list = cisco_config_features
        self.config_printer = cisco_config_printer
        self.feature_args = cisco_feature_selector
        self.suffix = 'cfg'

    def init_resources(self):
        """
        Initialize filters and list such as prefix lists and community lists
        """

        for i in range(3):

            perm = random.choice([' permit ', ' deny '])
            comm = CommunityList(i + 1, perm)
            n = random.randint(1, 2)
            for j in range(n):
                string_comms = [f'{AS.num}:{c}' for (AS, c) in self.topology.communities]
                c = random.choice(string_comms + ['internet', 'local-as', 'no-advertise', 'no-export'])
                comm.comms.append(c)

            self.comm_lists.append(comm)

            pre = PrefixList(f'prefix_list_{i}')
            for j in range(3):
                seq = j + 1
                perm = random.choice([' permit ', ' deny '])
                pre.perm[seq] = perm
                net = select_network(self.topology.network_list())
                pre.prefix[seq] = net
                val = random.randint(net.prefix, 32)
                pre.eq[seq] = random.choice([' le ' + str(val), ' ge ' + str(val), '',
                                             ' ge ' + str(val) + ' le ' + str(random.randint(val, 32))])

            self.prefix_lists.append(pre)

        for i in range(min(3, len(self.topology.ASes))):
            perm = ' permit '  # random.choice([' permit ', ' deny '])
            AS = self.topology.ASes[i]  # random.choice(self.topology.ASes)
            regex = f'_{AS.num}_'
            as_path_list = ASPathList(i + 1, regex, perm)

            self.as_path_lists.append(as_path_list)

        for f in self.feature_list.match_features_in:
            rm = RouteMap(f'map_in_{str.lower(f.name)}')
            seq = 1
            rm.perm[seq] = ' permit '  # random.choice([' permit ', ' deny '])
            rm.fixed_match_features[seq] = f
            self.bgp_in_route_maps.append(rm)

        for f in self.feature_list.match_features_out:
            rm = RouteMap(f'map_out_{str.lower(f.name)}')
            seq = 1
            rm.perm[seq] = ' permit '  # random.choice([' permit ', ' deny '])
            rm.fixed_match_features[seq] = f
            self.bgp_out_route_maps.append(rm)

    def get_next_interface(self):
        """
        Get the next available interface on this router
        :return: Interface object representing the next available interface on this router
        """
        adapter = len(self.interfaces) // 2
        port = len(self.interfaces) % 2
        name = f'FastEthernet{adapter}/{port}'
        interface = Interface(name, adapter, port)
        self.interfaces.append(interface)

        return interface
