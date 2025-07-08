--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-05-20 11:03:12

--SET statement_timeout = 0;
--SET lock_timeout = 0;
--SET idle_in_transaction_session_timeout = 0;
--SET transaction_timeout = 0;
--SET client_encoding = 'UTF8';
--SET standard_conforming_strings = on;
--SELECT pg_catalog.set_config('search_path', '', false);
--SET check_function_bodies = false;
--SET xmloption = content;
--SET client_min_messages = warning;
--SET row_security = off;

--
-- TOC entry 6 (class 2615 OID 16412)
-- Name: Auth; Type: SCHEMA; Schema: -; Owner: postgres
--

--CREATE SCHEMA "Auth";


--ALTER SCHEMA "Auth" OWNER TO postgres;

--SET default_tablespace = '';

--SET default_table_access_method = heap;

--
-- TOC entry 221 (class 1259 OID 16422)
-- Name: character; Type: TABLE; Schema: Auth; Owner: postgres
--

--CREATE TABLE "Auth"."character" (
--    character_id integer NOT NULL,
--    character_name text NOT NULL,
--    biography text,
--    color text NOT NULL,
--    user_id integer NOT NULL
--);


--ALTER TABLE "Auth"."character" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16421)
-- Name: character_character_id_seq; Type: SEQUENCE; Schema: Auth; Owner: postgres
--

--ALTER TABLE "Auth"."character" ALTER COLUMN character_id ADD GENERATED ALWAYS AS IDENTITY (
--    SEQUENCE NAME "Auth".character_character_id_seq
--    START WITH 1
--    INCREMENT BY 1
--    NO MINVALUE
--    NO MAXVALUE
--    CACHE 1
--);


--
-- TOC entry 219 (class 1259 OID 16414)
-- Name: user; Type: TABLE; Schema: Auth; Owner: postgres
--

--CREATE TABLE "Auth"."user" (
--    user_id integer NOT NULL,
--    nickname text NOT NULL,
--    email text NOT NULL,
--    password text NOT NULL,
--    master_status boolean NOT NULL
--);


--ALTER TABLE "Auth"."user" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16413)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: Auth; Owner: postgres
--

--ALTER TABLE "Auth"."user" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
--    SEQUENCE NAME "Auth".user_user_id_seq
--    START WITH 1
--    INCREMENT BY 1
--    NO MINVALUE
--    NO MAXVALUE
--    CACHE 1
--);


--
-- TOC entry 4854 (class 0 OID 16422)
-- Dependencies: 221
-- Data for Name: character; Type: TABLE DATA; Schema: Auth; Owner: postgres
--

--COPY "Auth"."character" (character_id, character_name, biography, color, user_id) FROM stdin;
--\.


--
-- TOC entry 4852 (class 0 OID 16414)
-- Dependencies: 219
-- Data for Name: user; Type: TABLE DATA; Schema: Auth; Owner: postgres
--

--COPY "Auth"."user" (user_id, nickname, email, password, master_status) FROM stdin;
--\.


--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 220
-- Name: character_character_id_seq; Type: SEQUENCE SET; Schema: Auth; Owner: postgres
--

--SELECT pg_catalog.setval('"Auth".character_character_id_seq', 1, false);


--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 218
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: Auth; Owner: postgres
--

--SELECT pg_catalog.setval('"Auth".user_user_id_seq', 1, false);


--
-- TOC entry 4704 (class 2606 OID 16428)
-- Name: character character_pkey; Type: CONSTRAINT; Schema: Auth; Owner: postgres
--

--ALTER TABLE ONLY "Auth"."character"
--    ADD CONSTRAINT character_pkey PRIMARY KEY (character_id);


--
-- TOC entry 4702 (class 2606 OID 16420)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: Auth; Owner: postgres
--

--ALTER TABLE ONLY "Auth"."user"
--    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4705 (class 2606 OID 16429)
-- Name: character none; Type: FK CONSTRAINT; Schema: Auth; Owner: postgres
--

--ALTER TABLE ONLY "Auth"."character"
--    ADD CONSTRAINT "none" FOREIGN KEY (user_id) REFERENCES "Auth"."user"(user_id) NOT VALID;


-- Completed on 2025-05-20 11:03:12

--
-- PostgreSQL database dump complete
--

