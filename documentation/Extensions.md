# Extending Metha

## Adding additional Cisco/Juniper configuration options

* Extend the Enum lists in the corresponding ```config_features``` file, and add them to appropriate lists in the same file.
* In the corresponding ```feature_args``` file, add boundary value parameters to ```get_possible_args``` for your new feature and random parameters to ```get_random_args```
* In the corresponding ```config_printer``` file, add a function which converts your feature and its parameters to a configuration string, as well as one to disable the feature.

## Adding different router images

* add a new GNS3 JSON file to GNS3 folder. A configuration for an installed router image can be viewed by querying the GNS3 server
* add new router type in ```GNS3/router_types.py```
* add handling of your custom router type to ```GNS3/router_types_config.py```
    * Adjust ```get_config_type(file)``` to be able to identify configurations of your new router type
    * Add the interface names of your new router to ```interface_name```
    * Add functions to read interfaces, hostnames, and router-ids from the configuration of your new router to ```get_interfaces```, ```get_hostname```, and ```get_router_id``` respectively
    * Add a GNS3 node type class which can communicate with your new router type. There are two base classes which can be used for this: ```NetmikoNode``` which uses the netmiko library to communicate with your router. This can be used for most routers, netmiko supports a large number of different router vendors. Alternatively, there is also the ```PyEzNode``` class which uses Juniper's PyEz python interface to communicate with Juniper nodes. This does not support other vendors however. Add your new router node class to ```node_types``` in ```GNS3/router_types_config.py```.
    * Adjust the adapter offset for interfaces, i.e. if there is mismatch between the GNS3 adapter number the adapter number in the interface if necessary and add it to ```adapter_offset```.
    * Add a Metha router class for your new router type if necessary. Extend the ```Router``` class or one of the already implemented routers for this (```Cisco7200Router```, ```JuniperVMXRouter```). The new router needs to initialize its resources (e.g. route-maps, community lists, as-path lists, etc.) in the ```init_resources``` function and return the next available interface with ```get_next_interface```. Additionally, the router needs to specify its configuration features using the attributes ```feature_list```, ```feature_args```, and ```config_printer```. This router class should then be added to ```metha_router``` in ```GNS3/router_types_config.py```.

## Adding new vendor/OS support

* Add configuration files in ```RouterConfiguration/vendor```. Generally, this should consist of three files:
    * ```feature_list```: This should specify features (usually in the form of one or several ```Enum```s), as well as several lists on how to interpret these features. Examples can be found in the implemented feature lists
    * ```feature_args```: This file should specify two functions:
        * ```get_possible_args```: This should return a dict indexed by features. The dict should contain a list of boundary value parameters for each feature
        * ```get_random_args```: This should also return a dict indexed by features. However, the dict should simply contain a random assignment of parameters for each feature
    * ```config_printer```: This should specify the following:
        * ```feature_config```: This should be a dict which maps every feature to a function which converts the feature and its parameters to a configuration string
        * ```feature_disable```: This should be a dict specifying the same function, but instead of enabling the configuration feature, it should disable the feature.
        * ```config_mode(router, feature, arg)```: If a special configuration mode command needs to be entered before configuring this feature, this function should return said configuration mode. It should return a tuple where every element of the tuple is issued before actually issuing the configuration command.
        * ```exit_config_mode(feature)```: This is the same as above, but instead exits the configuration mode
        * ```write_config(router, path)```: This function should write the current configuration of ```router``` to ```path```.
        
* Additionally, the new configuration files need to be used by a Metha router class which needs to be defined as described above.
    

## Add new system

To add a support for a new system to Metha, extend the ```System``` class found in ```Systems/systems.py```.
The following is the default implementation of the ```System``` class. Any custom systems needs to implement at the very least the ```run``` method, which generates the routing table. This method takes as input the path to a test folder as well as adjacency information and must return a routing table in Metha's dataframe format. In addition, there are also the ```transform_rt``` and ```init_runner``` which can be redefined but do not have to be implemented. ```transform_rt``` defines a transformation that is applied to the oracle routing table computed by GNS3 which can update the table to reflect what is actually computed by the system. For example, C-BGP does not include any connected routes, so the ```transform_rt``` is used to remove all directly connected routes from the GNS routing table. ```init_runner``` initializes the test runner, this method can be used to implement a custom test runner for a specific system.
The system can also define a set of unsupported features as well as which columns of the routing tables are compared.

```
class System:

    def __init__(self):
        self.unsupported_features = []
        # Possible values:
        # Node, VRF, Network, Next_Hop, Next_Hop_IP, Next_Hop_Interface, Protocol, Metric, Admin_Distance, Tag
        self.compare_items = [
            'Node',
            'Network',
            'Next_Hop',
            'Next_Hop_IP',
            'Next_Hop_Interface',
            'Protocol',
            'Metric',
            'Admin_Distance'
        ]

    @staticmethod
    def run(path, adj):
        raise NotImplementedError

    @staticmethod
    def transform_rt(df):
        return df

    def init_runner(self, path, t, num, allowed_features=None):
        topo = topology.Topology(**t)
        router_features = [f for r in topo.routers for f in r.get_supported_features(allowed_features)]
        runner = TestRunner(path, topo, self, router_features)
        runner.test_num = num
        possible_args = {f: r.get_possible_args(allowed_features)[f] for r in topo.routers for f in
                         r.get_possible_args(allowed_features)}

        return runner, router_features, possible_args
```

## Change to different oracle

To change to a different oracle, implement a custom extension of the ```TestRunner``` class. The ```run_test``` method then needs to be adjusted to communicate the test cases to your new oracle instead of GNS3. Alternatively, the GNS3 interface could also be reused for this by adjusting the communication methods used internally by the interface. By exposing the same interface as the original GNS3 interface, the test runner would only need to be adjusted to use the new interface instead of the GNS3 interface.

## Adding a custom test generation method

To add a custom test generation method, extend the ```TestGenerationEngine``` class. Your new generator needs to implement the methods ```generate``` and ```next_test```, where ```generate``` performs preprocessing to the test generation (such as generating combinatorial tests) and is called once, and ```next_test``` should return the actual test case specification.
