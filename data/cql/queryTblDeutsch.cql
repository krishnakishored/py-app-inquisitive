-- Common queries


use inquisitive;

-- select less frequent words
SELECT german_word,english_word, frequency FROM tbl_deutsch WHERE frequency>3 LIMIT 10 ALLOW FILTERING;

-- select tough words
SELECT english_word, german_word, difficulty FROM tbl_deutsch WHERE difficulty<0 LIMIT 10 ALLOW FILTERING;