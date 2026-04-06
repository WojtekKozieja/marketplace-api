-- migrate:up

CREATE TABLE public.users
(
	user_id bigint GENERATED ALWAYS AS IDENTITY,
	first_name varchar(30) NOT NULL,
	second_name varchar(30) NOT NULL,
	email varchar(50) UNIQUE NOT NULL ,
	password char(60) NOT NULL ,
	PRIMARY KEY ( user_id )
);

-- migrate:down

DROP TABLE IF EXISTS public.users;
















