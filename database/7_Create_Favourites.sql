-- migrate:up

CREATE TABLE public.favourites
(
    user_id bigint,
    offer_id bigint,
    is_active boolean DEFAULT TRUE,
    PRIMARY KEY (user_id, offer_id),
    CONSTRAINT user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT offer_id_fkey FOREIGN KEY (offer_id, is_active)
        REFERENCES public.offers (offer_id, is_active)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)PARTITION BY HASH (user_id);

CREATE TABLE public.favourites_0 PARTITION OF public.favourites
FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE public.favourites_1 PARTITION OF public.favourites
FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE public.favourites_2 PARTITION OF public.favourites
FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE public.favourites_3 PARTITION OF public.favourites
FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- migrate:down

DROP TABLE IF EXISTS public.favourites;
