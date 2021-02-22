#!/bin/bash

mkdir -p ./ext-systems/network-verification
cd ./ext-systems/network-verification

eval $(opam env)
opam install -y \
  integers \
  batteries \
  ounit \
  ansiterminal \
  menhir \
  mlcuddidl \
  ppx_deriving \
  ppx_deriving_argparse \
  lru-cache \
  zarith \
  ocamlgraph \
  fileutils \
  parmap \
  fix \
  jupyter \
  dune

git clone "https://github.com/NetworkVerification/nv.git"
cd nv
dune build src/exe/main.exe

cd ..

git clone "https://github.com/NetworkVerification/batfish.git"
cd batfish
source tools/batfish_functions.sh
batfish_build_all
