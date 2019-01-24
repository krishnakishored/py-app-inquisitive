/*
 * SQLite CREATE TABLE examples.
 * 
 */

--
-- master
--
CREATE TABLE IF NOT EXISTS master (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text,
                                        frequency integer,
                                        difficulty integer
                                ); 

--
-- indices
--
CREATE INDEX i_german_word ON master(german_word);
CREATE INDEX i_frequency ON master(frequency);
CREATE INDEX i_difficulty ON master(difficulty);
CREATE INDEX i_partsofspeech ON master(partsofspeech);
                                

--
-- verb
--
-- CREATE TABLE IF NOT EXISTS verb (
--                                         id integer PRIMARY KEY,
--                                         german_word text UNIQUE NOT NULL,
--                                         english_word text NOT NULL,
--                                         partsofspeech text
--                                     );                                


--
-- conjunction
--
-- CREATE TABLE IF NOT EXISTS conjunction (
--                                         id integer PRIMARY KEY,
--                                         german_word text UNIQUE NOT NULL,
--                                         english_word text NOT NULL,
--                                         partsofspeech text
--                                     );