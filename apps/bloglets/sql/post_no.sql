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
-- Name: bloglet_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eracks
--

SELECT pg_catalog.setval('bloglet_post_id_seq', 9, true);


--
-- Data for Name: bloglet_post; Type: TABLE DATA; Schema: public; Owner: eracks
--

INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (1, 'Fedora 10 reviews', 'fedora-10-reviews', '2009-01-05 22:34:36.724526+00', '2009-01-05 22:34:36.724564+00', '2009-01-05 22:34:36.724584+00', '<font color="red">News</font>: Fedora 10 gets 
<a href="http://www.theregister.co.uk/2008/11/25/fedora_10_review/">great reviews</a>!
<p>Significant price drops in Hard Drives!</p>
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (5, 'eRacks TWINGUARD', 'eracks-twinguard', '2009-01-05 10:00:00+00', '2009-01-05 23:15:12.717932+00', '2009-01-06 00:16:37.54301+00', '<b><a href="http://eracks.com/products/Firewall%20Servers/config?sku=TWINGUARD">eRacks/TWINGUARD</a></b><br>
Failover fully-redundant firewall system in one 1U chassis.
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (9, 'eRacks/STUBBY', 'eracksstubby', '2009-03-04 03:52:59+00', '2009-03-04 03:52:53.212106+00', '2009-03-05 00:20:16.24334+00', '<b><a href="/products/shallow">eRacks/STUBBY</a>
</b>
<a href="/product/stubby"><img src="/images/categories/shallow/stubby_100.jpg" alt="Short depth rackmount" title="eRacks/STUBBY" border="0" height="64" width="100"></a>
<br>
8.75 inch short-depth rackmount server<br>
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (8, 'eRacks Netbooks!', 'eracks-netbooks', '2009-01-05 23:19:23+00', '2009-01-05 23:19:23.782701+00', '2009-03-05 00:21:10.040302+00', '<a href="/products/netbooks">eRacks Netbooks!</a>
</b>
<a href="/products/netbooks"><img src="/images/categories/netbooks/cumulus_colors_xsmall.jpg" alt="" title="eRacks/CUMULUS" border="0" height="69" width="100"></a>
<br>
with Ubuntu and Fedora Linux<br>
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (7, 'eRacks i7 DESK', 'eracks-i7-desk', '2009-01-05 23:18:51+00', '2009-01-05 23:18:51.071072+00', '2009-03-05 00:22:01.452285+00', '<a href="/products/Desktops/config?sku=i7DESK">eRacks/i7DESK:</a>
<br>
Intel® Core i7 Desktop<br>
<a href="/products/Desktops/config?sku=i7DESK"><img src="/images/categories/desktops/intelcorei7_60.jpg" alt="" title="" border="0" height="73" width="60">', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (2, 'eRacks STUDIO OSDAW', 'eracks-studio-osdaw', '2009-01-05 13:00:00+00', '2009-01-05 22:42:42.865908+00', '2009-03-05 00:25:37.239258+00', '<b>
 <a href="http://eracks.com/products/Quiet%20Systems/config?sku=STUDIO">eRacks/STUDIO</a>
</b>
<a href="http://eracks.com/products/Quiet%20Systems/config?sku=STUDIO">
<img src="/images/categories/quiet/pedalup.png" alt="" title="eRacks/STUDIO" border="0" height="29" width="30">
</a>
Open Source Digital Audio Workstation', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (3, 'Dedicated Hosting Available', 'dedicated-hosting-available', '2009-01-05 12:00:00+00', '2009-01-05 22:43:40.311783+00', '2009-03-05 00:26:40.717184+00', '<b>Dedicated Hosting now Available!</b><br>
<a href="http://eracks.com/press/071207"><img src="/images/press/erackshostinglogo_100.jpg" alt="" title="eRacksHosting.com" border="0" height="51" width="100"></a><br>
<b><a href="http://erackshosting.com">eRacksHosting</a></b>
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (4, 'Do You Ubuntu?', 'do-you-ubuntu', '2009-01-05 11:00:00+00', '2009-01-05 23:14:23.162045+00', '2009-03-05 00:28:15.497404+00', '<b>eRacks Canonical Partnership announced!</b><p>
<a href="http://eracks.com/press/070216"><img src="/images/categories/desktops/ubuntu_70.jpg" alt="" title="Do you Ubuntu?" border="0" height="70" width="70"></a>
<br>
<b><a href="http://eracks.com/products/Desktops/">Do you Ubuntu?</a></b>
', 1, true);
INSERT INTO bloglet_post (id, title, slug, pub_date, create_date, update_date, body, author_id, published) VALUES (6, 'EFF Donations', 'eff-donations', '2009-01-05 09:00:00+00', '2009-01-05 23:15:58.53197+00', '2009-03-05 00:28:49.77486+00', '<p>
<a href="http://eff.org" target="new"><img src="/images/logos/eff-logo-s.png" border="0"></a><br>
 eRacks 
<a href="http://eracks.com/press/050201">matches donations</a> to EFF!
', 1, true);


--
-- PostgreSQL database dump complete
--

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
-- Name: bloglet_post_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eracks
--

SELECT pg_catalog.setval('bloglet_post_categories_id_seq', 19, true);


--
-- Data for Name: bloglet_post_categories; Type: TABLE DATA; Schema: public; Owner: eracks
--

INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (1, 1, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (9, 8, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (10, 7, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (15, 6, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (16, 5, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (17, 4, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (18, 3, 1);
INSERT INTO bloglet_post_categories (id, post_id, category_id) VALUES (19, 2, 1);


--
-- PostgreSQL database dump complete
--

