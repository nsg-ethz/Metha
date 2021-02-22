#!/bin/sh

mkdir -p ./ext-systems
cd ./ext-systems

git clone "https://github.com/microsoft/pict.git"
cd pict
make
