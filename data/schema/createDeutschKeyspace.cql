//  
// Name:  createDeutschKeyspace.cql
//
//  

CREATE KEYSPACE IF NOT EXISTS "deutsch_fragen" WITH REPLICATION = {
 'class' : 'NetworkTopologyStrategy', 
 'datacenter1' : 1 // datacenter:datacenter1,  create 2 replicas
};

-- CREATE KEYSPACE IF NOT EXISTS "deutsch_fragen" WITH REPLICATION = {
--  'class' : 'NetworkTopologyStrategy', 
--  'us-east-1' : 2, // 1-a, 1-b // datacenter: us-east rack:1a,1b
--  'us-west-1' : 2, // 1-a, 1-b
--  'us-east-2' : 3 // 2-a, 2-b, 2-c // datacenter: us-east rack:2a,2b,2c
-- };


use "deutsch_fragen";

-- //Load the custom types into this keyspace.
-- source 'customtypes.cql';

CREATE TABLE tbl_worte_liste
(
	"german" VARCHAR,
	"english" VARCHAR,
    "partsofspeech" ASCII,
    -- "counter" COUNTER, //message="Cannot mix counter and non counter columns in the same table"
    "article" ASCII,
	PRIMARY KEY (("german"))
);

CREATE INDEX ON "tbl_worte_liste" ("english");
