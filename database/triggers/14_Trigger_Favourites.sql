-- migrate:up

CREATE OR REPLACE FUNCTION delete_inactive_offers() RETURNS trigger
AS
$$
BEGIN
    IF new.is_active = FALSE then
        RETURN NULL;
    END IF;
    RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_del_inactive_offers BEFORE UPDATE ON public.favourites
FOR EACH ROW EXECUTE FUNCTION delete_inactive_offers();

-- migrate:down

DROP TRIGGER IF EXISTS trg_del_inactive_offers ON public.favourites;
DROP FUNCTION IF EXISTS delete_inactive_offers();