-- migrate:up

CREATE OR REPLACE FUNCTION  add_order_details() RETURNS trigger
AS
$$
BEGIN
    SELECT unit_price, title, photo, is_active
    INTO new.unit_price, new.title, new.photo, new.is_active
    FROM public.offers
    WHERE offer_id = new.offer_id AND is_active = TRUE;

    IF NOT found then
        RAISE EXCEPTION 'Not found offer';
    END IF;

    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_snapshot_order_details BEFORE INSERT ON order_details
FOR EACH ROW EXECUTE FUNCTION add_order_details();

-- migrate:down

DROP TRIGGER IF EXISTS trg_snapshot_order_details ON order_details;
DROP FUNCTION IF EXISTS add_order_details();
