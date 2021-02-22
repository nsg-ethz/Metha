import re

from utils import int_to_upper_mask

# Regex to find host name
hostname_juniper_regex = re.compile(r'host-name\s+(?P<name>\S+)')
# Regex to find interfaces and associated addresses
interface_juniper_regex = re.compile(r'set\s+interfaces\s+ge-0/0/(?P<adapter>\d)\s+unit\s+(?P<port>\d)\s+family\s+inet\s+address\s+'
                                     r'(?P<address1>\d\d?\d?)\.(?P<address2>\d\d?\d?)\.'
                                     r'(?P<address3>\d\d?\d?)\.(?P<address4>\d\d?\d?)/(?P<prefix>\d\d?)', re.MULTILINE)
# Regex to find the router id
router_id_juniper_regex = re.compile(r'router-id\s+(?P<address>\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)')


def get_hostname(config):
    """
    Find the host name in a Cisco router configuration
    :param config: Configuration as string
    :return: host name in the given configuration
    """
    host = hostname_juniper_regex.search(config)
    return host.group('name')


def get_router_id(config):
    """
    Find the router id if it is defined in the given Cisco config
    :param config: Configuration as string
    :return: Router id as string if one is found, None otherwise
    """
    rid = router_id_juniper_regex.search(config)
    if rid is not None:
        return rid.group('address')
    else:
        return None


def get_interfaces(config):
    """
    Find all configured interfaces in the given Cisco config and return their definitions
    :param config: Cisco configuration as string
    :return: tuple of interface address as string, mask address as string, adapter of the interface as int,
        and port of the interface as int
    """

    interfaces = []

    for i in interface_juniper_regex.finditer(config):
        interface_address = ('.'.join([
            i.group('address1'),
            i.group('address2'),
            i.group('address3'),
            i.group('address4')
        ]))
        adapter = i.group('adapter')
        port = i.group('port')
        prefix = int(i.group('prefix'))
        mask = int_to_upper_mask(prefix)

        interfaces.append((interface_address, mask, int(adapter), int(port)))

    return interfaces
