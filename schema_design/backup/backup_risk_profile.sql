--
-- PostgreSQL database dump
--

-- Dumped from database version 13.12 (Debian 13.12-1.pgdg120+1)
-- Dumped by pg_dump version 13.12 (Debian 13.12-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: risk_profile; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.risk_profile (name, max_var) FROM stdin;
Умеренный	0.1
Консервативный	0.15
Рациональный	0.3
Агрессивный	1.2
\.


--
-- PostgreSQL database dump complete
--

