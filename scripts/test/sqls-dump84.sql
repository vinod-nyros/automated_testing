--
-- PostgreSQL database dump
--

SET client_encoding = 'LATIN1';
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = true;

--
-- Name: sqls; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sqls (
    id serial NOT NULL,
    description character varying(160),
    thesql text
);


ALTER TABLE public.sqls OWNER TO postgres;

--
-- Name: sqls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('sqls', 'id'), 39, true);


--
-- Data for Name: sqls; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO sqls (id, description, thesql) VALUES (17, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (28, 'Create techdata table', '');
INSERT INTO sqls (id, description, thesql) VALUES (11, 'Create table', 'create table <dtml-var table> (id serial, col1 int, col2 varchar(80)) where <dtml-sqltest pkey column="id" type="int">;');
INSERT INTO sqls (id, description, thesql) VALUES (22, 'Create mfrs table', '--drop table mfrs;
create table mfrs 
 (id serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (20, 'Generic sql', 'select obj_description (o) from (select oid as o from testtable) foo;
');
INSERT INTO sqls (id, description, thesql) VALUES (3, 'A Test SQL', 'select * from pg_class');
INSERT INTO sqls (id, description, thesql) VALUES (5, 'another test SQL', 'select * from pg_views');
INSERT INTO sqls (id, description, thesql) VALUES (14, 'add new table', 'create table blah (myid serial, name text, description text);');
INSERT INTO sqls (id, description, thesql) VALUES (27, 'Get Columns', 'select column_name, '','' from information_schema.columns where table_name = ''techdata''
order by ordinal_position;');
INSERT INTO sqls (id, description, thesql) VALUES (18, 'Test Insert Into from sql', 'insert into testtable select * from testtable where id=123');
INSERT INTO sqls (id, description, thesql) VALUES (19, 'Boolean test', 'create table testtable (id serial primary key, name text, checkbox bool)');
INSERT INTO sqls (id, description, thesql) VALUES (15, 'create purchases table', '[edit me out!]drop table purchases; 
create table purchases 
(id serial, 
 vendorid int, 
 partid int, 
 price float,
 ts timestamp default ''now'',
 dt timestamp default ''now''
);
insert into purchases default values;
');
INSERT INTO sqls (id, description, thesql) VALUES (33, 'Audit trail for table record', 'select a.*, c.relname 
from audit a, pg_class c
where a.relid = 82166 
 and c.oid = a.relid
 and a.pkey = 43
order by created desc
limit 10; 
');
INSERT INTO sqls (id, description, thesql) VALUES (21, 'Create vendors table', '--drop table vendors;
create table vendors 
 (id serial primary key, 
  name varchar (80),  
  component varchar (80),
  contact varchar (80),
  salesphone varchar (80),
  acctnum varchar (20),	
  fax varchar (20),
  acctphone varchar (80),
  website varchar (160),
  login	varchar (80),
  rmaphone varchar (80),
  email varchar (80),
  terms varchar (20),
  amount float,
  product varchar (80),
  shipcutoff varchar (20),
  willcallcutoff varchar (20),
  ordmethod varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (16, 'Create Components Table (old)', 'create table components 
 (id serial, 
  name varchar(80), 
  sku varchar(20), 
  mfrid int, 
  mfrsku varchar(20), 
  msrp float, 
  upc varchar(40), 
  created timestamp default now()
)
');
INSERT INTO sqls (id, description, thesql) VALUES (24, 'Create phones table', '--drop table phones;
create table phones 
 (phoneid serial primary key,
  phone varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (23, 'Create emails table', '--drop table emails;
create table emails 
 (emailid serial primary key,
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (38, 'Create powersupplies table', '--drop table powersupplies;
Create table powersupplies
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  watts int,
  ff int,
  pfc bool,
  voltslo int,  -- PG8!
  voltshi int,
  universal bool,
  switch bool,
  lownoise bool
) inherits (components);

alter table powersupplies add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');
INSERT INTO sqls (id, description, thesql) VALUES (32, 'Create audit table', 'drop table audit;
create table audit 
 (id serial primary key, relid int, pkey int, type varchar, event varchar, 
  before varchar, after varchar, td varchar,  created timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (25, 'Create contactemails table', '--drop table contactemails;
create table contactemails 
 (contactemailid serial primary key,
  contactid int,
  emailid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (26, 'Create contactphones table', '--drop table contactphones;
create table contactphones 
 (contactphoneid serial primary key,
  contactid int,
  phoneid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (39, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (30, 'Create contacts table', '--drop table contacts;
create table contacts 
 (contactid serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (31, 'select prices', 'select *, vendorprices (c.id) from components c;');
INSERT INTO sqls (id, description, thesql) VALUES (35, 'Show components with (inherited) table', 'SELECT p.relname, c.*
FROM components c, pg_class p
WHERE c.tableoid = p.oid;');
INSERT INTO sqls (id, description, thesql) VALUES (29, 'Create components table', '--drop table components;
Create table components 
 (id serial primary key,
  sku character varying(30),
  name character varying(80),
  description varchar (250),
  mfrid int references mfrs (id),
  mfrsku character varying(30),
  model varchar (60),
  msrp float,
  upc character varying(60),
  created timestamp default now()
 );
');
INSERT INTO sqls (id, description, thesql) VALUES (34, 'Create chasses table', '--drop table chasses;
Create table chasses
 (us int,
-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  mobobays int,
-- powersupply dimensions, PG8 only!
-- mobotypeid int references mobotypes,
  bay5s int,
  bay3s int,
-- front usb? CF slots? psbay?
  hds int,
  rmhds int
) inherits (components);

alter table chasses add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id)');
INSERT INTO sqls (id, description, thesql) VALUES (37, 'Create motherboards table', '--drop table motherboards;
Create table motherboards
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  cputype varchar,
  acceptscpu varchar,  -- lo-hi range?  micron/die size?
  chipset varchar,
  ff int,  -- references formfactors or moboformfactors
  dimmslots int,
  serialports int,
  parallelports int,
  vgaonboard bool,  -- int?
  usbver int, -- 0,1,2
  usbports int,
  usbheaders int, -- the ones on the mobo that require a cable
  firewireports int,
  backplate int, -- references atxbackplates (id),
  memslots int, -- num slots
  memtypes int[],  -- references memtypes
  memspeedmin int, -- minimum memory speed required
  memspeedmax int, -- maximum memory speed required
  memcls int[], -- memory cls accepted - cl2, 2.5, 3
  notes varchar
) inherits (components);

alter table motherboards add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');
INSERT INTO sqls (id, description, thesql) VALUES (17, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (28, 'Create techdata table', '');
INSERT INTO sqls (id, description, thesql) VALUES (11, 'Create table', 'create table <dtml-var table> (id serial, col1 int, col2 varchar(80)) where <dtml-sqltest pkey column="id" type="int">;');
INSERT INTO sqls (id, description, thesql) VALUES (22, 'Create mfrs table', '--drop table mfrs;
create table mfrs 
 (id serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (20, 'Generic sql', 'select obj_description (o) from (select oid as o from testtable) foo;
');
INSERT INTO sqls (id, description, thesql) VALUES (3, 'A Test SQL', 'select * from pg_class');
INSERT INTO sqls (id, description, thesql) VALUES (5, 'another test SQL', 'select * from pg_views');
INSERT INTO sqls (id, description, thesql) VALUES (14, 'add new table', 'create table blah (myid serial, name text, description text);');
INSERT INTO sqls (id, description, thesql) VALUES (27, 'Get Columns', 'select column_name, '','' from information_schema.columns where table_name = ''techdata''
order by ordinal_position;');
INSERT INTO sqls (id, description, thesql) VALUES (18, 'Test Insert Into from sql', 'insert into testtable select * from testtable where id=123');
INSERT INTO sqls (id, description, thesql) VALUES (19, 'Boolean test', 'create table testtable (id serial primary key, name text, checkbox bool)');
INSERT INTO sqls (id, description, thesql) VALUES (15, 'create purchases table', '[edit me out!]drop table purchases; 
create table purchases 
(id serial, 
 vendorid int, 
 partid int, 
 price float,
 ts timestamp default ''now'',
 dt timestamp default ''now''
);
insert into purchases default values;
');
INSERT INTO sqls (id, description, thesql) VALUES (33, 'Audit trail for table record', 'select a.*, c.relname 
from audit a, pg_class c
where a.relid = 82166 
 and c.oid = a.relid
 and a.pkey = 43
order by created desc
limit 10; 
');
INSERT INTO sqls (id, description, thesql) VALUES (21, 'Create vendors table', '--drop table vendors;
create table vendors 
 (id serial primary key, 
  name varchar (80),  
  component varchar (80),
  contact varchar (80),
  salesphone varchar (80),
  acctnum varchar (20),	
  fax varchar (20),
  acctphone varchar (80),
  website varchar (160),
  login	varchar (80),
  rmaphone varchar (80),
  email varchar (80),
  terms varchar (20),
  amount float,
  product varchar (80),
  shipcutoff varchar (20),
  willcallcutoff varchar (20),
  ordmethod varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (16, 'Create Components Table (old)', 'create table components 
 (id serial, 
  name varchar(80), 
  sku varchar(20), 
  mfrid int, 
  mfrsku varchar(20), 
  msrp float, 
  upc varchar(40), 
  created timestamp default now()
)
');
INSERT INTO sqls (id, description, thesql) VALUES (24, 'Create phones table', '--drop table phones;
create table phones 
 (phoneid serial primary key,
  phone varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (23, 'Create emails table', '--drop table emails;
create table emails 
 (emailid serial primary key,
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (38, 'Create powersupplies table', '--drop table powersupplies;
Create table powersupplies
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  watts int,
  ff int,
  pfc bool,
  voltslo int,  -- PG8!
  voltshi int,
  universal bool,
  switch bool,
  lownoise bool
) inherits (components);

alter table powersupplies add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');
INSERT INTO sqls (id, description, thesql) VALUES (32, 'Create audit table', 'drop table audit;
create table audit 
 (id serial primary key, relid int, pkey int, type varchar, event varchar, 
  before varchar, after varchar, td varchar,  created timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (25, 'Create contactemails table', '--drop table contactemails;
create table contactemails 
 (contactemailid serial primary key,
  contactid int,
  emailid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (26, 'Create contactphones table', '--drop table contactphones;
create table contactphones 
 (contactphoneid serial primary key,
  contactid int,
  phoneid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (39, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (30, 'Create contacts table', '--drop table contacts;
create table contacts 
 (contactid serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (31, 'select prices', 'select *, vendorprices (c.id) from components c;');
INSERT INTO sqls (id, description, thesql) VALUES (35, 'Show components with (inherited) table', 'SELECT p.relname, c.*
FROM components c, pg_class p
WHERE c.tableoid = p.oid;');
INSERT INTO sqls (id, description, thesql) VALUES (29, 'Create components table', '--drop table components;
Create table components 
 (id serial primary key,
  sku character varying(30),
  name character varying(80),
  description varchar (250),
  mfrid int references mfrs (id),
  mfrsku character varying(30),
  model varchar (60),
  msrp float,
  upc character varying(60),
  created timestamp default now()
 );
');
INSERT INTO sqls (id, description, thesql) VALUES (34, 'Create chasses table', '--drop table chasses;
Create table chasses
 (us int,
-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  mobobays int,
-- powersupply dimensions, PG8 only!
-- mobotypeid int references mobotypes,
  bay5s int,
  bay3s int,
-- front usb? CF slots? psbay?
  hds int,
  rmhds int
) inherits (components);

alter table chasses add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id)');
INSERT INTO sqls (id, description, thesql) VALUES (37, 'Create motherboards table', '--drop table motherboards;
Create table motherboards
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  cputype varchar,
  acceptscpu varchar,  -- lo-hi range?  micron/die size?
  chipset varchar,
  ff int,  -- references formfactors or moboformfactors
  dimmslots int,
  serialports int,
  parallelports int,
  vgaonboard bool,  -- int?
  usbver int, -- 0,1,2
  usbports int,
  usbheaders int, -- the ones on the mobo that require a cable
  firewireports int,
  backplate int, -- references atxbackplates (id),
  memslots int, -- num slots
  memtypes int[],  -- references memtypes
  memspeedmin int, -- minimum memory speed required
  memspeedmax int, -- maximum memory speed required
  memcls int[], -- memory cls accepted - cl2, 2.5, 3
  notes varchar
) inherits (components);

alter table motherboards add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');
INSERT INTO sqls (id, description, thesql) VALUES (17, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (28, 'Create techdata table', '');
INSERT INTO sqls (id, description, thesql) VALUES (11, 'Create table', 'create table <dtml-var table> (id serial, col1 int, col2 varchar(80)) where <dtml-sqltest pkey column="id" type="int">;');
INSERT INTO sqls (id, description, thesql) VALUES (22, 'Create mfrs table', '--drop table mfrs;
create table mfrs 
 (id serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (20, 'Generic sql', 'select obj_description (o) from (select oid as o from testtable) foo;
');
INSERT INTO sqls (id, description, thesql) VALUES (3, 'A Test SQL', 'select * from pg_class');
INSERT INTO sqls (id, description, thesql) VALUES (5, 'another test SQL', 'select * from pg_views');
INSERT INTO sqls (id, description, thesql) VALUES (14, 'add new table', 'create table blah (myid serial, name text, description text);');
INSERT INTO sqls (id, description, thesql) VALUES (27, 'Get Columns', 'select column_name, '','' from information_schema.columns where table_name = ''techdata''
order by ordinal_position;');
INSERT INTO sqls (id, description, thesql) VALUES (18, 'Test Insert Into from sql', 'insert into testtable select * from testtable where id=123');
INSERT INTO sqls (id, description, thesql) VALUES (19, 'Boolean test', 'create table testtable (id serial primary key, name text, checkbox bool)');
INSERT INTO sqls (id, description, thesql) VALUES (15, 'create purchases table', '[edit me out!]drop table purchases; 
create table purchases 
(id serial, 
 vendorid int, 
 partid int, 
 price float,
 ts timestamp default ''now'',
 dt timestamp default ''now''
);
insert into purchases default values;
');
INSERT INTO sqls (id, description, thesql) VALUES (33, 'Audit trail for table record', 'select a.*, c.relname 
from audit a, pg_class c
where a.relid = 82166 
 and c.oid = a.relid
 and a.pkey = 43
order by created desc
limit 10; 
');
INSERT INTO sqls (id, description, thesql) VALUES (21, 'Create vendors table', '--drop table vendors;
create table vendors 
 (id serial primary key, 
  name varchar (80),  
  component varchar (80),
  contact varchar (80),
  salesphone varchar (80),
  acctnum varchar (20),	
  fax varchar (20),
  acctphone varchar (80),
  website varchar (160),
  login	varchar (80),
  rmaphone varchar (80),
  email varchar (80),
  terms varchar (20),
  amount float,
  product varchar (80),
  shipcutoff varchar (20),
  willcallcutoff varchar (20),
  ordmethod varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (16, 'Create Components Table (old)', 'create table components 
 (id serial, 
  name varchar(80), 
  sku varchar(20), 
  mfrid int, 
  mfrsku varchar(20), 
  msrp float, 
  upc varchar(40), 
  created timestamp default now()
)
');
INSERT INTO sqls (id, description, thesql) VALUES (24, 'Create phones table', '--drop table phones;
create table phones 
 (phoneid serial primary key,
  phone varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (23, 'Create emails table', '--drop table emails;
create table emails 
 (emailid serial primary key,
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (38, 'Create powersupplies table', '--drop table powersupplies;
Create table powersupplies
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  watts int,
  ff int,
  pfc bool,
  voltslo int,  -- PG8!
  voltshi int,
  universal bool,
  switch bool,
  lownoise bool
) inherits (components);

alter table powersupplies add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON powersupplies 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');
INSERT INTO sqls (id, description, thesql) VALUES (32, 'Create audit table', 'drop table audit;
create table audit 
 (id serial primary key, relid int, pkey int, type varchar, event varchar, 
  before varchar, after varchar, td varchar,  created timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (25, 'Create contactemails table', '--drop table contactemails;
create table contactemails 
 (contactemailid serial primary key,
  contactid int,
  emailid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (26, 'Create contactphones table', '--drop table contactphones;
create table contactphones 
 (contactphoneid serial primary key,
  contactid int,
  phoneid int,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (39, 'Create magazine table', 'drop table magazines;
create table magazines 
 (id serial primary key, name varchar(80), class varchar(20), method varchar(20), contact text, 
  subscribed bool, expires date, retention varchar(20), comments text,
  created timestamp not null default now(), modified timestamp not null default now());');
INSERT INTO sqls (id, description, thesql) VALUES (30, 'Create contacts table', '--drop table contacts;
create table contacts 
 (contactid serial primary key,
  name varchar (80),
  contact varchar (80),
  phone varchar (80),
  fax varchar (20),
  website varchar (160),
  email varchar (80),
  notes text,
  created timestamp not null default now(), modified timestamp not null default now()
);
');
INSERT INTO sqls (id, description, thesql) VALUES (31, 'select prices', 'select *, vendorprices (c.id) from components c;');
INSERT INTO sqls (id, description, thesql) VALUES (35, 'Show components with (inherited) table', 'SELECT p.relname, c.*
FROM components c, pg_class p
WHERE c.tableoid = p.oid;');
INSERT INTO sqls (id, description, thesql) VALUES (29, 'Create components table', '--drop table components;
Create table components 
 (id serial primary key,
  sku character varying(30),
  name character varying(80),
  description varchar (250),
  mfrid int references mfrs (id),
  mfrsku character varying(30),
  model varchar (60),
  msrp float,
  upc character varying(60),
  created timestamp default now()
 );
');
INSERT INTO sqls (id, description, thesql) VALUES (34, 'Create chasses table', '--drop table chasses;
Create table chasses
 (us int,
-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  mobobays int,
-- powersupply dimensions, PG8 only!
-- mobotypeid int references mobotypes,
  bay5s int,
  bay3s int,
-- front usb? CF slots? psbay?
  hds int,
  rmhds int
) inherits (components);

alter table chasses add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON chasses FOR EACH ROW EXECUTE PROCEDURE audit(id)');
INSERT INTO sqls (id, description, thesql) VALUES (37, 'Create motherboards table', '--drop table motherboards;
Create table motherboards
 (-- dims dimensions, PG8 only!
  h float,
  w float,
  d float,
  cputype varchar,
  acceptscpu varchar,  -- lo-hi range?  micron/die size?
  chipset varchar,
  ff int,  -- references formfactors or moboformfactors
  dimmslots int,
  serialports int,
  parallelports int,
  vgaonboard bool,  -- int?
  usbver int, -- 0,1,2
  usbports int,
  usbheaders int, -- the ones on the mobo that require a cable
  firewireports int,
  backplate int, -- references atxbackplates (id),
  memslots int, -- num slots
  memtypes int[],  -- references memtypes
  memspeedmin int, -- minimum memory speed required
  memspeedmax int, -- maximum memory speed required
  memcls int[], -- memory cls accepted - cl2, 2.5, 3
  notes varchar
) inherits (components);

alter table motherboards add foreign key (mfrid) references mfrs (id);

CREATE TRIGGER afterimage AFTER INSERT OR UPDATE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);

CREATE TRIGGER beforeimage BEFORE DELETE ON motherboards 
  FOR EACH ROW EXECUTE PROCEDURE audit(id);
');


--
-- PostgreSQL database dump complete
--

