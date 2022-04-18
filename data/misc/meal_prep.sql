--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1


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

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.addresses (
    id integer NOT NULL,
    address_line_1 text NOT NULL,
    address_line_2 text,
    city text NOT NULL,
    state text NOT NULL,
    zip_code integer NOT NULL
);

CREATE SEQUENCE public.addresses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.contacts (
    id integer NOT NULL,
    email_address text NOT NULL,
    phone_number text
);

CREATE SEQUENCE public.contacts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.items (
    id integer NOT NULL,
    name character(20) NOT NULL UNIQUE,
    category character(20) NOT NULL,
    quantity_avail integer NOT NULL,
    price numeric NOT NULL,
    image text NOT NULL
);

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.names (
    id integer NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    middle_name text
);

CREATE SEQUENCE public.names_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.nutritional_rqts (
    id integer NOT NULL,
    description text NOT NULL
);

CREATE SEQUENCE public.nutritional_rqts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.orders (
    id integer NOT NULL,
    address_id integer NOT NULL,
    contact_id integer NOT NULL,
    name_id integer NOT NULL,
    payment_id integer NOT NULL,
    user_id integer,
    delivered_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.orders_items (
    order_id integer NOT NULL,
    item_id integer NOT NULL,
    quantity integer NOT NULL
);


CREATE TABLE public.orders_nutritional_rqts (
    order_id integer NOT NULL,
    nutritional_rqt_id integer NOT NULL
);


CREATE TABLE public.payments (
    id integer NOT NULL,
    card_number text NOT NULL,
    expiration_date character(10) NOT NULL,
    address_id integer NOT NULL
);

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.users (
    id integer NOT NULL,
    password text NOT NULL,
    name_id integer NOT NULL,
    address_id integer,
    nutritional_rqt_id integer,
    contact_id integer NOT NULL
);

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


CREATE TABLE public.users_payments (
    user_id integer NOT NULL,
    payment_id integer NOT NULL
);

ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);


--
-- Name: contacts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts ALTER COLUMN id SET DEFAULT nextval('public.contacts_id_seq'::regclass);


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Name: names id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.names ALTER COLUMN id SET DEFAULT nextval('public.names_id_seq'::regclass);


--
-- Name: nutritional_rqts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutritional_rqts ALTER COLUMN id SET DEFAULT nextval('public.nutritional_rqts_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- Name: names names_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.names
    ADD CONSTRAINT names_pkey PRIMARY KEY (id);


--
-- Name: nutritional_rqts nutritional_rqts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.nutritional_rqts
    ADD CONSTRAINT nutritional_rqts_pkey PRIMARY KEY (id);


--
-- Name: orders_items orders_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_pkey PRIMARY KEY (order_id, item_id);


--
-- Name: orders_nutritional_rqts orders_nutritional_rqts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_nutritional_rqts
    ADD CONSTRAINT orders_nutritional_rqts_pkey PRIMARY KEY (order_id, nutritional_rqt_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: users_payments users_payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_payments
    ADD CONSTRAINT users_payments_pkey PRIMARY KEY (user_id, payment_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users fk_addresses; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_addresses FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: payments fk_addresses; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT fk_addresses FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: orders fk_addresses; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_addresses FOREIGN KEY (address_id) REFERENCES public.addresses(id);


--
-- Name: orders fk_contacts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_contacts FOREIGN KEY (contact_id) REFERENCES public.contacts(id);


--
-- Name: users fk_contacts_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_contacts_id FOREIGN KEY (contact_id) REFERENCES public.contacts(id);


--
-- Name: users fk_names; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_names FOREIGN KEY (name_id) REFERENCES public.names(id);


--
-- Name: orders fk_names; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_names FOREIGN KEY (name_id) REFERENCES public.names(id);


--
-- Name: users fk_nutritional_rqts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_nutritional_rqts FOREIGN KEY (nutritional_rqt_id) REFERENCES public.nutritional_rqts(id);


--
-- Name: orders_items fk_oi_items; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT fk_oi_items FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: orders_items fk_oi_orders; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT fk_oi_orders FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: orders_nutritional_rqts fk_on_nutritional_rqts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_nutritional_rqts
    ADD CONSTRAINT fk_on_nutritional_rqts FOREIGN KEY (nutritional_rqt_id) REFERENCES public.nutritional_rqts(id);


--
-- Name: orders_nutritional_rqts fk_on_orders; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_nutritional_rqts
    ADD CONSTRAINT fk_on_orders FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: orders fk_payments; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_payments FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: users_payments fk_up_payments; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_payments
    ADD CONSTRAINT fk_up_payments FOREIGN KEY (payment_id) REFERENCES public.payments(id);


--
-- Name: users_payments fk_up_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_payments
    ADD CONSTRAINT fk_up_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: orders fk_users; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

