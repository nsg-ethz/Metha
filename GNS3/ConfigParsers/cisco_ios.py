import re

# Regex to find the host name
hostname_cisco_regex = re.compile(r'hostname\s+(?P<name>\S+)')
# Regex to find interface definitions as well as assigned addresses
interface_cisco_regex = re.compile(
    r'interface\s+FastEthernet(?P<adapter>\d)/(?P<port>\d)(?!\n no ip address)(.*?)\n\s*'
    r'ip\s+address\s+'
    r'(?P<address1>\d\d?\d?)\.(?P<address2>\d\d?\d?)\.'
    r'(?P<address3>\d\d?\d?)\.(?P<address4>\d\d?\d?)\s+'
    r'(?P<mask1>\d\d?\d?)\.(?P<mask2>\d\d?\d?)\.'
    r'(?P<mask3>\d\d?\d?)\.(?P<mask4>\d\d?\d?)',
    re.DOTALL | re.MULTILINE
)
# Regex to find the router id (there is no differentiation between ospf or bgp router-id)
router_id_cisco_regex = re.compile(r'router-id\s+(?P<address>\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?)')


def get_hostname(config):
    """
    Find the host name in a Cisco router configuration
    :param config: Configuration as string
    :return: host name in the given configuration
    """
    host = hostname_cisco_regex.search(config)
    return host.group('name')


def get_router_id(config):
    """
    Find the router id if it is defined in the given Cisco config
    :param config: Configuration as string
    :return: Router id as string if one is found, None otherwise
    """
    rid = router_id_cisco_regex.search(config)
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

    for i in interface_cisco_regex.finditer(config):
        interface_address = ('.'.join([
            i.group('address1'),
            i.group('address2'),
            i.group('address3'),
            i.group('address4')
        ]))
        adapter = i.group('adapter')
        port = i.group('port')
        mask = ('.'.join([
            i.group('mask1'),
            i.group('mask2'),
            i.group('mask3'),
            i.group('mask4')
        ]))

        interfaces.append((interface_address, mask, int(adapter), int(port)))

    return interfaces
