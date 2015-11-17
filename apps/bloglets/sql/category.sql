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
-- Name: bloglet_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eracks
--

SELECT pg_catalog.setval('bloglet_category_id_seq', 1, true);


--
-- Data for Name: bloglet_category; Type: TABLE DATA; Schema: public; Owner: eracks
--

INSERT INTO bloglet_category (id, title, slug, create_date, update_date, published) VALUES (1, 'eRacks News', 'eracks-news', '2009-01-05 22:32:21.932779+00', '2009-01-05 22:32:21.932821+00', true);


--
-- PostgreSQL database dump complete
--

