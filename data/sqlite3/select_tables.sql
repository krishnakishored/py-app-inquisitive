/*
 * SQLite CREATE TABLE examples.
 * 
 */

--
-- master
--
SELECT * FROM master ORDER BY RANDOM() LIMIT 3;
select german_word,frequency,difficulty from master where german_word='weder … noch';
select german_word,frequency,difficulty from master where frequency>0;
select german_word,frequency,difficulty from master where difficulty<0;

--
-- conjunction
--
-- SELECT * FROM conjunction ORDER BY RANDOM() LIMIT 3;
