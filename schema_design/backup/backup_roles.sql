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
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.roles (id, name) FROM stdin;
3864be7b-1432-4111-9056-5f7fc3ba8fb9	Управляющий
b7eb8dea-bf52-49df-aeba-ab716fad29bb	Риск-менеджер
8086f599-8822-4302-9b3e-cb14018af3de	Сотрудник бэк-офиса
4773b77e-2637-496d-a86b-6e91279b0128	Аналитик
d02f84a9-bc73-4f7f-9107-26484e449943	Руководство
\.


--
-- PostgreSQL database dump complete
--

