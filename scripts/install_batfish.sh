#!/bin/sh

mkdir -p ./ext-systems
cd ./ext-systems

git clone "https://github.com/batfish/batfish.git"
cd batfish
tools/install_z3.sh
source tools/batfish_functions.sh
batfish_build_all
