-- migrate:up

CREATE OR REPLACE FUNCTION add_price_logs() RETURNS trigger
AS
$$
BEGIN
    IF tg_op = 'INSERT' OR old.unit_price != new.unit_price THEN
        INSERT INTO public.price_logs (offer_id, changed_date, new_price, is_active)  VALUES
            (new.offer_id, CURRENT_TIMESTAMP, new.unit_price, new.is_active);
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_price_logs AFTER INSERT OR UPDATE ON public.offers
FOR EACH ROW EXECUTE FUNCTION add_price_logs();

-- migrate:down

DROP TRIGGER IF EXISTS trg_price_logs ON public.offers;
DROP FUNCTION IF EXISTS add_price_logs();
