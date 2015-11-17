# Copyright 2014 Joseph Wolff & eRacks Systems

from ubuntu:trusty

maintainer Joseph Wolff, joe@eracks.com


# install user joe
RUN useradd -ms /bin/zsh joe
WORKDIR /home/joe/
ENV HOME /home/joe


ENV TERM linux
#dont: ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
	build-essential git \
	python python-dev python-setuptools \
	python-software-properties software-properties-common \
	mc arj p7zip xz-utils mercurial \
	libxslt1-dev libxml2-dev zlib1g-dev \
	memcached \
	python-psycopg2 \
	postgresql postgresql-plpython-9.3 \
	tidy \
	npm
# supervisor

run easy_install pip

RUN apt-add-repository -y ppa:gunicorn/ppa
RUN apt-get install -y gunicorn

RUN add-apt-repository -y ppa:nginx/stable
#run apt-get install -y sqlite3
run apt-get install -y nginx

RUN npm install stylus -g

#ADD eracks11 /home/joe/eracks11
#VOLUME /home/joe/eracks11:/home/joe/eracks11
VOLUME /home/joe/eracks11
#RUN git clone https://github.com/jowolf/eracks11.git

# setup all the configfiles
#run echo "daemon off;" >> /etc/nginx/nginx.conf
#run rm /etc/nginx/sites-enabled/default
#run ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
#run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/

ADD requirements.txt /home/joe/

RUN pip install -r requirements.txt

WORKDIR /home/joe/eracks11


# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
#run django-admin.py startproject website /home/docker/code/app/ 

#ENTRYPOINT PYTHONPATH=apps python manage.py 
ENTRYPOINT /bin/bash

expose 80 8080 22

#cmd ["supervisord", "-n"]
