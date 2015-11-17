--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: obdjects_meta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eracks
--

SELECT pg_catalog.setval('obdjects_meta_id_seq', 2, true);


--
-- Data for Name: obdjects_meta; Type: TABLE DATA; Schema: public; Owner: eracks
--

INSERT INTO obdjects_meta (id, title, name, http_equiv, scheme, content, create_date, update_date, published) VALUES (1, 'My eRacks Description', 'description', '', '', 'eRacks - the best Open Source Rackmount Servers on the net', '2009-01-09 22:03:30.282883+00', '2009-01-09 22:05:56.767597+00', true);
INSERT INTO obdjects_meta (id, title, name, http_equiv, scheme, content, create_date, update_date, published) VALUES (2, 'My eRacks Keywords', 'keywords', '', '', 'Rack mount servers, rackmount, servers, Open Source, Penguin, Dell, Pogo Linux, Rack, NAS, DAS, SAS, SATA', '2009-01-09 22:07:06.285149+00', '2009-01-09 22:07:06.285196+00', true);


--
-- PostgreSQL database dump complete
--

