from enum import Enum, auto


class RouterTypes(Enum):
    Cisco7200 = auto()
    JuniperVMX = auto()


def router_type_from_string(s):
    string_types = {
        'Cisco7200': RouterTypes.Cisco7200,
        'JuniperVMX': RouterTypes.JuniperVMX
    }

    return string_types[s]
