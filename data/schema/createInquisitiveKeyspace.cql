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
    "german_word" VARCHAR,
    "english_word" VARCHAR,
    "partsofspeech" ASCII,
    "plural" VARCHAR,
    "article" ASCII,
    "toughness" DECIMAL,
    "frequency" DECIMAL,
    "synonyms" VARCHAR,
    "antonyms" VARCHAR,
	PRIMARY KEY (("german_word"))
);

    -- "counter" COUNTER, //message="Cannot mix counter and non counter columns in the same table"


CREATE INDEX ON "tbl_deutsch" ("english_word");
CREATE INDEX ON "tbl_deutsch" ("partsofspeech");
CREATE INDEX ON "tbl_deutsch" ("toughness");
CREATE INDEX ON "tbl_deutsch" ("frequency");
