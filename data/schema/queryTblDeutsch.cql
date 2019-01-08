-- Common queries


use inquisitive;

-- select less frequent words
SELECT german_word,english_word, frequency FROM tbl_deutsch WHERE frequency>3 LIMIT 10 ALLOW FILTERING;

-- select tough words
SELECT english_word, german_word, toughness FROM tbl_deutsch WHERE toughness<0 LIMIT 10 ALLOW FILTERING;