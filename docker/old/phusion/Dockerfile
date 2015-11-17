# Copyright 2014 Joseph Wolff & eRacks Systems

FROM phusion/baseimage
# ubuntu:trusty

MAINTAINER Joseph Wolff, joe@eracks.com

RUN apt-get update && apt-get upgrade -y 
# -o DPkg::Options::=--force-confold


#VOLUME ['/etc/salt/minion.d', ]
ADD minion.conf /etc/salt/minion.d/


# Install Development Vdersion @ 2014.7
# See: https://github.com/saltstack/salt-bootstrap/issues/394

ADD https://bootstrap.saltstack.com /usr/local/bin/install_salt.sh
RUN chmod +x /usr/local/bin/install_salt.sh
ADD relay.sh /usr/local/bin/relay.sh
RUN chmod +x /usr/local/bin/relay.sh
RUN relay.sh install_salt.sh git v2014.7


CMD ["/sbin/my_init"]