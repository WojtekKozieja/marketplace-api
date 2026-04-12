-- migrate:up

CREATE TABLE public.price_logs
(
    offer_id bigint,
    changed_date timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    new_price numeric(10,2) NOT NULL CHECK ( new_price >= 0 ),
    is_active boolean NOT NULL,
    PRIMARY KEY (offer_id, changed_date),
    CONSTRAINT offer_id_is_active_fkey FOREIGN KEY (offer_id, is_active)
        REFERENCES public.offers (offer_id, is_active)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- migrate:down

DROP TABLE IF EXISTS public.price_logs;

