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


CREATE INDEX i_german_word ON master(german_word);
                                
--
-- conjunction
--
CREATE TABLE IF NOT EXISTS conjunction (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text
                                    );