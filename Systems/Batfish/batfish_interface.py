from pybatfish.client.commands import *
from pybatfish.question import bfq
from pybatfish.question.question import load_questions

from Systems.systems import System


class BatfishInterface(System):

    def __init__(self):
        super().__init__()

    @staticmethod
    def run(path, adj):
        """
        Generates the Batfish routing table
        :param path: Path to the config files used to generate the routing table
        :param adj: Adjacency information, not used by Batfish
        :return: Triplet of routing table, parse warning and init issues of Batfish
        """
        load_questions()
        bf_set_network('fuzzer')
        bf_init_snapshot(path)

        return bfq.routes().answer().frame(), bfq.parseWarning().answer().frame(), bfq.initIssues().answer().frame()

    def __str__(self):
        return 'Batfish'
