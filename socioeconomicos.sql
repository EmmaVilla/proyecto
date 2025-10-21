--
-- PostgreSQL database dump
--

\restrict s3JusRqfa0zNTOJR0XimXE2qMrisQLfyLGJ6PURpNyCG8UTNCJkW8lVAAkjsIuM

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: candidatos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.candidatos (
    id integer NOT NULL,
    nombre text,
    email text,
    password text,
    fecha_registro timestamp without time zone,
    rol character varying(50),
    CONSTRAINT candidatos_rol_check CHECK (((rol)::text = ANY ((ARRAY['admin'::character varying, 'candidato'::character varying])::text[])))
);


ALTER TABLE public.candidatos OWNER TO postgres;

--
-- Name: candidatos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.candidatos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.candidatos_id_seq OWNER TO postgres;

--
-- Name: candidatos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.candidatos_id_seq OWNED BY public.candidatos.id;


--
-- Name: datos_socioeconomicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datos_socioeconomicos (
    candidato_id integer,
    situacion_familiar text,
    ingresos text,
    gastos text,
    situacion_laboral text,
    educacion text,
    vivienda text,
    referencias text,
    antecedentes text
);


ALTER TABLE public.datos_socioeconomicos OWNER TO postgres;

--
-- Name: documentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documentos (
    id integer NOT NULL,
    candidato_id integer,
    nombre_archivo text,
    ruta text,
    fecha_subida timestamp without time zone
);


ALTER TABLE public.documentos OWNER TO postgres;

--
-- Name: documentos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documentos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documentos_id_seq OWNER TO postgres;

--
-- Name: documentos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documentos_id_seq OWNED BY public.documentos.id;


--
-- Name: etapas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.etapas (
    candidato_id integer,
    estudio_completo boolean,
    documentos_completos boolean,
    api_consulta_completa boolean,
    pdf_generado boolean
);


ALTER TABLE public.etapas OWNER TO postgres;

--
-- Name: candidatos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidatos ALTER COLUMN id SET DEFAULT nextval('public.candidatos_id_seq'::regclass);


--
-- Name: documentos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos ALTER COLUMN id SET DEFAULT nextval('public.documentos_id_seq'::regclass);


--
-- Data for Name: candidatos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.candidatos (id, nombre, email, password, fecha_registro, rol) FROM stdin;
10	juan perez prado	emmanuel.v@acheme.com.mx	12345	2025-10-20 09:38:36.180599	candidato
11	emmanuelvc	emmanuel@gmail.com	12345	2025-10-20 10:39:28.018671	admin
\.


--
-- Data for Name: datos_socioeconomicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datos_socioeconomicos (candidato_id, situacion_familiar, ingresos, gastos, situacion_laboral, educacion, vivienda, referencias, antecedentes) FROM stdin;
\.


--
-- Data for Name: documentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documentos (id, candidato_id, nombre_archivo, ruta, fecha_subida) FROM stdin;
\.


--
-- Data for Name: etapas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.etapas (candidato_id, estudio_completo, documentos_completos, api_consulta_completa, pdf_generado) FROM stdin;
\.


--
-- Name: candidatos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.candidatos_id_seq', 11, true);


--
-- Name: documentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documentos_id_seq', 2, true);


--
-- Name: candidatos candidatos_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidatos
    ADD CONSTRAINT candidatos_email_key UNIQUE (email);


--
-- Name: candidatos candidatos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidatos
    ADD CONSTRAINT candidatos_pkey PRIMARY KEY (id);


--
-- Name: documentos documentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos
    ADD CONSTRAINT documentos_pkey PRIMARY KEY (id);


--
-- Name: datos_socioeconomicos datos_socioeconomicos_candidato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datos_socioeconomicos
    ADD CONSTRAINT datos_socioeconomicos_candidato_id_fkey FOREIGN KEY (candidato_id) REFERENCES public.candidatos(id);


--
-- Name: documentos documentos_candidato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos
    ADD CONSTRAINT documentos_candidato_id_fkey FOREIGN KEY (candidato_id) REFERENCES public.candidatos(id);


--
-- Name: etapas etapas_candidato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.etapas
    ADD CONSTRAINT etapas_candidato_id_fkey FOREIGN KEY (candidato_id) REFERENCES public.candidatos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict s3JusRqfa0zNTOJR0XimXE2qMrisQLfyLGJ6PURpNyCG8UTNCJkW8lVAAkjsIuM

