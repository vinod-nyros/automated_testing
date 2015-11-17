# 8/29/15 Saltified prerequisites for requirements.txt - JJW

## These first two are set in the command line in salt-requirements.sh:
{% set cwd      = pillar.master.file_root %}
{% set me       = pillar.master.pillar_root %}
{% set project  = salt['file.dirname'](cwd) %}


## Clean up possible leftover cruft, ensure certain packages not present:

django-haystack-pkg-removed:
  pkg.removed:
    - name: django-haystack

# can't have two of the same ID, can't have two xxx.removed states.  Yuk.
#django-haystack-pip-removed:
#  pip.removed:
#    - name: django-haystack

# really need ensure_removed, or ensure_python_removed - start with pkg, then pip, then manual..
#django-haystack.egg:
  #file: absent

# commenting out, not idemoptent - returns False if already not present
#gnupg:
#  pip.removed
#
#django-admin-tools:
#  pip.removed


## Ensure virtualenv present, other dependent packages, install my virtualenv & requirements

my-packages:
  pkg:
    - installed
    - names:
      - python-virtualenv
      - mercurial
      - libxml2-dev
      - libxslt-dev
      - zlib1g-dev
      - libjpeg-dev  # for Pillow
      - python-psycopg2  # this is outside the venv, so need to turn on system_site_packages
      - npm  # for stylus, bower, (and possibly coffeescript)
      - chromium-chromedriver
      # todo, set up with Salt:
      #- xvfb
      #- firefox
      #- chrome

{{ cwd }}/env:
  virtualenv.managed:
    - cwd: {{ cwd }}
    - user: {{ me }}
    #- system_site_packages: False
    - system_site_packages: True
    - requirements: requirements.txt  # salt://REQUIREMENTS.txt
    - require:
      - pkg: django-haystack-pkg-removed
      - pkg: my-packages


## Djide permissions

{{ cwd }}/env/src/django-ide/djide/metafiles:
  file.directory:
    - user: {{ me }}
    - mode: 0777
    - require:
      - virtualenv: {{ cwd }}/env


## Node.js symlink for Ubuntu

/usr/local/bin/node:
  file.symlink:
    - target: /usr/bin/nodejs


## Stylus

stylus:
  npm.installed:
    - require:
      - pkg: npm
      - file: /usr/local/bin/node


## Bower

bower:
  npm.installed:
    - require:
      - pkg: npm
      - file: /usr/local/bin/node

magnific-popup:
  bower.installed:
    - dir: {{ cwd }}
    - require:
      - npm: bower

# The remainder of the packages are all now in requirements.txt


## post-install setup - really only needs to be run the 1st time:

compilethemes:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py compilethemes

collectstatic:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py collectstatic --link --noinput

update_index:
  cmd.run:
    - cwd: {{ project }}
    - name: |
        . conf/env/bin/activate
        ./manage.py update_index

