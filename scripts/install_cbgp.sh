#!/bin/sh

mkdir -p ./ext-systems
cd ./ext-systems

wget "http://sourceforge.net/projects/libgds/files/libgds-2.2.2.tar.gz"
tar xvzf "libgds-2.2.2.tar.gz"
cd libgds-2.2.2
./configure --prefix=/usr/app/baitfish/ext-systems
make
make install

export PKG_CONFIG_PATH="/usr/app/baitfish/ext-systems/lib/pkgconfig":$PKG_CONFIG_PATH

wget "http://sourceforge.net/projects/c-bgp/files/cbgp-2.3.2.tar.gz"
tar xvzf "cbgp-2.3.2.tar.gz"
cd cbgp-2.3.2
./configure --prefix=/usr/app/baitfish/ext-systems
make
make install
