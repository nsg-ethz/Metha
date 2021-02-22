import os
import json

with open('config.json') as f:
    j = json.load(f)

TOPOLOGY_PATH = os.path.abspath(j['topology_path'])
MAX_BASE_TESTS = j['max_base_tests']
GNS_ROUTER_PATH = os.path.abspath(j['gns3']['router_path'])
GNS_SERVER_HOST = j['gns3']['host']
GNS_SERVER_PORT = j['gns3']['port']
GNS_NUM_UNCHANGED = j['gns3']['rt_converged_num']
GNS_SLEEP_TIME = j['gns3']['rt_read_sleep']
GNS_RESTART_INTERVAL = j['gns3']['restart_interval']
GNS_METHA_SAME_SYSTEM = j['gns3']['same_system']
PICT_PATH = os.path.abspath(j['pict_command'])
NV_PATH = os.path.abspath(j['nv_command'])
CBGP_COMMAND = j['cbgp_command']
NV_BATFISH = os.path.abspath(j['nv_batfish'])
