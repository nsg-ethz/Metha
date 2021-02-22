import json


def int_to_ip(ip):
    """
    Convert a 32-bit integer into IPv4 string format
    :param ip: 32-bit integer
    :return: IPv4 string equivalent to ip
    """
    if type(ip) is str:
        return ip
    return '.'.join([str((ip >> i) & 0xff) for i in [24, 16, 8, 0]])


def int_to_lower_mask(mask):
    """
    Convert an integer into a lower mask in IPv4 string format where the first mask bits are 0
    and all remaining bits are 1 (e.g. 8 -> 0.255.255.255)
    :param mask: mask as integer, 0 <= mask <= 32
    :return: IPv4 string representing a lower mask corresponding to mask
    """
    return '.'.join([str((0xffffffff >> mask >> i) & 0xff) for i in [24, 16, 8, 0]])


def int_to_upper_mask(mask):
    """
    Convert an integer into an upper mask in IPv4 string format where the first mask bits are 1
    and all remaining bits are 0 (e.g. 8 -> 255.0.0.0)
    :param mask: mask as integer, 0 <= mask <= 32
    :return: IPv4 string representing an upper mask corresponding to mask
    """
    return '.'.join([str((0xffffffff << (32 - mask) >> i) & 0xff) for i in [24, 16, 8, 0]])


def mask_address(ip, prefix):
    """
    Reduce a 32-bit integer to its first prefix bits
    :param ip: 32-bit integer
    :param prefix: integer, 0 <= prefix <= 32
    :return: integer corresponding to ip where bits [prefix+1..32] are 0
    """
    return ip & (0xffffffff << (32 - prefix))


def ip_to_int(ip_str):
    """
    Convert an IPv4 string to its integer representation
    :param ip_str: IPv4 address string
    :return: 32-bit integer corresponding to ip_str
    """
    return sum(int(ip) << i for ip, i in zip(ip_str.split('.'), [24, 16, 8, 0]))


def str_recurse(features):
    """
    Helper function to recursively convert "base elements" to strings while leaving datastructures intact
    :param features: item or collection of items to convert to strings
    :return: string representation of features where datastructures are preserved
    """
    if type(features) == tuple:
        return tuple(map(str_recurse, features))
    elif type(features) == list:
        return list(map(str_recurse, features))
    elif type(features) == set:
        return set(map(str_recurse, features))
    elif type(features) == dict:
        return dict(map(lambda kv: (str_recurse(kv[0]), str_recurse(kv[1])), features.items()))
    else:
        return str(features)


def str_repr(features):
    """
    Convert to nice string representation
    :param features: item to be converted to a string representation
    :return: string representation of features
    """
    return str(str_recurse(features))


def filter_optional(l, filter_list=None):
    """
    Optionally filter elements in a list according to a second filter list
    :param l: list to potentially filter
    :param filter_list: filter list specifying all elements which are allowed in the returned list
    :return: if filter_list is not None, list containing the intersection of l and filter_list else l
    """
    if filter_list is None:
        return l
    else:
        return [f for f in l if f in filter_list]


def get_unique_features(router_features):
    """
    Convert router feature triplets to unique config features
    :param router_features: Iterable of router feature triplets
    :return: Set of unique features
    """
    return set([feature for (router, feature, arg) in router_features])


def filter_features(router_features, features):
    """
    Filter router feature triplets according to specified feature set
    :param router_features: Iterable of router feature triplets
    :param features: Iterable of features to restrict to
    :return: List of router feature triplets where the feature is in features
    """
    return [(router, feature, arg) for (router, feature, arg) in router_features if feature in features]


class CustomEncoder(json.JSONEncoder):
    """
    Custom encoder which encodes sets as lists in JSON
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def write_json(minsets, path):
    """
    Write JSON file which can handle sets
    :param minsets: structure to be converted to JSON format
    :param path: path where the JSON file will be saved
    """
    with open(path, 'w') as f:
        json.dump(str_recurse(minsets), f, indent=4, separators=(',', ': '), cls=CustomEncoder)


def filter_dict(it, d):
    """
    Filters a dictionary to all elements in a given iterable
    :param it: iterable containing all keys which should still be in the dictionary
    :param d: the dictionary to filter
    :return: dictionary with all elements of d whose keys are also in it
    """
    if d is None:
        return {}
    return dict(filter(lambda cf: cf[0] in it, d.items()))
