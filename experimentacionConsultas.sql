set search_path to bd1k;
---setear (con indices)
SET enable_mergejoin TO OFF ;
SET enable_hashjoin TO OFF ;
SET enable_bitmapscan TO OFF ;
SET enable_sort TO OFF ;

---setear (sin indices)
SET enable_mergejoin TO ON ;
SET enable_hashjoin TO ON ;
SET enable_bitmapscan TO ON ;
SET enable_sort TO ON ;

--
EXPLAIN ANALYZE
