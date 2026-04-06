-- migrate:up

CREATE TABLE public.categories
(
	category_id smallint GENERATED ALWAYS AS IDENTITY,
	category_name varchar(30) UNIQUE NOT NULL ,
	PRIMARY KEY ( category_id )
);

CREATE TABLE public.subcategories
(
	subcategory_id smallint GENERATED ALWAYS AS IDENTITY UNIQUE,
	category_id integer NOT NULL,
	subcategory_name varchar(30) NOT NULL,
	PRIMARY KEY (subcategory_id, category_id),
	CONSTRAINT category_id_fkey FOREIGN KEY (category_id)
		REFERENCES public.categories ( category_id )
		ON UPDATE CASCADE
		ON DELETE CASCADE
);


-- migrate:down

DROP TABLE IF EXISTS public.subcategories;
DROP TABLE IF EXISTS public.categories;