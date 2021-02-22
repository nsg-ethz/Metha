FROM ubuntu:20.04

WORKDIR /root

ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt .
COPY ./scripts ./scripts

RUN apt-get update && apt-get install -y software-properties-common git python3 python3-pip opam z3 wget pkg-config libgmp-dev libzmq3-dev maven openjdk-8-jdk libpcre3 libpcre3-dev
RUN opam init --disable-sandboxing

RUN pip3 install -r requirements.txt

RUN chmod +x ./scripts/install_pict.sh
RUN ./scripts/install_pict.sh
RUN chmod +x ./scripts/install_nv.sh
RUN ./scripts/install_nv.sh
RUN chmod +x ./scripts/install_cbgp.sh
RUN ./scripts/install_cbgp.sh
RUN git clone https://github.com/networktocode/ntc-templates.git
