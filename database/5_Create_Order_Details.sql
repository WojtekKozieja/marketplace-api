-- migrate:up

CREATE TABLE public.order_details
(
	order_id bigint,
	offer_id bigint,
	order_date timestamp,
	unit_price numeric(10,2) NOT NULL CHECK ( unit_price >= 0 ),
	quantity int NOT NULL,
    title varchar(50) NOT NULL,
	photo varchar(100), -- path to photo
	is_active boolean NOT NULL DEFAULT TRUE,
	PRIMARY KEY (order_id, offer_id, order_date, is_active),
	CONSTRAINT order_id_fkey FOREIGN KEY (order_id, order_date)
		REFERENCES public.orders (order_id, order_date)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
    CONSTRAINT offer_id_fkey FOREIGN KEY ( offer_Id, is_active )
		REFERENCES public.offers ( offer_id, is_active )
		ON DELETE CASCADE
		ON UPDATE CASCADE
) PARTITION BY RANGE (order_date);

CREATE TABLE public.order_details_2024 PARTITION OF public.order_details
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE public.order_details_2025 PARTITION OF public.order_details
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE public.order_details_2026 PARTITION OF public.order_details
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- migrate:down

DROP TABLE IF EXISTS public.order_details;