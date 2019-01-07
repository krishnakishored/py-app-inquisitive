//  Name:  createCustomTypes.cql
//
//  This module is the proprietary property of Telecommunication Systems, Inc.
//  Copyright (C) 2017 Telecommunications Systems, Inc.
//  All Rights Reserved


CREATE KEYSPACE IF NOT EXISTS "inquisitive" WITH REPLICATION = {
 'class' : 'NetworkTopologyStrategy', 
 'datacenter1' : 1 // datacenter:datacenter1,  create 2 replicas
};



use "inquisitive";

CREATE TABLE tbl_deutsch
(
    "id" uuid,
    "german_word" VARCHAR,
    "english_word" VARCHAR,
    "partsofspeech" ASCII,
    "plural" VARCHAR,
    "article" ASCII,
    "synonyms" VARCHAR,
    "antonyms" VARCHAR,
    "frequency" DECIMAL,     
    "toughness" DECIMAL,
	PRIMARY KEY (("id"))
);
CREATE INDEX ON "tbl_deutsch" ("german_word");    
CREATE INDEX ON "tbl_deutsch" ("english_word");
CREATE INDEX ON "tbl_deutsch" ("partsofspeech");
CREATE INDEX ON "tbl_deutsch" ("frequency");
CREATE INDEX ON "tbl_deutsch" ("toughness");


-- -- "counter" COUNTER, //message="Cannot mix counter and non counter columns in the same table"
-- CREATE TABLE tbl_analytics
-- (
--     "german_word" VARCHAR,
--     "frequency" COUNTER,
--     "toughness" COUNTER,
   
-- 	PRIMARY KEY (("german_word"))
-- );
-- -- "Secondary indexes are not supported on counter tables"

-- CREATE INDEX ON "tbl_analytics" ("toughness"); 
-- CREATE INDEX ON "tbl_analytics" ("frequency");
