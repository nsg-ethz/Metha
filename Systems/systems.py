from NetworkRepresentation import topology
from test_runner import TestRunner


class System:

    def __init__(self):
        self.unsupported_features = []
        # Possible values:
        # Node, VRF, Network, Next_Hop, Next_Hop_IP, Next_Hop_Interface, Protocol, Metric, Admin_Distance, Tag
        self.compare_items = [
            'Node',
            'Network',
            'Next_Hop',
            'Next_Hop_IP',
            'Next_Hop_Interface',
            'Protocol',
            'Metric',
            'Admin_Distance'
        ]

    def __str__(self):
        return 'metha-testing-system'

    @staticmethod
    def run(path, adj):
        raise NotImplementedError

    @staticmethod
    def transform_rt(df):
        return df

    def init_runner(self, path, t, num, allowed_features=None):
        topo = topology.Topology(**t)
        router_features = [f for r in topo.routers for f in r.get_supported_features(allowed_features)]
        runner = TestRunner(path, topo, self, router_features)
        runner.test_num = num
        possible_args = {f: r.get_possible_args(allowed_features)[f] for r in topo.routers for f in
                         r.get_possible_args(allowed_features)}

        return runner, router_features, possible_args
