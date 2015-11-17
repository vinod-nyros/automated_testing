# Copyright 2014 Joseph Wolff & eRacks Systems

#FROM phusion/baseimage
#FROM ubuntu:trusty
#FROM ubuntu:latest

# based on dockerfile/ubuntu:
FROM dockerfile/supervisor

MAINTAINER Joseph Wolff, joe@eracks.com

ENV TERM linux

RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8


RUN apt-get update && apt-get upgrade -y
# -o DPkg::Options::=--force-confold

#VOLUME ['/etc/salt/minion.d', ]
ADD etc/salt/minion.d/minion.conf /etc/salt/minion.d/
ADD etc/salt/pki/ /etc/salt/pki/


# Install Development Vdersion @ 2014.7
# See: https://github.com/saltstack/salt-bootstrap/issues/394

ADD https://bootstrap.saltstack.com /usr/local/bin/install_salt.sh
RUN chmod +x /usr/local/bin/install_salt.sh
ADD relay.sh /usr/local/bin/relay.sh
RUN chmod +x /usr/local/bin/relay.sh
RUN relay.sh install_salt.sh git v2014.7

#RUN salt-call state.highstate | egrep -C 500 'Failed:[[:blank:]]*0'
#RUN salt-call state.highstate && echo nope | egrep -C 500 'Failed:[[:blank:]]*0'
RUN salt-call state.highstate | tee salt.log | egrep -C 500 'Failed:[[:blank:]]*0'

# OKOK - I think I figured this out:
# the parent image has the /etc/superviusor/conf.d dir declred as a volume (and wrkdir), 
# so changes to it are DISCARDED. (!)
#
# solution: pass volume in at runtime, er then example (!)

# old:

# Work around 2 symlink bugs:
# 1. saltstack says 'stdin not a tty' when doing ln -s and even readlinks (the unless clause)
# 2. docker commit won't commit hand-changes to /etc/supservisor/conf.d
#RUN ln -s /home/dev/eracks11/conf/etc/conf.d/* /etc/supervisor/conf.d/

# nope! neither of these work:
#RUN salt-call state.sls suprlinks
#RUN ln -s /home/dev/eracks11/conf/etc/conf.d/* /etc/supervisor/conf.d/
# docker just IGNORES the symlinks!

#RUN cp -r /home/dev/eracks11/conf/etc/conf.d/* /etc/supervisor/conf.d/

#RUN mkdir -p /etc/supervisor/confd
##RUN cp -r /home/dev/eracks11/conf/etc/conf.d/* /etc/supervisor/confd/
#RUN ln -s /home/dev/eracks11/conf/etc/conf.d/* /etc/supervisor/confd/

WORKDIR /home/dev/

#RUN mv /etc/supervisor/conf.d /etc/supervisor/conf.d.bak
#RUN mv /etc/supervisor/confd /etc/supervisor/conf.d


EXPOSE 22 2222 80 8080 8000 443

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
