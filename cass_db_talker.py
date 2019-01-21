
#
# Connecting to Cassandra
#
import logging
from cassandra.auth import PlainTextAuthProvider

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement

from cql_builder.builder import QueryBuilder
from cql_builder.condition import eq,lte,gte
from cassandra import ReadTimeout

import uuid

from word import Word, build_word_dict_from_file

class CassandraConnection:
    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = None
        self.log = None
        self.auth_provider = None
    
    # @classmethod
    def create_session(self,ip_address=['localhost']):
        self.cluster = Cluster(ip_address)
        self.session = self.cluster.connect(self.keyspace)
        return self.session
        # return self.cluster
        # self.session = self.cluster.connect(keyspace_name)


def get_session_with_defaults():
    cassConnection = CassandraConnection()
    #initialize
    ip_address = ["127.0.0.1"] # You can also specify a list of IP addresses for nodes in your cluster:
    cassConnection.cluster = Cluster(ip_address)
    cassConnection.keyspace = 'inquisitive'
    cassConnection.auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra') #security flaw - read from environment
    return cassConnection.create_session()

def populate_db_from_file(filename='./data/german_english.txt',delimiter=':'):
    '''
    read from a text file and insert into to the database
    '''
    # create a session with defaults
    session = get_session_with_defaults()

    # statement_insert_word = session.prepare("INSERT INTO tbl_deutsch (german_word, english_word, partsofspeech) VALUES (?,?,?)")
    # filename='./data/german_english.txt'
    # delimiter=":"

    word_dictionary = build_word_dict_from_file(filename,delimiter)
    
    # word_count = len(word_dictionary.keys())
    # batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM) # batch too large
    for ger,eng in word_dictionary.items():
        # batch.add(statement_insert_word,(ger,eng)) # batch too large
        uniqueId = uuid.uuid5(uuid.NAMESPACE_DNS, ger)
        statement_insert_word = (QueryBuilder.insert_into("tbl_deutsch").values(id=uniqueId, german_word=ger, english_word=eng, frequency=0,toughness=0))
        query, args = statement_insert_word.statement()
        session.execute(query, args)

    # session.execute(batch) # batch too large

def get_wordpairs_from_db(question_count=10,):
    ''' returns a list of word objects reading from the database'''

    # create a session with defaults
    session = get_session_with_defaults()
    
    wordpair_list = []
    # where(gte('frequency',1)) message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
    # statement_select_words = (QueryBuilder.select_from("tbl_deutsch").columns('german_word', 'english_word').limit(question_count))

    # random_uniqueId = uuid.uuid4() # Random
    #To get random set of words
    ticks = time.time()
    rand_time = lambda: float(random.randrange(0,10000)+ticks)
    random_uniqueId = uuid.uuid5(uuid.NAMESPACE_DNS,str(rand_time()))

    statement_select_words = "SELECT german_word,english_word FROM tbl_deutsch WHERE id>%s LIMIT %s ALLOW FILTERING"
    future = session.execute_async(statement_select_words, [random_uniqueId,question_count])

    try:
        rows = future.result()
        for row in rows:
           current_word = Word(row.german_word,row.english_word)
           wordpair_list.append(current_word)
    except ReadTimeout:
        log.exception("Query timed out:")
    
    return wordpair_list


# update the fields
def update_word_toughness_freq(results):
    '''
    takes a map of words, word:-1 or +1 for incorrect
     set frequency = frequency + 1 
     set toughness = toughness +1 or -1
    '''
    # create a session with defaults
    session = get_session_with_defaults()

    
    for word,value in results.items():
        # get freq & toughness    
        uniqueId = uuid.uuid5(uuid.NAMESPACE_DNS,word)
        select_query = "SELECT frequency,toughness FROM tbl_deutsch WHERE id=%s"
        future = session.execute_async(select_query, [uniqueId])
        try:
            rows = future.result()
            row = rows.one()
            # print (user.frequency, user.toughness)
            word_frequency,word_toughness =  row.frequency,row.toughness
            # print(word_frequency,": ",word_toughness)
        except ReadTimeout:
            log.exception("Query timed out:")

        # print(word_frequency+1,word_toughness+value,word)


        update_query = "UPDATE tbl_deutsch SET frequency=%s,toughness=%s WHERE id=%s"
        future = session.execute_async(update_query, [word_frequency+1,word_toughness+value,uniqueId])
        try:
            rows = future.result()
        except ReadTimeout:
            log.exception("Query timed out:")
# delete rows



import random, time

if __name__ == "__main__":

    filename='./data/german_english.txt'
    delimiter=":"
    populate_db_from_file(filename,delimiter)
    
    runtime_wordlist = get_wordpairs_from_db(5)
    for word in runtime_wordlist:
        print(word.german,"=",word.english)
    
    # results={'Goldstaub':1}
    # update_word_toughness_freq(results)
   


#notes

# https://github.com/jjengo/cql-builder