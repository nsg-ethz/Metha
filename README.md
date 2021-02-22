# Metha: Automated Testing of Network Analyzers
## Installation

### Docker Installation

* Install GNS3 by following the [install instructions](https://docs.gns3.com/docs/getting-started/installation/linux) appropriate for your system
* Plug in router images in the GNS3 folder of your installation, on Linux, by default this is the directory ```~/GNS3/images```
* Run ```docker_setup.sh``` to generate the necessary docker images.
* Run the GNS3 server, by default this can be done by simply running ```gns3server``` in a terminal
* Then run ```run_batfish.sh``` if you want to run tests using Batfish. This uses the batfish docker image, it can later be resumed by using ```docker start batfish```.
* Finally, run ```run_docker.sh``` to run the Metha docker image. By default, this will mount this directory into ```~/metha``` inside the docker image for easy access to files there. This docker container can be resumed by running ```docker start metha-system``` after the initial generation.


### Manual Installation

* Install GNS3 by following the [install instructions](https://docs.gns3.com/docs/getting-started/installation/linux) appropriate for your system
* Plug in router images in the GNS3 folder of your installation
* There are some scripts available for the installation of the following programs in the ```scripts``` folder. However, all prerequisites need to be installed first.
* Install [PICT](https://github.com/microsoft/pict)
* Install [Batfish](https://github.com/batfish/batfish)
* Install [NV](https://github.com/NetworkVerification/nv)
* Install the NV [fork](https://github.com/NetworkVerification/batfish) of Batfish
* Install [C-BPG](http://c-bgp.sourceforge.net/downloads.php)
* Finally clone [ntc-templates](https://github.com/networktocode/ntc-templates), and, if you did not clone it to ```~```, set the following environment variable: 
```
export NET_TEXTFSM=/path/to/ntc-templates/templates/
```
* Clone this git repository and run 
```
pip install -r requirements.txt
```
* Finally adjust ```config.json``` to point to your manually installed files

## Setup to run Metha:
* Systems to be tested needs to be properly installed
* To test Batfish, additionally the Batfish server needs to be up and running. This can be done by running ```scripts/run_batfish.sh```.
* The GNS3 Server needs to be properly installed and running
  * The router image used should be installed to the GNS3 image directory. By default, Metha supports the Cisco ```c7200-adventerprisek9-mz.124-24.T8.image``` image and Juniper VMX which requires ```junos-vmx-x86-64-18.2R1.9.qcow2```, ```vmxhdd.img```, ```metadata-usb-re.img```, and ```vFPC-20180605.img``` to be installed in GNS3, i.e. to be placed in the ```images``` directory of GNS3.
  * Password protection of the GNS3 server needs to be disabled

## Running full Metha
To generate new test cases, run
```
python3 metha.py -p path run -s system
```
where ```path``` is the directory where the new test cases will be saved to after generation, and ```system``` is the system which is being tested, by default the supported systems are ```batfish```, ```nv```, ```cbgp```.
The GNS3 server needs to be running, by default Metha expects a local GNS3 server. In addition, to test Batfish the Batfish server also needs to be running locally. This will generate a ```results``` directory on the same level as ```path```. In this directory, a summary of results will be saved as well as reports for any discrepancies found. In the folder passed by ```path```, Metha will generate a subdirectory for every test case which includes all configurations as well as the computed routing tables in ```csv``` format.

## Running a single comparison: 
Both the Batfish and GNS3 Servers must be running locally, then run
```
python3 metha.py -p path single-test -s system
```
where ```path``` is a directory containing at least a folder ```config``` of configs used for the routers, plus possibly a topology file (can be generated as well). If C-BGP is used, additionally there must also be a file called ```cbgp_config.txt``` in the folder at ```path```.

## Additional documentation

More detailed documentation can be found in the documentation folder in this git repository.
Specifically, the following documentation files are available:

* [```Command-Line-Options.md```](./documentation/Command-Line-Options.md): Describes all different command-line options to running Metha, including how to run different evaluation configurations
* [```Configuration.md```](./documentation/Configuration.md): Describes the Metha configuration in the ```config.json``` file. This sets up a lot of base configurations such as the location of external executables.
* [```Extensions.md```](./documentation/Extensions.md): Describes how to extend Metha, in particular to different routers and to testing different systems.
* [```Network-Configuration-Features.md```](./documentation/Network-Configuration-Features.md): Describes how to restrict the set of configuration features used by Metha.
* [```Topology.md```](./documentation/Topology.md): Describes how to define new topologies to run Metha on.

## Team

Metha is a project at the ICE Center at ETH Zurich, comprising researchers from the Networked Systems Group and the Secure, Reliable, and Intelligent Systems Lab:

* [Rüdiger Birkner](https://nsg.ee.ethz.ch/people/ruediger-birkner/)
* Tobias Brodmann
* [Petar Tsankov](https://www.sri.inf.ethz.ch/people/petar)
* [Laurent Vanbever](https://nsg.ee.ethz.ch/people/laurent-vanbever/)
* [Martin Vechev](https://www.sri.inf.ethz.ch/people/martin)
