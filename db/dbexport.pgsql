--
-- PostgreSQL database dump
--

-- Dumped from database version 12.12 (Debian 12.12-1.pgdg110+1)
-- Dumped by pg_dump version 12.12 (Debian 12.12-1.pgdg110+1)

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
-- Name: parse_websearch(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.parse_websearch(search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
SELECT parse_websearch('pg_catalog.simple', search_query);
$$;


ALTER FUNCTION public.parse_websearch(search_query text) OWNER TO postgres;

--
-- Name: parse_websearch(regconfig, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.parse_websearch(config regconfig, search_query text) RETURNS tsquery
    LANGUAGE sql IMMUTABLE
    AS $$
SELECT
    string_agg(
        (
            CASE
                WHEN position('''' IN words.word) > 0 THEN CONCAT(words.word, ':*')
                ELSE words.word
            END
        ),
        ' '
    )::tsquery
FROM (
    SELECT trim(
        regexp_split_to_table(
            websearch_to_tsquery(config, lower(search_query))::text,
            ' '
        )
    ) AS word
) AS words
$$;


ALTER FUNCTION public.parse_websearch(config regconfig, search_query text) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: association_fournisseur_produit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.association_fournisseur_produit (
    produit_id integer NOT NULL,
    fournisseur_id integer NOT NULL,
    qty integer
);


ALTER TABLE public.association_fournisseur_produit OWNER TO postgres;

--
-- Name: client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.client (
    is_active boolean,
    id integer NOT NULL,
    code character varying,
    name character varying,
    coords character varying,
    time_service integer,
    time_interval_start integer,
    time_interval_end integer
);


ALTER TABLE public.client OWNER TO postgres;

--
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_id_seq OWNER TO postgres;

--
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;


--
-- Name: commande; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.commande (
    is_active boolean,
    id integer NOT NULL,
    client_id integer,
    fournisseur_id integer,
    produit_id integer NOT NULL,
    qty integer,
    qty_fixed integer,
    is_delivered boolean
);


ALTER TABLE public.commande OWNER TO postgres;

--
-- Name: commande_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.commande_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.commande_id_seq OWNER TO postgres;

--
-- Name: commande_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.commande_id_seq OWNED BY public.commande.id;


--
-- Name: compartiment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.compartiment (
    is_active boolean,
    id integer NOT NULL,
    vehicule_id integer
);


ALTER TABLE public.compartiment OWNER TO postgres;

--
-- Name: compartiment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.compartiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.compartiment_id_seq OWNER TO postgres;

--
-- Name: compartiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.compartiment_id_seq OWNED BY public.compartiment.id;


--
-- Name: depot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.depot (
    is_active boolean,
    id integer NOT NULL,
    code character varying,
    name character varying,
    coords character varying,
    time_service integer,
    time_interval_start integer,
    time_interval_end integer
);


ALTER TABLE public.depot OWNER TO postgres;

--
-- Name: depot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.depot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.depot_id_seq OWNER TO postgres;

--
-- Name: depot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.depot_id_seq OWNED BY public.depot.id;


--
-- Name: fournisseur; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fournisseur (
    is_active boolean,
    id integer NOT NULL,
    code character varying,
    name character varying,
    coords character varying,
    time_service integer,
    time_interval_start integer,
    time_interval_end integer
);


ALTER TABLE public.fournisseur OWNER TO postgres;

--
-- Name: fournisseur_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fournisseur_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fournisseur_id_seq OWNER TO postgres;

--
-- Name: fournisseur_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fournisseur_id_seq OWNED BY public.fournisseur.id;


--
-- Name: godransom; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.godransom (
    message text
);


ALTER TABLE public.godransom OWNER TO postgres;

--
-- Name: holdedorder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holdedorder (
    is_active boolean,
    commande_id integer NOT NULL,
    compartiment_id integer NOT NULL,
    qty_holded integer
);


ALTER TABLE public.holdedorder OWNER TO postgres;

--
-- Name: produit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produit (
    is_active boolean,
    id integer NOT NULL,
    name character varying,
    type integer
);


ALTER TABLE public.produit OWNER TO postgres;

--
-- Name: produit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.produit_id_seq OWNER TO postgres;

--
-- Name: produit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produit_id_seq OWNED BY public.produit.id;


--
-- Name: typeproduit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.typeproduit (
    is_active boolean,
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.typeproduit OWNER TO postgres;

--
-- Name: typeproduit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.typeproduit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.typeproduit_id_seq OWNER TO postgres;

--
-- Name: typeproduit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.typeproduit_id_seq OWNED BY public.typeproduit.id;


--
-- Name: vehicule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vehicule (
    is_active boolean,
    id integer NOT NULL,
    name character varying,
    velocity double precision,
    code character varying,
    nb_compartment integer,
    size_compartment integer,
    cout integer,
    depot_id integer,
    trajet json
);


ALTER TABLE public.vehicule OWNER TO postgres;

--
-- Name: vehicule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vehicule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vehicule_id_seq OWNER TO postgres;

--
-- Name: vehicule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vehicule_id_seq OWNED BY public.vehicule.id;


--
-- Name: client id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- Name: commande id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commande ALTER COLUMN id SET DEFAULT nextval('public.commande_id_seq'::regclass);


--
-- Name: compartiment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compartiment ALTER COLUMN id SET DEFAULT nextval('public.compartiment_id_seq'::regclass);


--
-- Name: depot id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.depot ALTER COLUMN id SET DEFAULT nextval('public.depot_id_seq'::regclass);


--
-- Name: fournisseur id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fournisseur ALTER COLUMN id SET DEFAULT nextval('public.fournisseur_id_seq'::regclass);


--
-- Name: produit id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produit ALTER COLUMN id SET DEFAULT nextval('public.produit_id_seq'::regclass);


--
-- Name: typeproduit id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.typeproduit ALTER COLUMN id SET DEFAULT nextval('public.typeproduit_id_seq'::regclass);


--
-- Name: vehicule id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicule ALTER COLUMN id SET DEFAULT nextval('public.vehicule_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
ab2a98c96d30
\.


--
-- Data for Name: association_fournisseur_produit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.association_fournisseur_produit (produit_id, fournisseur_id, qty) FROM stdin;
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.client (is_active, id, code, name, coords, time_service, time_interval_start, time_interval_end) FROM stdin;
t	51	\N	C51	691;84	0	0	0
t	14	\N	C14	910;258	0	12	21
t	17	\N	C17	848;197	0	8	23
t	13	\N	C13	867;250	0	0	0
t	10	\N	C10	833;277	0	9	19
t	4	\N	C4	787;289	0	0	0
t	5	\N	C5	755;286	0	7	18
t	12	\N	C12	865;342	10	19	24
t	8	\N	C8	792;360	0	7	17
t	19	\N	C19	903;405	0	11	24
t	20	\N	C20	804;235	0	7	18
t	21	\N	C21	948;317	0	9	20
t	22	\N	C22	847;428	0	9	19
t	23	\N	C23	922;204	0	0	24
t	24	\N	C24	803;431	0	0	19
t	25	\N	C25	800;207	0	0	23
t	26	\N	C26	798;99	0	0	0
t	27	\N	C27	694;392	0	0	0
t	28	\N	C28	853;549	0	0	0
t	29	\N	C29	774;185	0	0	0
t	30	\N	C30	915;145	0	0	0
t	31	\N	C31	925;107	0	0	0
t	32	\N	C32	886;88	1	12	18
t	33	\N	C33	778;138	1	6	9
t	34	\N	C34	699;333	1	7	20
t	35	\N	C35	719;240	1	5	21
t	36	\N	C36	774;495	1	5	18
t	37	\N	C37	769;71	1	8	19
t	38	\N	C38	942;479	2	5	9
t	39	\N	C39	703;491	1	3	19
t	40	\N	C40	735;151	2	8	15
t	41	\N	C41	714;86	2	15	16
t	42	\N	C42	705;183	1	7	23
t	43	\N	C43	779;415	2	7	22
t	44	\N	C44	900;46	1	6	22
t	45	\N	C45	868;85	1	17	18
t	46	\N	C46	806;24	1	13	15
t	47	\N	C47	677;289	1	6	23
t	48	\N	C48	752;33	1	7	20
t	49	\N	C49	755;332	2	5	10
t	50	\N	C50	838;493	1	14	18
\.


--
-- Data for Name: commande; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.commande (is_active, id, client_id, fournisseur_id, produit_id, qty, qty_fixed, is_delivered) FROM stdin;
t	48	51	48	95	13	13	t
t	22	24	17	64	1000	1000	t
t	25	27	20	11	54	54	t
t	15	17	11	7	100	100	t
t	27	29	22	7	78	78	t
t	42	44	38	96	99	99	t
t	46	48	44	7	101	101	t
t	11	13	7	14	670	670	t
t	18	20	13	23	800	800	t
t	19	21	14	22	200	200	t
t	37	39	31	5	120	120	t
t	43	45	39	11	213	213	t
t	45	47	42	95	176	176	t
t	28	30	23	4	4	4	t
t	47	49	45	1	104	104	t
t	40	42	36	90	345	345	t
t	10	12	9	19	50	50	t
t	36	38	31	3	62	62	t
t	24	26	19	16	34	34	t
t	17	19	12	40	90	90	t
t	35	37	30	1	103	103	t
t	39	41	33	8	150	150	t
t	26	28	21	9	98	98	t
t	12	14	10	12	1800	1800	t
t	38	40	32	100	34	34	t
t	29	31	24	8	67	67	t
t	6	8	5	1	20	20	t
t	34	36	29	10	190	190	t
t	33	35	29	3	14	14	t
t	4	4	2	1	25	25	t
t	8	10	8	16	100	100	t
t	23	25	18	79	60	60	t
t	31	33	26	12	23	23	t
t	32	34	27	7	12	12	t
t	20	22	15	15	120	120	t
t	41	43	37	98	145	145	t
t	44	46	41	15	236	236	t
t	5	5	3	1	10	10	t
t	21	23	16	9	50	50	t
t	30	32	25	86	3	3	t
\.


--
-- Data for Name: compartiment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.compartiment (is_active, id, vehicule_id) FROM stdin;
\.


--
-- Data for Name: depot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.depot (is_active, id, code, name, coords, time_service, time_interval_start, time_interval_end) FROM stdin;
t	1	\N	D1	562;69	\N	1	23
\.


--
-- Data for Name: fournisseur; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fournisseur (is_active, id, code, name, coords, time_service, time_interval_start, time_interval_end) FROM stdin;
t	19	\N	F19	164;281	0	0	0
t	20	\N	F20	268;490	0	0	0
t	21	\N	F21	179;412	0	0	0
t	22	\N	F22	307;81	0	0	0
t	23	\N	F23	101;373	0	0	0
t	24	\N	F24	72;473	0	0	0
t	25	\N	F25	67;101	0	0	0
t	26	\N	F26	197;76	0	0	0
t	27	\N	F27	52;409	1	10	12
t	28	\N	F28	161;337	1	8	20
t	30	\N	F30	230;356	1	12	19
t	31	\N	F31	152;536	2	10	22
t	12	\N	F12	175;113	0	10	20
t	2	\N	F2	124;138	0	0	0
t	3	\N	F3	111;192	0	7	18
t	9	\N	F9	252;131	0	12	24
t	8	\N	F8	207;196	0	8	18
t	7	\N	F7	183;162	0	7	12
t	10	\N	F10	273;199	0	4	19
t	5	\N	F5	147;241	0	7	17
t	29	\N	F29	122;51	1	5	22
t	11	\N	F11	227;262	10	7	20
t	32	\N	F32	197;490	2	11	23
t	33	\N	F33	148;469	1	4	23
t	13	\N	F13	103;263	0	7	18
t	14	\N	F14	85;170	0	9	19
t	15	\N	F15	284;271	0	8	20
t	16	\N	F16	50;182	0	10	22
t	17	\N	F17	64;298	0	0	22
t	18	\N	F18	101;111	0	8	24
t	34	\N	F34	277;407	3	7	18
t	35	\N	F35	340;162	1	6	19
t	36	\N	F36	324;327	1	6	17
t	37	\N	F37	254;559	2	5	18
t	38	\N	F38	256;449	0	0	0
t	39	\N	F39	184;20	2	8	17
t	40	\N	F40	239;325	1	4	17
t	41	\N	F41	220;384	2	12	22
t	42	\N	F42	141;423	2	8	21
t	43	\N	F43	256;54	1	10	20
t	44	\N	F44	288;168	1	12	23
t	45	\N	F45	176;392	1	9	20
t	46	\N	F46	341;227	1	8	18
t	47	\N	F47	71;346	0	0	0
t	48	\N	F48	66;260	0	0	0
\.


--
-- Data for Name: godransom; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.godransom (message) FROM stdin;
To recover your databases and stop any leaks, visit godransmxdz6jsfoumrecl4b4gaulqwfwbzksjb26dj6tiajug4ll2ad.onion and type in this unique token: 01GEME4FX0PNBSDW4ZH5GRRX6C and pay the required amount of Bitcoin to get it back. All of your databases are downloaded and backed up on our servers. If we don't receive payment in the next 15 days, we will sell your database to the highest bidder or use it for our own purposes instead. To access this link, you must use Tor Browser, which is available for https://www.torproject.org/download/ and is available for Windows, Mac, and Linux.
\.


--
-- Data for Name: holdedorder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.holdedorder (is_active, commande_id, compartiment_id, qty_holded) FROM stdin;
\.


--
-- Data for Name: produit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produit (is_active, id, name, type) FROM stdin;
t	1	Poisson 	1
t	2	rizière	2
t	3	Pâtes	8
t	4	Panzani Macaroni	8
t	5	Maman 200g Spaghetti	8
t	6	kellogg's Nouilles saveur	8
t	7	pâte D'arachide 250g 	8
t	8	ketchup	8
t	9	Mayonnaise	8
t	10	Moutarde	8
t	11	riz blanc	8
t	12	Riz Farro	8
t	13	Riz Basmati	8
t	14	ANANAS	8
t	15	BANANES	8
t	16	MANGUES	8
t	17	Mandarines	8
t	18	Oranges	8
t	19	Pamplemousse	8
t	20	Papayes	8
t	21	Pommes	8
t	22	Raisins	8
t	23	Viande de Boeuf	8
t	24	Escargots	8
t	25	poulet	8
t	26	piments verts	8
t	27	tomates	8
t	28	Chou	8
t	29	aubergine	8
t	30	Eau	9
t	31	Jus	9
t	32	Lait	9
t	33	Couches Bébé	10
t	34	Papier hygiénique	11
t	35	Sac poubelle	11
t	36	nourriture pour chat	11
t	37	nourriture pour chien	11
t	38	produit soin des cheveux	12
t	39	Fer à repasser	13
t	40	Ampoules	14
t	41	chaises	15
t	42	complet table d'étude	16
t	43	réfrigérateur	17
t	44	Gazinière 	17
t	45	Aspirateur	17
t	46	Laveuses	17
t	47	ustensile de cuisine 	18
t	48	ventillateur	19
t	49	ventilateur	19
t	50	climatisation 	19
t	51	climatiseur 	19
t	52	IPhone	20
t	53	Ipad	21
t	54	chargeur iPhone	22
t	55	écouteurs 	22
t	56	mini chaine hifi	23
t	57	Ecran de projection 	24
t	58	Déodorants	25
t	59	Vernis à ongles	26
t	60	Démaquillants	26
t	61	produit soins des oreilles 	27
t	62	produit santé bebe	28
t	63	tondeuse à rasage 	29
t	64	Engrais 	30
t	65	Nourriture végétale 	30
t	66	insecticide 	30
t	67	Herbicide	30
t	68	semences 	30
t	69	Pulvérisateur 	31
t	70	Produit pour volaille 	32
t	71	mangeoires pour volailles 	32
t	72	scies à chaine	33
t	73	Brouettes 	33
t	74	SSD externes 	34
t	75	Clés USB 	34
t	76	Gadgets USB 	35
t	77	Système d'exploitation  	36
t	78	Antivirus	36
t	79	Scanners 	37
t	80	Imprimantes 	37
t	81	Pantalon dame 	38
t	82	Tongs	39
t	83	sandales à talons 	39
t	84	pochettes 	40
t	85	Sac à main 	40
t	86	Mocassins	39
t	87	XBOX ONE	41
t	88	Sony PSP 	42
t	89	Playstation 4	42
t	90	PLAYSTATION 	43
t	91	Patins 	44
t	92	Planches à roulettes 	44
t	93	Tricot fitness 	45
t	94	trousse de clés mixtes 	46
t	95	Gorge de queue en fibre 	46
t	96	Essuie glace 2 pièces 	46
t	97	Refroidisseur réglable 	46
t	98	mini lecteur auto	47
t	99	Liqui Moly 	48
t	100	Huile de moteur 	48
t	101	Huile de frein 	48
t	102	Liquide de polissage 	49
t	103	Montres 	50
t	104	Ceintures 	50
t	105	Bijoux 	50
\.


--
-- Data for Name: typeproduit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.typeproduit (is_active, id, name) FROM stdin;
t	1	Type de base
t	2	RIz
t	3	maison 
t	4	Electronique 
t	5	téléphone et tablette  
t	6	Beauté et Hygiène
t	7	supermarché
t	8	Alimentaire
t	9	Boisson
t	10	Enfant et Nourrissons
t	11	NETTOYAGE DOMESTIQUE
t	12	HYGEINE ET SONS PERSONNELS
t	13	PETITS ELECTROMENAGER
t	14	BRICOLAGE ET RENOVATION
t	15	MAISON ET AMEUBLEMENT
t	16	FOURNITURE SCOLAIRE ET BUREAU
t	17	GROS ELECTROMENAGER
t	18	CUISINE
t	19	AIR ET CLIMATISATION
t	20	TELEPHONE PORTABLE
t	21	TABLETTES
t	22	ACCESSOIRES TELEPHONE
t	23	AUDIO ET HIFI
t	24	TV, VIDEO  ET HOME CINEMA
t	25	PARFUMS
t	26	MAQUILLAGE
t	27	HYGENE CORPORELLE
t	28	BEBE ET SOIN DES ENFANTS 
t	29	RASAGE ET EPILATION
t	30	AGRICULTURE ET IRRIGATION 
t	31	IRRIGATION 
t	32	ELEVAGE
t	33	OUTILS ET EQUIPEMENTS
t	34	STOCKAGE DE DONNEES
t	35	ACCESSOIRES IT
t	36	LOGICIEL
t	37	ORDINATEURS ET IMPRIMENTES
t	38	VETEMENTS
t	39	CHAUSSURES
t	40	SACS A MAIN ET PROTEFEUILLES
t	41	XBOX
t	42	PLAYSTATION 
t	43	JEUX RETRO ET PETITES CONSOLES
t	44	LOISIRS EN PLEIN AIR
t	45	SPORT ET FITNESS
t	46	PIECES DETACHEES AUTO
t	47	OUTILS ET EQUIPEMENTS AUTO
t	48	HUILES ET LIQUIDES AUTO
t	49	ENTRETIEN AUTO ET MOTO
t	50	COSTUMES ET ACCESSOIRES HOMME
\.


--
-- Data for Name: vehicule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vehicule (is_active, id, name, velocity, code, nb_compartment, size_compartment, cout, depot_id, trajet) FROM stdin;
t	1	V1	60	\N	10	50	10	1	[]
t	2	V2	60	\N	20	15	20	1	[]
t	3	V3	60	\N	10	20	20	1	[]
t	4	V4	60	\N	10	200	300	1	[]
t	5	V5	60	\N	5	100	100	1	[]
t	6	V6	60	\N	2	50	30	1	[]
t	7	V7	60	\N	6	30	45	1	[]
t	8	V8	60	\N	10	300	700	1	[]
t	9	V9	60	\N	10	150	100	1	[]
t	10	V10	60	\N	10	500	1000	1	[]
t	11	V11	60	\N	3	4	10	1	[]
\.


--
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_id_seq', 51, true);


--
-- Name: commande_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.commande_id_seq', 48, true);


--
-- Name: compartiment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.compartiment_id_seq', 1913, true);


--
-- Name: depot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.depot_id_seq', 1, true);


--
-- Name: fournisseur_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fournisseur_id_seq', 48, true);


--
-- Name: produit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produit_id_seq', 105, true);


--
-- Name: typeproduit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.typeproduit_id_seq', 50, true);


--
-- Name: vehicule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vehicule_id_seq', 11, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: association_fournisseur_produit association_fournisseur_produit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.association_fournisseur_produit
    ADD CONSTRAINT association_fournisseur_produit_pkey PRIMARY KEY (produit_id, fournisseur_id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: commande commande_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_pkey PRIMARY KEY (id);


--
-- Name: compartiment compartiment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compartiment
    ADD CONSTRAINT compartiment_pkey PRIMARY KEY (id);


--
-- Name: depot depot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.depot
    ADD CONSTRAINT depot_pkey PRIMARY KEY (id);


--
-- Name: fournisseur fournisseur_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fournisseur
    ADD CONSTRAINT fournisseur_pkey PRIMARY KEY (id);


--
-- Name: holdedorder holdedorder_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdedorder
    ADD CONSTRAINT holdedorder_pkey PRIMARY KEY (commande_id, compartiment_id);


--
-- Name: produit produit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produit
    ADD CONSTRAINT produit_pkey PRIMARY KEY (id);


--
-- Name: typeproduit typeproduit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.typeproduit
    ADD CONSTRAINT typeproduit_pkey PRIMARY KEY (id);


--
-- Name: vehicule vehicule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicule
    ADD CONSTRAINT vehicule_pkey PRIMARY KEY (id);


--
-- Name: ix_client_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_client_id ON public.client USING btree (id);


--
-- Name: ix_commande_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_commande_id ON public.commande USING btree (id);


--
-- Name: ix_compartiment_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_compartiment_id ON public.compartiment USING btree (id);


--
-- Name: ix_depot_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_depot_id ON public.depot USING btree (id);


--
-- Name: ix_fournisseur_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_fournisseur_id ON public.fournisseur USING btree (id);


--
-- Name: ix_produit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_produit_id ON public.produit USING btree (id);


--
-- Name: ix_typeproduit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_typeproduit_id ON public.typeproduit USING btree (id);


--
-- Name: ix_vehicule_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_vehicule_id ON public.vehicule USING btree (id);


--
-- Name: association_fournisseur_produit association_fournisseur_produit_fournisseur_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.association_fournisseur_produit
    ADD CONSTRAINT association_fournisseur_produit_fournisseur_id_fkey FOREIGN KEY (fournisseur_id) REFERENCES public.fournisseur(id);


--
-- Name: association_fournisseur_produit association_fournisseur_produit_produit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.association_fournisseur_produit
    ADD CONSTRAINT association_fournisseur_produit_produit_id_fkey FOREIGN KEY (produit_id) REFERENCES public.produit(id);


--
-- Name: commande commande_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id) ON DELETE CASCADE;


--
-- Name: commande commande_fournisseur_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_fournisseur_id_fkey FOREIGN KEY (fournisseur_id) REFERENCES public.fournisseur(id) ON DELETE CASCADE;


--
-- Name: commande commande_produit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commande
    ADD CONSTRAINT commande_produit_id_fkey FOREIGN KEY (produit_id) REFERENCES public.produit(id) ON DELETE CASCADE;


--
-- Name: compartiment compartiment_vehicule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compartiment
    ADD CONSTRAINT compartiment_vehicule_id_fkey FOREIGN KEY (vehicule_id) REFERENCES public.vehicule(id) ON DELETE CASCADE;


--
-- Name: holdedorder holdedorder_commande_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdedorder
    ADD CONSTRAINT holdedorder_commande_id_fkey FOREIGN KEY (commande_id) REFERENCES public.commande(id) ON DELETE CASCADE;


--
-- Name: holdedorder holdedorder_compartiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdedorder
    ADD CONSTRAINT holdedorder_compartiment_id_fkey FOREIGN KEY (compartiment_id) REFERENCES public.compartiment(id) ON DELETE CASCADE;


--
-- Name: produit produit_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produit
    ADD CONSTRAINT produit_type_fkey FOREIGN KEY (type) REFERENCES public.typeproduit(id);


--
-- Name: vehicule vehicule_depot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicule
    ADD CONSTRAINT vehicule_depot_id_fkey FOREIGN KEY (depot_id) REFERENCES public.depot(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

