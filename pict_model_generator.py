import subprocess

import pandas as pd

from settings import PICT_PATH
from Systems.CBGP.Configuration import cbgp_config_features
from utils import *


def no_off(router, feature, arg):
    """
    Checks whether a value to turn off the feature should be added to the PICT model. This is usually indicated
    by the value -1.
    :param router:
    :param feature:
    :param arg:
    :return:
    """
    no_off_features = [
        cbgp_config_features.FilterFeatures.FILTER_MATCH_OUT,
        cbgp_config_features.FilterFeatures.FILTER_MATCH_IN,
        cbgp_config_features.FilterFeatures.FILTER_ACTION_IN,
        cbgp_config_features.FilterFeatures.FILTER_ACTION_OUT
    ]

    if feature in no_off_features:
        return True
    else:
        return False


def generate_model(router_features, possible_args):
    """
    Generate the PICT model, for every feature create a list of possible numeric values
    :param router_features: Router features used to run PICT
    :param possible_args: Possible arguments for these features
    :return: Dict mapping features to value lists
    """
    possible_values = {}

    for (router, feature, arg) in router_features:
        possible_values[router, feature, arg] = list(range(len(possible_args[feature])))

    return possible_values


def write_model(path, possible_values):
    """
    Write the PICT model file to disk
    :param path: Location and name of the created PICT file
    :param possible_values: PICT model dict
    :return: 
    """
    s = []
    feature_to_str = {}

    for arg in possible_values:
        feature_str = str_repr(arg).replace(',', '')
        feature_to_str[arg] = feature_str
        if no_off(*arg):
            s.append(feature_str + ': ' + ','.join(map(str, possible_values[arg])))
        else:
            s.append(feature_str + ': ' + '-1 (100),' + ','.join(map(str, possible_values[arg])))

    with open(path, 'w') as f:
        f.write('\n'.join(s))

    return feature_to_str


def call_pict(inpath, outpath):

    with open(outpath, 'w') as f:
        ret = subprocess.call([PICT_PATH, inpath], stdout=f)

    df = pd.read_csv(outpath, sep='\t')

    return df
