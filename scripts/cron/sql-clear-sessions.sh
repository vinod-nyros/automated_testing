#!/usr/bin/env bash

echo Running: $0

time env PGPASSWORD=Wav3lets9 psql -h127.0.0.1 -p5432 -Ueracks eracksdb <<EOF
select count(*) from django_session where expire_date <now();
select pg_size_pretty(pg_total_relation_size('django_session'));
delete from django_session where expire_date <now();
VACUUM FULL django_session;
select pg_size_pretty(pg_total_relation_size('django_session'));
select count(*) from django_session where expire_date <now();
EOF
