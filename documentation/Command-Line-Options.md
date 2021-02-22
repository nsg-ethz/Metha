# Metha command-line options

## General Options

The following options apply everywhere:

* ```--enable-logging```: Enables creation of Netmiko and Metha logs
* ```-p dir, --path dir```: All Metha modes require a path to a directory where they operate, depending on other configurations the path can be used differently

## Run Metha

Metha's combinatorial testing can be run using ```python3 metha.py run```. where ```path``` is the directory in which Metha will save automatically generated test cases as well as test results, and ```system``` is a system supported by Metha.

In addition, this mode supports the following configuration options:

* ```--allowed-features file```: This can be used to pass a JSON file containing a subset of features which are allowed to be used by Metha
* ```--disabled-features file```: This can be used to pass a JSON file containing a subset of features which are disabled
* If both an allowed features as well as a disabled features file are passed, only features which are allowed by both will be used (i.e. features which are not in the disable file and in the allow file)
* ```-t file, --topology file```: Passes a JSON topology file to Metha, Metha will then generate tests according to this topology. The topology format is described separately. By default, Metha will use all topologies in the configured topology folder, this can be used to overwrite this setting.
* ```-s sys, --system sys```: Sets the system which is tested, this setting is required, by default sys can be ```batfish```, ```nv```, or ```cbgp```.

## Run single comparison

This mode of Metha can be used to compare the routing table output for pre-generated configurations. The directory passed as ```path``` to Metha should contain a folder called ```config``` where router configurations are saved. In addition, if C-BGP is used, ```path``` must also contain a file called ```cbgp_config.txt``` which contains C-BGP settings corresponding to the router configurations in the ```config``` folder. This mode can be run using ```python3 metha.py path single-test -s system``` where ```path``` and ```system``` are defined as above.

## Run GNS3

This mode only sets up a GNS3 project for pre-generated configs, and runs this GNS3 project. This can be run using ```python3 metha.py run-gns```. The configuration files are expected to be in the same file structure as above.

## Get configuration features

This mode creates a JSON file containing all possible network configuration features which can be used in the files passed using the ```---alowed-features``` and ```--disabled-features``` options in different modes. It can be run using ```python3 metha.py get-config-features```.

## Run Evaluation

This mode is used for different submodes related to the evaluation of Metha. It is run using ```python3 metha.py eval```.

All evaluation modes have the following additional command-line options:

* ```-s sys, --system sys```: Defines the system used to run the evaluation. In evaluation modes this defaults to Batfish since this was used for the evaluation.
* ```--allowed-features file```: This can be used to pass a JSON file containing a subset of features which are allowed to be used by Metha
* ```--disabled-features file```: This can be used to pass a JSON file containing a subset of features which are disabled
* If both an allowed features as well as a disabled features file are passed, only features which are allowed by both will be used (i.e. features which are not in the disable file and in the allow file)
* ```-t file, --topology file```: Passes a JSON topology file to Metha, Metha will then generate tests according to this topology. The topology format is described separately. By default, Metha will use the topology used to generate the Metha evaluation.

### Run random baseline

This mode runs the completely random baseline used in Metha which is essentially equivalent to traditional grammar-based fuzzing. It can be run using ```python3 metha.py eval random-base```.
In additon, this mode adds the following options:

* ```-n N, --num-tests N```: Specifies how many test cases to generate for this baseline. This will default to the value used in the Metha evaluation.

### Run semantic Metha

This mode runs the semantic Metha baseline which generates tests randomly while ensuring semantic correctness of the generated tests. It can be run using ```python3 metha.py eval semantic```.
In additon, this mode adds the following options:

* ```-n N, --num-tests N```: Specifies how many test cases to generate for this baseline. This will default to the value used in the Metha evaluation.

### Run bounded Metha

This mode runs the bounded Metha baseline which additionally reduces feature parameters used to boundary values. It can be run using ```python3 metha.py eval bounded```.
In additon, this mode adds the following options:

* ```-n N, --num-tests N```: Specifies how many test cases to generate for this baseline. This will default to the value used in the Metha evaluation.

### Generate coverage information

This mode generates the combinatorial coverage information to compare the different baselines. It can be run using ```python3 metha.py eval coverage```.
In additon, this mode adds the following options:

* ```-n N, --num-tests N```: Specifies how many test cases to generate for the non-combinatorial baselines. This will default to the value used in the Metha evaluation. If the combinatorial testing results in a different number of test cases, there will be a mismatch between combinatorial and non-combinatorial tests, i.e. coverage measured for either more or less cases.

### Benchmark PICT runtime

This mode can be used to benchmark the runtime of the PICT combinatorial testing tool when applied to Metha's configuration generation. By default, it will run PICT on all topologies in the configured topology folder. This mode can be run using ```python3 metha.py eval pict-runtime```.
