from enum import Enum, auto


class Protocols(Enum):
    """
    Protocols supported by Metha
    """
    STATIC = auto()
    OSPF = auto()
    BGP = auto()


class OSPF_Area_Type(Enum):
    """
    OSPF area types which can be used by Metha
    """
    DEFAULT = auto()
    STUB = auto()
    NSSA = auto()


def protocol_from_string(prot):
    """
    Converts protocols from string representation used in JSON files to the Enum used in Metha
    :param prot: String protocol to convert
    :return: Enum corresponding to the string prot
    """
    translation = {
        'static': Protocols.STATIC,
        'ospf': Protocols.OSPF,
        'bgp': Protocols.BGP
    }

    return translation[prot]
