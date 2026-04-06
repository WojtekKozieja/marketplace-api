-- migrate:up

CREATE TABLE public.orders
(
	order_id bigint GENERATED ALWAYS AS IDENTITY,
	buyer_id bigint NOT NULL,
	order_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY ( order_id, order_date ),
	CONSTRAINT buyer_id_fkey FOREIGN KEY ( buyer_id )
		REFERENCES public.users ( user_id )
		ON DELETE RESTRICT
		ON UPDATE CASCADE
) PARTITION BY RANGE ( order_date );

-- start of service was in 2024 year
CREATE TABLE public.orders_2024 PARTITION OF public.orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE public.orders_2025 PARTITION OF public.orders
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE public.orders_2026 PARTITION OF public.orders
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX idx_orders_buyer ON public.orders (buyer_id);

-- migrate:down

DROP TABLE IF EXISTS public.orders;