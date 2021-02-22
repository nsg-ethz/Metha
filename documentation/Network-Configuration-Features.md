# Configuring allowed network configuration features

In ```RouterConfiguration/feature_parser.py```, Metha includes a list of all network configuration feature types. By default, the supported feature types are ```CiscoConfiguration``` in the file ```RouterConfiguration/Cisco/cisco_config_features.py```, ```JuniperConfiguration``` in the file ```RouterConfiguration/Juniper/juniper_config_features.py```, and C-BGP configuration in the file ```CBGP/cbgp_config_features.py```. Each of these files includes a range of Enum's describing different types of features. For example, Juniper configurations include the types ```ProtocolIndependentFeatures``` used mainly for static routes, ```OSPFFeatures``` for all OSPF related features, ```BGPFeatures``` to control BGP features, and ```PolicyFeatures``` for all features related to Juniper's policies.
To define a custom set of allowed or disabled features, use a JSON file defined as follows:

```
{
ConfigType: {
    FeatureType: [
        Features
        ]
    }
}
```

## Example

The following configuration file defines static routes as well as the ospf features distance, redistribution of static routes, and ospf cost of interfaces of cisco configurations. Such a JSON file can then be provided to Metha to restrict the used configuration features, either to only use these features or to disable these features.

```
{
    "CiscoConfiguration": {
        "RouterFeatures": [
            "RouterFeatures.STATIC_ROUTE"
        ],
        "OSPFFeatures": [
            "OSPFFeatures.DISTANCE",
            "OSPFFeatures.REDISTRIBUTE_STATIC",
            "OSPFFeatures.INTERFACE_OSPF_COST",
        ]
    }
}
```

A file containing all possible configuration features can be created by running ```python3 metha.py get-config-features```.
