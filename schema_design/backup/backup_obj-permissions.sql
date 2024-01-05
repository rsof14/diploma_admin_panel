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
-- Data for Name: objects_permissions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY public.objects_permissions (object, role_id, permission, strategy_type, id) FROM stdin;
Strategy	3864be7b-1432-4111-9056-5f7fc3ba8fb9	r	Регламентная	9072e690-4404-444b-8d36-9a5410b6f0df
Strategy	3864be7b-1432-4111-9056-5f7fc3ba8fb9	r	Индивидуальная	9e2d42a0-90fe-475d-bdb4-56eceecf4fed
Strategy	b7eb8dea-bf52-49df-aeba-ab716fad29bb	r	Регламентная	3e3aa11c-f772-4d39-8a69-cf545fddcf91
Strategy	b7eb8dea-bf52-49df-aeba-ab716fad29bb	r	Индивидуальная	34e335bc-d31d-4fdf-8930-88e603d9b8b8
Strategy	4773b77e-2637-496d-a86b-6e91279b0128	r	Регламентная	91e3dadb-5f3f-4c8f-a3a9-96bc7649cdd2
Strategy	d02f84a9-bc73-4f7f-9107-26484e449943	r	Регламентная	a85bcb28-6223-4df6-87ef-c70f5638b659
Strategy	d02f84a9-bc73-4f7f-9107-26484e449943	r	Индивидуальная	7e296021-ea43-4d6a-94c6-3e89ec5456a8
Strategy	8086f599-8822-4302-9b3e-cb14018af3de	rwad	Регламентная	37e8a212-632a-45c5-bf52-aab573baccb2
Strategy	8086f599-8822-4302-9b3e-cb14018af3de	rwad	Индивидуальная	b8d2e6f1-1ded-40cc-a134-19b652412a85
RiskProfile	3864be7b-1432-4111-9056-5f7fc3ba8fb9	r	NULL	8eda897a-e668-45ea-8e8e-1721aa32dcd5
RiskProfile	b7eb8dea-bf52-49df-aeba-ab716fad29bb	r	NULL	b8cd83ba-a0a1-4bb3-8280-bc2f20d80ad6
RiskProfile	4773b77e-2637-496d-a86b-6e91279b0128	r	NULL	3e53b81a-1f85-4bcf-9870-edffd70b0ed1
RiskProfile	d02f84a9-bc73-4f7f-9107-26484e449943	r	NULL	e3df5f0d-1c0a-48c5-a4c7-9d63f09a95a1
RiskProfile	8086f599-8822-4302-9b3e-cb14018af3de	rwa	NULL	8c3da61b-7da1-480b-9e16-557916d53946
Asset	3864be7b-1432-4111-9056-5f7fc3ba8fb9	r	NULL	0ba2c10c-8ae4-4948-b6bb-f5442818a946
Asset	b7eb8dea-bf52-49df-aeba-ab716fad29bb	r	NULL	1853c54d-802b-48b4-998d-cb11144f3614
Asset	4773b77e-2637-496d-a86b-6e91279b0128	r	NULL	ed699cbf-9b77-4052-9194-8cd84c51d933
Asset	d02f84a9-bc73-4f7f-9107-26484e449943	r	NULL	8a5e7bb6-69ae-4a45-95a8-be6656ff96df
Asset	8086f599-8822-4302-9b3e-cb14018af3de	rwa	NULL	064594c9-0350-49e3-8dbc-5de62a895c37
Customer	3864be7b-1432-4111-9056-5f7fc3ba8fb9	r	NULL	f0afc545-c1bf-4613-8209-d84a6a35ea44
Customer	d02f84a9-bc73-4f7f-9107-26484e449943	r	NULL	89ea279d-7655-412f-9199-a426e6cd2eb1
Customer	8086f599-8822-4302-9b3e-cb14018af3de	rwad	NULL	66b657f2-6717-45fa-af30-3832e5663bd4
Portfolio	3864be7b-1432-4111-9056-5f7fc3ba8fb9	rw	NULL	3cebaadf-a3cf-4d68-836e-8ab6056976f2
Portfolio	b7eb8dea-bf52-49df-aeba-ab716fad29bb	r	NULL	dad017f8-0f36-4e9b-95d3-fce67da5ad60
Portfolio	8086f599-8822-4302-9b3e-cb14018af3de	rwad	NULL	0e136507-d9b6-400c-9770-16476d8d7ca0
Operations	3864be7b-1432-4111-9056-5f7fc3ba8fb9	e	NULL	60474015-a28d-406f-8389-51cda30708b3
RiskCalculation	b7eb8dea-bf52-49df-aeba-ab716fad29bb	e	NULL	4c4e6820-a21f-4c50-a9f2-e7c5f3cdf9eb
\.


--
-- PostgreSQL database dump complete
--

