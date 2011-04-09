BEGIN;

ALTER TABLE blogapp_entry
ADD COLUMN search_tsv tsvector;

UPDATE blogapp_entry
SET search_tsv=to_tsvector(text);

CREATE INDEX blogapp_search_tsv_index
ON blogapp_entry USING gin(search_tsv);

CREATE TRIGGER blogapp_search_tsv_trigger
BEFORE INSERT OR UPDATE
ON blogapp_entry
FOR EACH ROW
EXECUTE PROCEDURE
tsvector_update_trigger('search_tsv', 'pg_catalog.english', 'text');

COMMIT;
