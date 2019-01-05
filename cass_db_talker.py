
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


# cluster = Cluster()

# cluster = Cluster(['192.168.0.1', '192.168.0.2'])  # You can also specify a list of IP addresses for nodes in your cluster:
# The set of IP addresses we pass to the Cluster is simply an initial set of contact points. 
# After the driver connects to one of these nodes it will automatically discover the rest of the nodes in the cluster and connect to them,  so you don’t need to list every node in your cluster.

# The connect() method takes an optional keyspace argument which sets the default keyspace for all queries made through that Session:
# session = cluster.connect('worte_liste') 

# session = cluster.connect('inquisitive') # keyspace

# You can always change a Session’s keyspace using set_keyspace() or by executing a USE query:
# session.execute("CREATE KEYSPACE worte_liste WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '1' };") 
# session.set_keyspace('worte_liste')
# session.execute('USE users') # or you can do this instead

#
# Executing Queries
# 




# Passing Parameters to CQL Queries

# When executing non-prepared statements, the driver supports two forms of parameter place-holders: positional and named.

# INSERT - Positional parameters are used with a %s placeholder. 
# Note that you should use %s for all types of arguments, not just strings. 
#  you must always use a sequence for the second argument - [], (), even if you are only passing in a single variable 

# Named place-holders use the %(name)s form:


def populate_db_from_file():
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


def get_session_with_defaults():
    cassConnection = CassandraConnection()
    #initialize
    ip_address = ["127.0.0.1"]
    cassConnection.cluster = Cluster(ip_address)
    cassConnection.keyspace = 'inquisitive'
    cassConnection.auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra') #security flaw - read from environment
    return cassConnection.create_session()


if __name__ == "__main__":

    # read these from a config or an environment
    
    # populate_db_from_file(session)
    runtime_wordlist = get_wordpairs_from_db(10)
    for word in runtime_wordlist:
        print(word.german,"=",word.english)
