import pexpect
import pandas as pd

from Systems.CBGP import cbgp_parser
from Systems.CBGP.Configuration import cbgp_feature_args
from Systems.CBGP.Configuration.cbgp_config_features import *
from Systems.CBGP.Translation.router_translator import cbgp_translator
from Systems.CBGP.cbgp_runner import CBGPRunner
from settings import CBGP_COMMAND
from NetworkRepresentation import routers, topology
from Systems.systems import System

from utils import *


def get_cbgp_features(topo, allowed_features=None):
    supported_global_features = filter_optional(global_features, allowed_features)
    features = [(None, f, None) for f in supported_global_features]
    neighbour_filters = {}
    comm_lists = {}
    next_hop_acls = {}
    as_path_lists = {}

    for router in topo.routers:
        num_acls = 1
        num_comm_lists = 1
        features.append((router, RouterFeatures.STATIC_ROUTE, None))

        for neighbour in router.bgp_neighbours:

            neighbour_filters[neighbour, 'out'] = routers.RouteMap(f'map_out_{neighbour.address}')
            neighbour_filters[neighbour, 'out'].perm[5] = 'permit'
            neighbour_filters[neighbour, 'out'].set_features[5] = (cbgp_translator[router.feature_list].next_filter(),)
            neighbour_filters[neighbour, 'in'] = routers.RouteMap(f'map_in_{neighbour.address}')

            router.bgp_in_route_maps.append(neighbour_filters[neighbour, 'in'])
            router.bgp_out_route_maps.append(neighbour_filters[neighbour, 'out'])

            supported_neighbour_features = filter_optional(neighbour_features, allowed_features)
            features.extend([(router, f, neighbour) for f in supported_neighbour_features])

            next_hop_acls[router, neighbour.address] = routers.AccessList(num_acls, 'permit', topology.Network(neighbour.address, 32))
            router.access_lists.append(next_hop_acls[router, neighbour.address])
            num_acls = num_acls + 1

            for i in [10]:
                neighbour_filters[neighbour, 'out'].perm[i] = 'permit'
                neighbour_filters[neighbour, 'in'].perm[i] = 'permit'
                features.append((router, FilterFeatures.FILTER_MATCH_OUT, (neighbour, 'out', i)))
                features.append((router, FilterFeatures.FILTER_ACTION_OUT, (neighbour, 'out', i)))
                features.append((router, FilterFeatures.FILTER_MATCH_IN, (neighbour, 'in', i)))
                features.append((router, FilterFeatures.FILTER_ACTION_IN, (neighbour, 'in', i)))

        for interface in router.interfaces:
            if interface.area is not None:
                supported_interface_features = filter_optional(interface_features, allowed_features)
                features.extend([(router, f, interface) for f in supported_interface_features])

        for (AS, comm) in topo.communities:
            comm_lists[router, f'{AS}:{comm}'] = routers.CommunityList(num_comm_lists, 'permit')
            comm_lists[router, f'{AS}:{comm}'].comms.append(f'{AS}:{comm}')
            router.comm_lists.append(comm_lists[router, f'{AS}:{comm}'])
            num_comm_lists = num_comm_lists + 1

        for comm in cbgp_translator[router.feature_list].get_extra_comms():
            comm_lists[router, comm] = routers.CommunityList(num_comm_lists, 'permit')
            comm_lists[router, comm].comms.append(comm)
            router.comm_lists.append(comm_lists[router, comm])
            num_comm_lists = num_comm_lists + 1

        for i, AS in enumerate(topo.ASes):
            as_path_lists[router, AS] = routers.ASPathList(i + 1, cbgp_translator[router.feature_list].AS_regex(AS), 'permit')
            router.as_path_lists.append(as_path_lists[router, AS])

    return features, {'neighbour_filters': neighbour_filters, 'comm_lists': comm_lists, 'next_hop_acls': next_hop_acls, 'as_path_lists': as_path_lists}


def translate_router_features(topo, filters_lists_conversion):
    router_features = [
        rf for router in topo.routers for rf in
        cbgp_translator[router.feature_list].get_router_features(router, filters_lists_conversion['neighbour_filters'])
    ]

    return router_features


class CBGPInterface(System):

    def __init__(self):
        super().__init__()
        self.compare_items = [
            'Node',
            'Network',
            'Next_Hop',
            'Next_Hop_IP',
            'Next_Hop_Interface',
            'Protocol',
            'Metric',
        ]

    def __str__(self):
        return 'CBGP'

    @staticmethod
    def run(path, adj):
        """
        Run C-BGP
        :param path: Path to C-BGP config file
        :param adj: Adjacency information
        :return: Routing tables received from C-BGP
        """
        rt = pd.DataFrame(
            columns=["Node", "VRF", "Network", "Next_Hop", "Next_Hop_IP", "Next_Hop_Interface", "Protocol",
                     "Metric", "Admin_Distance", "Tag"])
        p = pexpect.spawn(CBGP_COMMAND)

        with open(f'{path}cbgp_config.txt') as f:
            config = f.read()

        p.write(config)
        p.expect('sim run\r\ncbgp> ')
        for router in adj['router-ids']:
            p.write(f'net node {adj["router-ids"][router]} show rt *\n')
            p.expect('cbgp> ')
            rt = rt.append(cbgp_parser.parse_cbgp(p.before.decode('ascii'), router, adj), ignore_index=True)
        p.close()
        return rt, None, None

    @staticmethod
    def transform_rt(df):
        """
        Transform applied to the oracle routing table when using C-BGP
        :param df: Routing table dataframe computed by the oracle
        :return: Transformed routing table
        """
        return df.loc[df['Protocol'] != 'connected']

    def init_runner(self, path, t, num, allowed_features=None):
        topo = topology.Topology(**t, init_resources=False)

        for router in topo.routers:
            for neighbour in router.bgp_neighbours:
                if neighbour.AS != router.AS:
                    pass  # router.fixed_static_routes.append((Network(neighbour.address, 32), neighbour.interface))

        cbgp_features, resource_conversion = get_cbgp_features(topo, allowed_features)
        router_features = translate_router_features(topo, resource_conversion)
        runner = CBGPRunner(path, topo, self, router_features, cbgp_features, resource_conversion)
        runner.test_num = num
        possible_args = {f: cbgp_feature_args.get_possible_args(r, allowed_features)[f] for r in topo.routers for f in
                         cbgp_feature_args.get_possible_args(r, allowed_features)}

        return runner, cbgp_features, possible_args
