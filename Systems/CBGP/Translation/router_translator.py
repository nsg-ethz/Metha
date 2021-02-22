from RouterConfiguration.Cisco import cisco_config_features
from RouterConfiguration.Juniper import juniper_config_features
from Systems.CBGP.Translation import cisco_translator, juniper_translator

cbgp_translator = {
    cisco_config_features: cisco_translator,
    juniper_config_features: juniper_translator
}