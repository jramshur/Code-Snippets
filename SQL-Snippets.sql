-- Example of single line comment
/* Example of multi line
comment */

SELECT
*
FROM table1 t1
LEFT JOIN table2 t2 ON t1.id = t2.id
WHERE t2.id IS NULL
