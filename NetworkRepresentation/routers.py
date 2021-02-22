import itertools
import random

from GNS3.router_types import RouterTypes
from NetworkRepresentation.networks import Network
from network_features import Protocols, OSPF_Area_Type
from utils import mask_address, filter_optional


class Interface:

    def __init__(self, name, adapter, port):
        """

        :param name: Name of the interface
        :param adapter: Physical adapter number of the interface
        :param port: Physical port number of the interface
        """
        self.name = name
        self.adapter = adapter
        self.port = port
        self.address = None
        self.prefix = None
        self.area = None

    def __str__(self):
        return self.name


class Router:

    def __init__(self, name, router_id, topology, router_type, protocols=None):
        """

        :param name: Name of the router
        :param router_id: ID of the router, 32 bit integer corresponding to an IP address
        :param topology: Topology object to which this router belongs
        :param router_type: Type of the router / router image, enum from router_types.py
        :param protocols: List of protocols to be enabled on this router, if None, all protocols are enabled
        """
        self.name = name
        self.topology = topology
        self.ospf_areas = []
        self.AS = None
        self.interfaces = []
        self.router_id = router_id
        self.neighbours = []
        self.bgp_neighbours = []
        self.ospf_proc = 100
        self.ospf_in_route_maps = []
        self.ospf_out_route_maps = []
        self.bgp_in_route_maps = []
        self.bgp_out_route_maps = []
        self.prefix_lists = []
        self.comm_lists = []
        self.as_path_lists = []
        self.access_lists = []

        if protocols is None:
            self.enabled_protocols = list(Protocols)
        else:
            self.enabled_protocols = protocols

        self.enable_filters = True

        self.map_counter = 0
        self.prefix_counter = 0

        self.features = {}

        self.enabled_features = {}
        self.config_remove = []

        self.router_type = router_type
        self.static_routes = []
        for i in range(3):
            mask = random.randint(16, 31)
            address = mask_address(random.randint(0x80000000, 0xdfffffff), mask)
            self.static_routes.append(Network(address, mask))

        self.fixed_static_routes = []
        self.bgp_networks = True

        self.feature_list = None
        self.feature_args = None
        self.config_printer = None
        self.unsupported_features = []

    def __str__(self):
        return self.name

    def init_resources(self):
        """
        Initialize filters and list such as prefix lists and community lists
        """
        raise NotImplementedError

    def get_next_interface(self):
        """
        Return the next available interface on this router
        """
        raise NotImplementedError

    def get_supported_features(self, allowed_features=None):
        """
        Get all router feature triplets which are supported by this router
        :param allowed_features: Optional parameter, restricts the router feature triplets to only use configuration
        features which are in allowed_features
        :return: list of valid router feature triplets
        """
        disabled_features = self.unsupported_features

        if Protocols.STATIC not in self.enabled_protocols:
            disabled_features.extend(self.feature_list.static_features)
        if Protocols.OSPF not in self.enabled_protocols:
            disabled_features.extend(self.feature_list.ospf_features)
        if Protocols.BGP not in self.enabled_protocols:
            disabled_features.extend(self.feature_list.bgp_features)
        if not self.enable_filters:
            disabled_features.extend(self.feature_list.filter_req_features)

        if allowed_features is not None:
            allowed_features = [f for f in allowed_features if f not in disabled_features]
        elif disabled_features:
            allowed_features = [f for f in self.feature_list.all_features if f not in disabled_features]

        supported_router_features = filter_optional(self.feature_list.router_features, allowed_features)
        supported_interface_features = filter_optional(self.feature_list.interface_features, allowed_features)
        supported_ospf_area_features = filter_optional(self.feature_list.area_features, allowed_features)
        supported_ospf_nssa_features = filter_optional(self.feature_list.nssa_features, allowed_features)
        supported_ospf_stub_features = filter_optional(self.feature_list.stub_features, allowed_features)
        supported_bgp_neighbour_features = filter_optional(self.feature_list.neighbour_features, allowed_features)
        supported_filter_ospf_in_features = filter_optional(self.feature_list.filter_ospf_in_features, allowed_features)
        supported_filter_ospf_out_features = filter_optional(self.feature_list.filter_ospf_out_features, allowed_features)
        supported_filter_bgp_in_features = filter_optional(self.feature_list.filter_bgp_in_features, allowed_features)
        supported_filter_bgp_out_features = filter_optional(self.feature_list.filter_bgp_out_features, allowed_features)

        if Protocols.OSPF not in self.enabled_protocols:
            supported_filter_ospf_in_features = []
            supported_filter_ospf_out_features = []
        if Protocols.BGP not in self.enabled_protocols:
            supported_filter_bgp_in_features = []
            supported_filter_bgp_out_features = []

        nssa_areas = [a for a in self.ospf_areas if a.type == OSPF_Area_Type.NSSA]
        stub_areas = [a for a in self.ospf_areas if a.type == OSPF_Area_Type.STUB]
        ospf_interfaces = [i for i in self.interfaces if i.area is not None]

        filters_ospf_in = [(rm, seq) for rm in self.ospf_in_route_maps for seq in rm.perm]
        filters_ospf_out = [(rm, seq) for rm in self.ospf_out_route_maps for seq in rm.perm]
        filters_bgp_in = [(rm, seq) for rm in self.bgp_in_route_maps for seq in rm.perm]
        filters_bgp_out = [(rm, seq) for rm in self.bgp_out_route_maps for seq in rm.perm]

        interface_features = list(itertools.product(supported_interface_features, ospf_interfaces))
        area_features = list(itertools.product(supported_ospf_area_features, self.ospf_areas))
        nssa_features = list(itertools.product(supported_ospf_nssa_features, nssa_areas))
        stub_features = list(itertools.product(supported_ospf_stub_features, stub_areas))
        router_features = list(itertools.product(supported_router_features, [None]))
        neighbour_features = list(
            itertools.product(supported_bgp_neighbour_features, [n.address for n in self.bgp_neighbours]))
        filter_ospf_in_features = list(itertools.product(supported_filter_ospf_in_features, filters_ospf_in))
        filter_ospf_out_features = list(itertools.product(supported_filter_ospf_out_features, filters_ospf_out))
        filter_bgp_in_features = list(itertools.product(supported_filter_bgp_in_features, filters_bgp_in))
        if self.router_type == RouterTypes.Cisco7200:
            filter_bgp_in_features.extend([(rm.fixed_match_features[seq], (rm, seq)) for (rm, seq) in filters_bgp_in])
        filter_bgp_out_features = list(itertools.product(supported_filter_bgp_out_features, filters_bgp_out))
        if self.router_type == RouterTypes.Cisco7200:
            filter_bgp_out_features.extend([(rm.fixed_match_features[seq], (rm, seq)) for (rm, seq) in filters_bgp_out])

        features = (interface_features + area_features + nssa_features + stub_features + router_features
                    + neighbour_features + filter_ospf_in_features + filter_ospf_out_features + filter_bgp_in_features
                    + filter_bgp_out_features)

        return list(map(lambda f: (f[0],) + f[1], itertools.product([self], features)))

    def get_possible_args(self, allowed_features=None):

        disabled_features = self.unsupported_features
        if allowed_features and disabled_features:
            allowed_features = [f for f in allowed_features if f not in disabled_features]
        elif disabled_features:
            allowed_features = [f for f in self.feature_list.all_features if f not in disabled_features]

        return self.feature_args.get_possible_args(self, allowed_features)

    def get_random_args(self, allowed_features=None):

        disabled_features = self.unsupported_features
        if allowed_features and disabled_features:
            allowed_features = [f for f in allowed_features if f not in disabled_features]
        elif disabled_features:
            allowed_features = [f for f in self.feature_list.all_features if f not in disabled_features]

        return self.feature_args.get_random_args(self, allowed_features)

    def write_config(self, path):

        return self.config_printer.write_config(self, path)


class RouteMap:

    def __init__(self, name):
        self.name = name

        self.perm = {}
        self.match_features = {}
        self.set_features = {}
        self.fixed_match_features = {}

    def __str__(self):
        return f' route-map {self.name}'


class PrefixList:

    def __init__(self, name):
        self.name = name

        self.perm = {}
        self.prefix = {}
        self.eq = {}

    def __str__(self):
        return self.name


class CommunityList:

    def __init__(self, name, perm=None):
        self.name = name
        self.perm = perm

        self.comms = []

    def __str__(self):
        return str(self.name)


class ASPathList:

    def __init__(self, name, regex, perm=None):
        self.name = name
        self.perm = perm
        self.regex = regex

    def __str__(self):
        return str(self.name)


class AccessList:

    def __init__(self, num, perm, net):
        self.num = num
        self.perm = perm
        self.net = net

    def __str__(self):
        return str(self.num)
