PGDMP         5                 }         	   lingvo_db     15.10 (Debian 15.10-1.pgdg120+1)    15.10 (Debian 15.10-0+deb12u1) 3    H           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            I           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            J           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            K           1262    16384 	   lingvo_db    DATABASE     t   CREATE DATABASE lingvo_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
    DROP DATABASE lingvo_db;
                postgres    false            �            1259    16428 
   crosswords    TABLE     �   CREATE TABLE public.crosswords (
    id integer NOT NULL,
    title character varying NOT NULL,
    grid json NOT NULL,
    clues json NOT NULL,
    topic_id integer
);
    DROP TABLE public.crosswords;
       public         heap    postgres    false            �            1259    16427    crosswords_id_seq    SEQUENCE     �   CREATE SEQUENCE public.crosswords_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.crosswords_id_seq;
       public          postgres    false    221            L           0    0    crosswords_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.crosswords_id_seq OWNED BY public.crosswords.id;
          public          postgres    false    220            �            1259    16412 
   flashcards    TABLE     �   CREATE TABLE public.flashcards (
    id integer NOT NULL,
    word character varying NOT NULL,
    translation character varying NOT NULL,
    definition text,
    examples json,
    img_path text,
    topic_id integer
);
    DROP TABLE public.flashcards;
       public         heap    postgres    false            �            1259    16411    flashcards_id_seq    SEQUENCE     �   CREATE SEQUENCE public.flashcards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.flashcards_id_seq;
       public          postgres    false    219            M           0    0    flashcards_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.flashcards_id_seq OWNED BY public.flashcards.id;
          public          postgres    false    218            �            1259    16397    topics    TABLE     �   CREATE TABLE public.topics (
    id integer NOT NULL,
    title character varying NOT NULL,
    description text,
    tags json NOT NULL,
    max_grade integer NOT NULL,
    user_id integer
);
    DROP TABLE public.topics;
       public         heap    postgres    false            �            1259    16396    topics_id_seq    SEQUENCE     �   CREATE SEQUENCE public.topics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.topics_id_seq;
       public          postgres    false    217            N           0    0    topics_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.topics_id_seq OWNED BY public.topics.id;
          public          postgres    false    216            �            1259    16443    user_topic_grades    TABLE     �   CREATE TABLE public.user_topic_grades (
    id integer NOT NULL,
    user_id integer,
    topic_id integer,
    grade integer NOT NULL,
    at timestamp without time zone NOT NULL
);
 %   DROP TABLE public.user_topic_grades;
       public         heap    postgres    false            �            1259    16442    user_topic_grades_id_seq    SEQUENCE     �   CREATE SEQUENCE public.user_topic_grades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.user_topic_grades_id_seq;
       public          postgres    false    223            O           0    0    user_topic_grades_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.user_topic_grades_id_seq OWNED BY public.user_topic_grades.id;
          public          postgres    false    222            �            1259    16386    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_admin boolean NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16385    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    215            P           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    214            �           2604    16431    crosswords id    DEFAULT     n   ALTER TABLE ONLY public.crosswords ALTER COLUMN id SET DEFAULT nextval('public.crosswords_id_seq'::regclass);
 <   ALTER TABLE public.crosswords ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            �           2604    16415    flashcards id    DEFAULT     n   ALTER TABLE ONLY public.flashcards ALTER COLUMN id SET DEFAULT nextval('public.flashcards_id_seq'::regclass);
 <   ALTER TABLE public.flashcards ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    219    219            �           2604    16400 	   topics id    DEFAULT     f   ALTER TABLE ONLY public.topics ALTER COLUMN id SET DEFAULT nextval('public.topics_id_seq'::regclass);
 8   ALTER TABLE public.topics ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    16446    user_topic_grades id    DEFAULT     |   ALTER TABLE ONLY public.user_topic_grades ALTER COLUMN id SET DEFAULT nextval('public.user_topic_grades_id_seq'::regclass);
 C   ALTER TABLE public.user_topic_grades ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    223    222    223            �           2604    16389    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    214    215    215            C          0    16428 
   crosswords 
   TABLE DATA           F   COPY public.crosswords (id, title, grid, clues, topic_id) FROM stdin;
    public          postgres    false    221   �8       A          0    16412 
   flashcards 
   TABLE DATA           e   COPY public.flashcards (id, word, translation, definition, examples, img_path, topic_id) FROM stdin;
    public          postgres    false    219   9       ?          0    16397    topics 
   TABLE DATA           R   COPY public.topics (id, title, description, tags, max_grade, user_id) FROM stdin;
    public          postgres    false    217   .9       E          0    16443    user_topic_grades 
   TABLE DATA           M   COPY public.user_topic_grades (id, user_id, topic_id, grade, at) FROM stdin;
    public          postgres    false    223   K9       =          0    16386    users 
   TABLE DATA           H   COPY public.users (id, username, hashed_password, is_admin) FROM stdin;
    public          postgres    false    215   h9       Q           0    0    crosswords_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.crosswords_id_seq', 1, false);
          public          postgres    false    220            R           0    0    flashcards_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.flashcards_id_seq', 1, false);
          public          postgres    false    218            S           0    0    topics_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.topics_id_seq', 1, false);
          public          postgres    false    216            T           0    0    user_topic_grades_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.user_topic_grades_id_seq', 1, false);
          public          postgres    false    222            U           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 1, true);
          public          postgres    false    214            �           2606    16435    crosswords crosswords_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.crosswords
    ADD CONSTRAINT crosswords_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.crosswords DROP CONSTRAINT crosswords_pkey;
       public            postgres    false    221            �           2606    16419    flashcards flashcards_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.flashcards
    ADD CONSTRAINT flashcards_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.flashcards DROP CONSTRAINT flashcards_pkey;
       public            postgres    false    219            �           2606    16404    topics topics_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.topics DROP CONSTRAINT topics_pkey;
       public            postgres    false    217            �           2606    16448 (   user_topic_grades user_topic_grades_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.user_topic_grades
    ADD CONSTRAINT user_topic_grades_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.user_topic_grades DROP CONSTRAINT user_topic_grades_pkey;
       public            postgres    false    223            �           2606    16393    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            �           1259    16441    ix_crosswords_id    INDEX     E   CREATE INDEX ix_crosswords_id ON public.crosswords USING btree (id);
 $   DROP INDEX public.ix_crosswords_id;
       public            postgres    false    221            �           1259    16426    ix_flashcards_id    INDEX     E   CREATE INDEX ix_flashcards_id ON public.flashcards USING btree (id);
 $   DROP INDEX public.ix_flashcards_id;
       public            postgres    false    219            �           1259    16425    ix_flashcards_word    INDEX     I   CREATE INDEX ix_flashcards_word ON public.flashcards USING btree (word);
 &   DROP INDEX public.ix_flashcards_word;
       public            postgres    false    219            �           1259    16410    ix_topics_id    INDEX     =   CREATE INDEX ix_topics_id ON public.topics USING btree (id);
     DROP INDEX public.ix_topics_id;
       public            postgres    false    217            �           1259    16459    ix_user_topic_grades_id    INDEX     S   CREATE INDEX ix_user_topic_grades_id ON public.user_topic_grades USING btree (id);
 +   DROP INDEX public.ix_user_topic_grades_id;
       public            postgres    false    223            �           1259    16395    ix_users_id    INDEX     ;   CREATE INDEX ix_users_id ON public.users USING btree (id);
    DROP INDEX public.ix_users_id;
       public            postgres    false    215            �           1259    16394    ix_users_username    INDEX     N   CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);
 %   DROP INDEX public.ix_users_username;
       public            postgres    false    215            �           2606    16436 #   crosswords crosswords_topic_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.crosswords
    ADD CONSTRAINT crosswords_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id);
 M   ALTER TABLE ONLY public.crosswords DROP CONSTRAINT crosswords_topic_id_fkey;
       public          postgres    false    221    217    3230            �           2606    16420 #   flashcards flashcards_topic_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.flashcards
    ADD CONSTRAINT flashcards_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id);
 M   ALTER TABLE ONLY public.flashcards DROP CONSTRAINT flashcards_topic_id_fkey;
       public          postgres    false    3230    219    217            �           2606    16405    topics topics_user_id_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 D   ALTER TABLE ONLY public.topics DROP CONSTRAINT topics_user_id_fkey;
       public          postgres    false    217    3227    215            �           2606    16454 1   user_topic_grades user_topic_grades_topic_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_topic_grades
    ADD CONSTRAINT user_topic_grades_topic_id_fkey FOREIGN KEY (topic_id) REFERENCES public.topics(id);
 [   ALTER TABLE ONLY public.user_topic_grades DROP CONSTRAINT user_topic_grades_topic_id_fkey;
       public          postgres    false    217    3230    223            �           2606    16449 0   user_topic_grades user_topic_grades_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_topic_grades
    ADD CONSTRAINT user_topic_grades_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 Z   ALTER TABLE ONLY public.user_topic_grades DROP CONSTRAINT user_topic_grades_user_id_fkey;
       public          postgres    false    223    215    3227            C      x������ � �      A      x������ � �      ?      x������ � �      E      x������ � �      =   U   x�3�,.)��K�T1JR14R	.�vLʬ
3�ȯ,�73r�	�35��-���4�ss�O7JK��5MKʪ,Ύ*�,����� �5x     