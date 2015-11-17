Dockerfile phases:
=================

Setup: 

- At least this directory is required, although you can also check out the whole eracks11 tree

- The dockerfile build requires:  docker aha elinks 

  - aha is required to persist results files in color

  - elinks is required to view html5 result files in color.

  - sudo apt-get -y install docker aha elinks

  - Note that docker 1.2.x requires a PPA as of Oct 2014 on Ubu 14.04 LTS


Phase 1: docker build from supervisor (ubuntu-based) base image

Phase 2: salt it with eracksdev

Phase 3: launch, ssh in and Load the eRacks db with scripts/db/load_from_prod.sh

Normal operation - run with restart!


Phase 1 & 2:

sudo docker build -t eracksdev-phase1and2 . | tee >(aha > phase1and2-docker-outfile.html)

or to clear the cache:

sudo docker build --no-cache -t eracksdev-phase1and2 . | tee >(aha > phase1and2-docker-outfile.html)


Phase 3:

sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -p 443:443 -h dev.eracks.com eracksdev-phase1and2 | tee >(aha > phase3-docker-outfile.html)

launches supervisor, so ssh in - if you need to fix, launch bash:

sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -p 443:443 -h dev.eracks.com eracksdev-phase1and2 /bin/bash | tee >(aha > phase3-docker-outfile.html)


Notes:
=====

Phase 3 is still required to be separate, due to limitations of Docker volumes - 
  You can't specify a host-based volume in the dockerfile itself, so a separate run is required.


Bugs:
====

1. salt fails to create supervisor symlinks, with 'stdin is not a tty' - so log in manually with bash and:

- salt-call -l debug state.sls eracksdev whitelist=supervisor-symlinks

in the future, 2014.7 (not on the master yet) will have state.sls_id eracksdev supervisor-symlinks

then do:

sudo docker commit $(sudo docker ps -aq | head -1)
sudo docker tag $(sudo docker images -q | head -1) phase2.5
sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -p 443:443 -h dev.eracks.com phase2.5 supervisord -c /etc/supervisor/supervisord.conf | tee >(aha > phase3-manual-docker-outfile.html)

from eracks11/:

sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -p 443:443 \
    -h dev.eracks.com -v /home/joe/eracks11/conf/etc/conf.d:/etc/supervisor/conf.d \
     eracksdev-phase1and2 | tee >(aha > phase3-manual-docker-outfile.html)

