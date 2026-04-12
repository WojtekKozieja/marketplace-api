-- migrate:up

CREATE OR REPLACE FUNCTION update_quantity() RETURNS trigger
AS
$$
DECLARE
    current_quantity integer;
BEGIN
    SELECT quantity INTO current_quantity
    FROM public.offers
    WHERE offer_id = new.offer_id AND is_active = TRUE AND end_offer_date >= CURRENT_TIMESTAMP;

    IF NOT found then
        RAISE EXCEPTION 'This offer not exists';
    END IF;

    IF current_quantity < new.quantity then
        RAISE EXCEPTION 'insufficient quantity in offer';
    END IF;

    UPDATE public.offers
    SET
        quantity = quantity - new.quantity,
        is_active = CASE
            WHEN quantity - new.quantity = 0 THEN FALSE
            ELSE TRUE
        END,
        end_offer_date = CASE
            WHEN quantity - new.quantity = 0 THEN CURRENT_TIMESTAMP
            ELSE end_offer_date
        END

    WHERE offer_id = new.offer_id AND is_active = TRUE; --partition pruning

    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_offers_quantity AFTER INSERT ON public.order_details
FOR EACH ROW EXECUTE FUNCTION update_quantity();

-- migrate:down

DROP TRIGGER IF EXISTS trg_offers_quantity ON public.order_details;
DROP FUNCTION IF EXISTS update_quantity();