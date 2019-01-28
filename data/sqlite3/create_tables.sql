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
CREATE INDEX i_master_german_word ON master(german_word);
CREATE INDEX i_master_frequency ON master(frequency);
CREATE INDEX i_master_difficulty ON master(difficulty);
CREATE INDEX i_master_partsofspeech ON master(partsofspeech);
                                

--
-- verb
--
CREATE TABLE IF NOT EXISTS verb (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        -- conjugation text,
                                        partsofspeech text
                                        
                                    );       

CREATE INDEX i_verb_german_word ON master(german_word);                                                      
--
-- conjunction
--
CREATE TABLE IF NOT EXISTS conjunction (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text
                                    );
CREATE INDEX i_conjunction_german_word ON master(german_word);                                    
-- CREATE TABLE conjunction AS SELECT german_word,english_word,partsofspeech FROM master where partsofspeech='conjunction';


CREATE TABLE IF NOT EXISTS noun (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        -- plural text,
                                        partsofspeech text
                                        
                                    );
CREATE INDEX i_noun_german_word ON master(german_word); 

-- CREATE TABLE noun AS SELECT german_word,english_word,partsofspeech FROM master where partsofspeech='noun';

CREATE TABLE IF NOT EXISTS sentence (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        -- plural text,
                                        partsofspeech sentence
                                        
                                    );
CREATE INDEX i_sentence_german_word ON master(german_word); 