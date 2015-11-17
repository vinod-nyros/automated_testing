#!/bin/bash

# get the path from current dir to this script (may just be '.')
DIR=`dirname $0`"/.."

# echo $DIR

# yes, we need to add both $DIR _and_ $DIR/../ because that is the closest way to match how manage.py works with imports.
# This gives us the greatest compatibility and the least amount of problems between running scripts and the site.
#echo env PYTHONPATH=$DIR/apps/:$DIR/../:$DIR DJANGO_SETTINGS_MODULE=django_eracks.settings python "$@"
env PYTHONPATH=$DIR/apps/:$DIR/../:$DIR DJANGO_SETTINGS_MODULE=eracks.settings python "$@"

