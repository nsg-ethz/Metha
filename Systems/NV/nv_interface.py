import subprocess

from Systems.NV import nv_parser
from settings import NV_PATH, NV_BATFISH
from Systems.systems import System


class NVInterface(System):

    def __init__(self):
        super().__init__()
        self.compare_items = [
            'Node',
            'Network',
            'Next_Hop',
            'Protocol'
        ]

    def __str__(self):
        return 'NV'

    @staticmethod
    def run(path, adj):
        with open(f'{path}nv-compile', 'w') as f:
            f.write(f'init-snapshot {path} nv-snapshot\n'
                    f'get compile doData="false", file="{path}nv-gen", doNodeFaults="false",'
                    f' singlePrefix="false", doNextHop="true"')

        subprocess.call(f'source {NV_BATFISH}/tools/batfish_functions.sh; allinone -cmd {path}nv-compile', shell=True)

        with open(f'{path}nv-gen_control.nv') as f:
            data = f.read()
            data = data.replace('o.ad', 'o.ospfAd')
            conv = nv_parser.router_to_nv_node_conversion(data)

        with open(f'{path}nv-gen_control.nv', 'w') as f:
            f.write(data)

        with open(f'{path}nv_result.txt', 'w') as f:
            subprocess.call([NV_PATH, '-simulate', '-verbose', f'{path}nv-gen_control.nv'], stdout=f)

        with open(f'{path}nv_result.txt') as f:
            rt = nv_parser.parse_results(f.read())

        return nv_parser.build_rt(rt, conv, adj), None, None

    @staticmethod
    def transform_rt(df):
        df.loc[df['Protocol'] == 'ospfIA', 'Protocol'] = 'ospf'
        df.loc[df['Protocol'] == 'ospfE1', 'Protocol'] = 'ospf'
        df.loc[df['Protocol'] == 'ospfE2', 'Protocol'] = 'ospf'
        return df
