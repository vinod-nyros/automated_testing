# First, either create the eracks user, or if you already have a db, rename current db to eracks_old

# joe@dev:~/eracks11/scripts/db$ sudo su - postgres
# postgres@dev:~$ psql
# ...
#
# create user eracks with unencrypted password 'Wav3lets9';
#
# or
#
# create user eracks;
# alter user eracks unencrypted password 'Wav3lets9';
#
# or if you already have a db:
#
# postgres=# alter database eracksdb rename to eracksdb_old;


# also, ensure no other tasks are accessing pg - 
# SELECT * FROM pg_stat_activity;

# and kill as needed.

# Now, create new eracks db
# create database eracksdb owner eracks;

# Now, update comments appropriately:
# postgres=# comment ON database eracksdb is 'Copy of eRacks Production Database for dev';
# postgres=# comment ON database eracksdb_old is 'Old Copy of eRacks Production Database for dev';

# You can do \l+ to verify.

# Now do import from prod:

sudo -u joe ssh -c blowfish eracks.com 'sudo -u postgres pg_dump eracksdb | bzip2 -c ' | bzcat | sudo -u postgres psql eracksdb

