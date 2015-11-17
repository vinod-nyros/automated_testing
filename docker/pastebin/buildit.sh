# phase 1: docker build from phusion base image
# phase 2: salt it with eracksdev
# phase 3: db
# phase 4: run with restart

# requires:  docker aha elinks (to view result files)
# apt-get -y install aha elinks
# (docker 1.2.x requires PPA as of Oct 2014 - JJW)
#
# TERM=linux elinks phase1..

sudo docker build -t eracksdev-phase1 . | tee >(aha > phase1-docker-outfile.html) && \
sudo docker run -it -p 80:80 -p 8080:8080 -p 2222:22 -h dev.eracks.com $(sudo docker images -q |head -1) salt-minion -l debug \
  | tee >(aha > phase2-salt-log.html) && \

rm phase2-salt-log.html && \
sudo docker run -it -p 80:80 -p 8080:8080 -p 2222:22 -h dev.eracks.com eracksdev-phase1 salt-minion -l debug | tee >(aha > phase2-salt-log.html)

sudo docker commit -a joe -m eracksdev-phase2 $(sudo docker ps -aq |head -1)

sudo docker tag $(sudo docker images -q |head -1) eracksdev-phase2

sudo docker run -it -p 80:80 -p 8080:8080 -p 2222:22 -h dev.eracks.com eracksdev-phase2 /bin/bash

sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -v /home/joe/pgdump:/home/dev/pgdump -h dev.eracks.com newtesting supervisord -c /etc/supervisor/supervisord.conf

run pg unpack!


sudo docker build -t eracksdev-phase1 . | tee >(aha > phase1-docker-outfile.html) && \
sudo docker run -it -p 80:80 -p 8080:8080 -p 2222:22 -h dev.eracks.com eracksdev-phase1 salt-minion -l debug | tee >(aha > phase2-salt-log.html)


Phase 3:

Postgres examples:
psql -d eracksdb -U eracks -h 127.0.0.1 -c \\dt

echo \\l | sudo -u postgres psql 

Load:

sudo su - postgres -c bunzip2 -t pgdump/pgdump-140707.bz2 | psql 



# Handy one-liners:

apt-get install -y openssh-server && mkdir -p /var/run/sshd && sudo /usr/sbin/sshd -D


# new

sudo docker run -it -p 80:80 -p 8080:8080 -p 8000:8000 -p 2222:22 -p 443:443 -h dev.eracks.com eracksdev-phase123

