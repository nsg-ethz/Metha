import json

from Systems.CBGP.Configuration import cbgp_config_features
from RouterConfiguration.Cisco import cisco_config_features
from RouterConfiguration.Juniper import juniper_config_features
from utils import write_json

config_file = {
    'CiscoConfiguration': cisco_config_features,
    'JuniperConfiguration': juniper_config_features,
    'CBGPConfiguration': cbgp_config_features
}


def write_all_features(path):
    features = {}
    for config_type in config_file:
        features[config_type] = {}
        for feature_type in config_file[config_type].feature_type:
            features[config_type][feature_type] = list(config_file[config_type].feature_type[feature_type])

    write_json(features, f'{path}config_features.json')


def parse_feature_list(path, disable_list=False):

    feature_list = []
    if disable_list:
        for config_type in config_file:
            feature_list.append(config_file[config_type].all_features)

    with open(path) as file:
        features = json.load(file)

        for config_type in features:
            for feature_type in features[config_type]:
                for feature in features[config_type][feature_type]:
                    f = config_file[config_type].enum_from_string(feature_type)[feature]
                    if not disable_list:
                        feature_list.append(f)
                    else:
                        feature_list.remove(f)

    return feature_list
