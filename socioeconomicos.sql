--
-- PostgreSQL database dump
--

\restrict OLaSVIlz3lQ4DlvUz8LRbzv0Srhv5bLkQ2XqcELbrd6jka0HiUdB0Cu12Gp7n7h

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
    curp character varying(25),
    sexo character varying(10),
    ceclular character varying(15),
    tel_fijo character varying(15),
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
-- Name: salud; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.salud (
    id integer NOT NULL,
    candidato_id integer,
    enfermedad_actual text,
    servicio_medico text,
    ocupacion_actual character varying(100),
    escolaridad character varying(100),
    fuente_ingresos character varying(255),
    tiempo_trabajo character varying(100),
    ingreso_extra character varying(100)
);


ALTER TABLE public.salud OWNER TO postgres;

--
-- Name: salud_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.salud_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.salud_id_seq OWNER TO postgres;

--
-- Name: salud_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.salud_id_seq OWNED BY public.salud.id;


--
-- Name: vivienda; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vivienda (
    candidato_id integer,
    tipo_vivienda character varying(50),
    hombres_habitantes integer,
    mujeres_habitantes integer,
    total_habitantes integer,
    total_cuartos integer,
    dormitorios integer,
    material_piso character varying(100),
    material_techo character varying(100),
    material_paredes character varying(100),
    "tipo_ba¤o" character varying(100),
    tipo_drenaje character varying(100),
    tratamiento_basura character varying(100),
    obtencion_luz character varying(100),
    combustible_cocina character varying(100),
    estatus_casa character varying(100),
    id integer NOT NULL
);


ALTER TABLE public.vivienda OWNER TO postgres;

--
-- Name: vivienda_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vivienda_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vivienda_id_seq OWNER TO postgres;

--
-- Name: vivienda_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vivienda_id_seq OWNED BY public.vivienda.id;


--
-- Name: candidatos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.candidatos ALTER COLUMN id SET DEFAULT nextval('public.candidatos_id_seq'::regclass);


--
-- Name: documentos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos ALTER COLUMN id SET DEFAULT nextval('public.documentos_id_seq'::regclass);


--
-- Name: salud id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salud ALTER COLUMN id SET DEFAULT nextval('public.salud_id_seq'::regclass);


--
-- Name: vivienda id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vivienda ALTER COLUMN id SET DEFAULT nextval('public.vivienda_id_seq'::regclass);


--
-- Data for Name: candidatos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.candidatos (id, nombre, email, password, fecha_registro, rol, curp, sexo, ceclular, tel_fijo) FROM stdin;
10	juan perez prado	emmanuel.v@acheme.com.mx	12345	2025-10-20 09:38:36.180599	candidato	\N	\N	\N	\N
11	emmanuelvc	emmanuel@gmail.com	12345	2025-10-20 10:39:28.018671	admin	\N	\N	\N	\N
12	Emmanuel Villanueva Carrillo	emmanuel01@correo.com	12345	2025-10-21 11:37:03.03986	candidato	\N	\N	\N	\N
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
-- Data for Name: salud; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.salud (id, candidato_id, enfermedad_actual, servicio_medico, ocupacion_actual, escolaridad, fuente_ingresos, tiempo_trabajo, ingreso_extra) FROM stdin;
\.


--
-- Data for Name: vivienda; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vivienda (candidato_id, tipo_vivienda, hombres_habitantes, mujeres_habitantes, total_habitantes, total_cuartos, dormitorios, material_piso, material_techo, material_paredes, "tipo_ba¤o", tipo_drenaje, tratamiento_basura, obtencion_luz, combustible_cocina, estatus_casa, id) FROM stdin;
\.


--
-- Name: candidatos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.candidatos_id_seq', 12, true);


--
-- Name: documentos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documentos_id_seq', 2, true);


--
-- Name: salud_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.salud_id_seq', 1, false);


--
-- Name: vivienda_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vivienda_id_seq', 1, false);


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
-- Name: salud salud_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salud
    ADD CONSTRAINT salud_pkey PRIMARY KEY (id);


--
-- Name: vivienda vivienda_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vivienda
    ADD CONSTRAINT vivienda_pkey PRIMARY KEY (id);


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
-- Name: vivienda fk_vivienda_candidato; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vivienda
    ADD CONSTRAINT fk_vivienda_candidato FOREIGN KEY (candidato_id) REFERENCES public.candidatos(id);


--
-- Name: salud salud_candidato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salud
    ADD CONSTRAINT salud_candidato_id_fkey FOREIGN KEY (candidato_id) REFERENCES public.candidatos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict OLaSVIlz3lQ4DlvUz8LRbzv0Srhv5bLkQ2XqcELbrd6jka0HiUdB0Cu12Gp7n7h

