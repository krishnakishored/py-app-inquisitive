
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

def populate_db_from_file():
    '''
    read from a text file and insert into to the database
    '''
    # create a session with defaults
    session = get_session_with_defaults()

    # statement_insert_word = session.prepare("INSERT INTO tbl_deutsch (german_word, english_word, partsofspeech) VALUES (?,?,?)")
    filename='./data/german_english.txt'
    delimiter=":"

    word_dictionary = build_word_dict_from_file(filename,delimiter)
    
    # word_count = len(word_dictionary.keys())
    # batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM) # batch too large
    for ger,eng in word_dictionary.items():
        # batch.add(statement_insert_word,(ger,eng)) # batch too large
        statement_insert_word = (QueryBuilder.insert_into("tbl_deutsch").values(german_word=ger, english_word=eng))
        query, args = statement_insert_word.statement()
        session.execute(query, args)

    # session.execute(batch) # batch too large

def get_wordpairs_from_db(question_count=10,):
    ''' returns a list of word objects reading from the database'''

    # create a session with defaults
    session = get_session_with_defaults()
    
    wordpair_list = []
    
    statement_select_words = (QueryBuilder.select_from("tbl_deutsch").columns('german_word', 'english_word').limit(question_count))

    query, args = statement_select_words.statement()
    rows = session.execute(query,args)
    for row in rows:
        current_word = Word(row.german_word,row.english_word)
        # print(row.german_word,":",row.english_word)
        # current_word.german_word = row.german_word
        # current_word.english_word = row.english_word
        wordpair_list.append(current_word)
    return wordpair_list


# update the fields

# delete rows



if __name__ == "__main__":
    # populate_db_from_file(session)
    runtime_wordlist = get_wordpairs_from_db(10)
    for word in runtime_wordlist:
        print(word.german,"=",word.english)
