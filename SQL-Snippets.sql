-- Example of single line comment
/* Example of multi line
comment */

-- Basic Join


-- ANTI JOIN: all values from table1 where not in table2
-- Source: http://blog.montmere.com/2010/12/08/the-anti-join-all-values-from-table1-where-not-in-table2/
SELECT
*
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.id
WHERE t2.id IS NULL
