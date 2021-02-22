# Metha Configuration

The configuration for Metha can be found in ```config.json```. Metha contains the following configuration parameters:

* ```topology_path```: This is the path of the topology files used when running Metha
* ```max_base_tests```: The maximum number of tests performed to find a valid base configuration
* ```gns3```
    * ```host```: The host address used to communicate with the GNS3 server
    * ```port```: The port used to communicate with the GNS3 server
    * ```router_path```: This is the path to the JSON files describing GNS3 routers
    * ```rt_converged_num```: The number of times a routing table needs to be read unchanged to be considered converged
    * ```rt_read_sleep```: The number of seconds we wait between consecutive reads of the routing tables
    * ```restart_interval```: GNS3 is periodically restarted since otherwise there can be problems with artifacts from the previous tests persisting to the next test. This interval defines after how many tests GNS3 is restarted.
    * ```same_system```: This is a boolean variable that indicates whether GNS3 and Metha are running on the same system. If it is true, Metha will send configuration files directly to GNS3 instead of reading them and issuing corresponding commands. If it is false, all config files are read, and routers will only be configured via telnet (instead of trying to use a startup configuration where possible).
* ```pict_command```: The command issued to run PICT, usually the path to the compiled PICT executable
* ```nv_command```: The command issued to run NV, usually the path to the built NV executable
* ```cbgp_command```: Command used to run C-BGP
* ```nv_batfish```: Path to the NV fork of batfish, used for compiling NV files from configurations

## Default configuration

```
{
  "topology_path": "./topologies",
  "max_base_tests": 100,
  "gns3": {
    "host": "localhost",
    "port": 3080,
    "router_path": "./GNS3/node-definitions",
    "rt_converged_num": 10,
    "rt_read_sleep": 10,
    "restart_interval": 20
  },
  "pict_command": "./ext-systems/pict/pict",
  "nv_command": "./ext-systems/network-verification/nv/_build/default/src/exe/main.exe",
  "cbgp_command": "cbgp",
  "nv_batfish": "./ext-systems/network-verification/batfish"
}
```
