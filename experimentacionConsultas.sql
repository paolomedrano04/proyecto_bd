set search_path to bd1millon;
---setear (con indices)
SET enable_mergejoin TO OFF ;
SET enable_hashjoin TO OFF ;
SET enable_bitmapscan TO OFF ;
SET enable_sort TO OFF ;

---setear (sin indices)
SET enable_hashjoin TO ON ;
SET enable_bitmapscan TO ON ;
SET enable_sort TO ON ;
SET enable_mergejoin TO ON ;

--consulta
EXPLAIN ANALYZE


	
CREATE OR REPLACE FUNCTION drop_non_pk_fk_indexes()
RETURNS void LANGUAGE plpgsql AS $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT
            indexname AS index_name,
            tablename AS table_name
        FROM
            pg_indexes
        WHERE
            schemaname = 'bd1millon'  -- Cambia 'public' por el esquema que estés utilizando
            AND indexname NOT IN (
                SELECT conname
                FROM pg_constraint
                WHERE contype IN ('p', 'f')
            )
    LOOP
        EXECUTE 'DROP INDEX IF EXISTS ' || quote_ident(r.index_name) || ' CASCADE';
        RAISE NOTICE 'Dropped index: % on table: %', r.index_name, r.table_name;
    END LOOP;
END $$;

SELECT drop_non_pk_fk_indexes();
