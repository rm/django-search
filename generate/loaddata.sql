BEGIN;

DELETE FROM blogapp_author;
DELETE FROM blogapp_tag;
DELETE FROM blogapp_entry;
DELETE FROM blogapp_entry_tags;

\copy blogapp_author from generate/authors.csv with csv
\copy blogapp_tag from generate/tags.csv with csv
\copy blogapp_entry from generate/entries.csv with csv
\copy blogapp_entry_tags from generate/entries_tags.csv with csv

COMMIT;
