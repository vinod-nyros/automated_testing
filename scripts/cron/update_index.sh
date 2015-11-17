#!/bin/sh

# Symlink this file into /etc/cron.daily or hourly without the .sh

echo Running: $0

# following line is so can be run from cron via symlink
cd `dirname $(readlink -f $0)`

echo 'Updating whoosh index'
id
pwd

cd ../../eracks

pwd

../manage.py rebuild_index --noinput
chmod -R g+w whoosh_index/
chown -R joe:www-data whoosh_index/


# now done by sql 2/21/14 JW
#
#./manage.py clearsessions -v3
