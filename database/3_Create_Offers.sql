-- migrate:up

CREATE TABLE public.offers
(
	offer_id bigint GENERATED ALWAYS AS IDENTITY,
	seller_id bigint NOT NULL,
	--category_id integer NOT NULL,
	subcategory_id smallint NOT NULL,
	unit_price numeric(10,2) NOT NULL CHECK ( unit_price >= 0 ),
	quantity integer NOT NULL CHECK ( quantity >= 0 ),
	title varchar(50) NOT NULL,
	description varchar(1000) NOT NULL,
	photo varchar(100), -- path to photo
	start_offer_date timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
	end_offer_date timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days',
    is_active boolean NOT NULL DEFAULT TRUE,
	PRIMARY KEY ( offer_id, is_active ),
	CONSTRAINT seller_id_fkey FOREIGN KEY ( seller_id )
		REFERENCES public.users ( user_id )
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
    CONSTRAINT subcategory_id_fkey FOREIGN KEY (subcategory_id)
		REFERENCES public.subcategories (subcategory_id)
		ON DELETE RESTRICT
		ON UPDATE CASCADE
)PARTITION BY LIST (is_active);

CREATE TABLE public.active_offers PARTITION OF public.offers
    FOR VALUES IN (TRUE);

CREATE TABLE public.inactive_offers PARTITION OF public.offers
    FOR VALUES IN (FALSE);

CREATE INDEX idx_active_offer_unit_price ON public.active_offers (unit_price);
CREATE INDEX idx_active_offer_subcategory ON public.active_offers (subcategory_id);
CREATE INDEX idx_active_offer_end_offer_date ON public.active_offers (end_offer_date);

-- migrate:down

DROP TABLE IF EXISTS public.offers;