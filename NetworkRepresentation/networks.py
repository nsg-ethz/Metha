import random

from utils import mask_address


def select_subnet(network):
    """
    Randomly selects a subnet of the specified network
    :param network: Network object for which to select a subnet
    :return: Network object specifying a subnet of network
    """
    prefix = random.randint(min(network.prefix + 1, 31), 31)
    max_address = network.address | ((1 << (32 - prefix)) - 1)
    address = mask_address(random.randint(network.address, max_address), prefix)
    return Network(address, prefix)


def select_supernet(network):
    """
    Randomly selects a supernet of the specified network
    :param network: Network object for which to select a supernet
    :return: Network object specifying a supernet of network
    """
    prefix = random.randint(1, max(1, network.prefix - 1))
    return Network(mask_address(network.address, prefix), prefix)


def select_ip_from_network(network):
    """
    Randomly selects an IP address from a particular network
    :param network: Network from which to select the IP address
    :return: IP address as integer from network
    """
    max_address = network.address | ((1 << (32 - network.prefix)) - 1)
    return random.randint(network.address, max_address)


def select_ip_address(topology):
    """
    Randomly selects an IP address from the list of used networks in a given topology
    :param topology: Topology from which the IP address is selected
    :return: IP address as integer
    """
    return random.choice(list(map(select_ip_from_network, topology.network_list())))


def select_network(networks):
    network = random.choice(networks)
    mode = random.randrange(5)

    if mode == 0:
        subnet = select_subnet(network)
        return subnet
    elif mode == 1:
        supernet = select_supernet(network)
        return supernet
    else:
        return network


class Network:

    def __init__(self, address, prefix):
        """
        Initialize Network object
        :param address: Address of the network, last 32-prefix bits should be 0
        :param prefix: Prefix mask used for this network
        """
        self.address = address
        self.prefix = prefix
