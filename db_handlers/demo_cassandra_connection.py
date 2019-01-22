'''
https://datastax.github.io/python-driver/object_mapper.html#contents
'''

import logging
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster, BatchStatement
from cassandra.query import SimpleStatement
from cassandra.auth import PlainTextAuthProvider

class CassandraConnection:
    def __init__(self):
        self.cluster = None
        self.session = None
        self.keyspace = None
        self.log = None
        self.auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')#security flaw - read from environment


    # ToDo: read default values of ip_addr_list, keyspace from environment
    def assign_defaults(self,ip_addr_list=["localhost"],keyspace="default_keyspace"):
        '''
        1. set default logging level to INFO
        2. create a session - connecting to localhost with default credentials
        3. create a default_keyspace if it does not exists
        4. set the new keyspace

        '''
        self.setlogger()
        self.cluster = Cluster(ip_addr_list,auth_provider = self.auth_provider) # ToDo: how to pass list of strings as ip_addr
        self.session = self.cluster.connect()
        self.keyspace = keyspace
        # self.create_new_keyspace(self.keyspace) # create the default keyspace
        self.create_keyspace_if_not_exists(self.keyspace)
        self.session.set_keyspace(self.keyspace)

    def __del__(self):
        self.cluster.shutdown()


    # def create_session(self,ip_address=['localhost']):
    #     # self.cluster = Cluster(ip_address)
    #     self.session = self.cluster.connect(self.keyspace)
    #     # return self.cluster
    #     # self.session = self.cluster.connect(keyspace_name)


    def get_session(self):
        return self.session


    # How about Adding some log info to see what went wrong
    def setlogger(self,log_level='INFO'):
        log = logging.getLogger()
        log.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        log.addHandler(handler)
        self.log = log

    # Create new Keyspace based on Given Name
    def create_new_keyspace(self, keyspace):
        """
        :param keyspace:  The Name of Keyspace to be created
        :return:
        """
        # Before we create new lets check if exiting keyspace; we will drop that and create new
        rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if keyspace in [row[0] for row in rows]:
            self.log.info("dropping existing keyspace...")
            self.session.execute("DROP KEYSPACE " + keyspace)
        self.log.info("creating keyspace...")
        self.session.execute("""
                CREATE KEYSPACE %s WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' } """ % keyspace)
        self.log.info("setting keyspace...")
        self.session.set_keyspace(keyspace)


    def create_keyspace_if_not_exists(self, keyspace):
        """
        :param keyspace:  The Name of Keyspace to be created
        :return:
        """
        # Before we create new lets check if exiting keyspace; we will drop that and create new
        rows = self.session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
        if keyspace in [row[0] for row in rows]:
            self.log.info("found existing keyspace...")
        else:    
            self.log.info("creating new keyspace...")
            self.session.execute("""
                    CREATE KEYSPACE %s WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' } """ % keyspace)
        self.log.info("setting the keyspace...")
        self.session.set_keyspace(keyspace)

    def create_table(self):
        create_sql = """
                CREATE TABLE IF NOT EXISTS tbl_wordlist("german" VARCHAR, "english" VARCHAR,
                                              "partsofspeech" ASCII ,
                                              "article" ASCII,
                                              PRIMARY KEY(("german")));
                 """
        self.session.execute(create_sql)
        self.log.info("tbl_wordlist is Created !!!")

    # lets do some batch insert
    def insert_data(self):
        insert_sql = self.session.prepare("INSERT INTO  tbl_wordlist (german, english, partsofspeech, article) VALUES (?,?,?,?)")
        batch = BatchStatement()
        # list_of_dict = [{'Vielfalt':'variety'},{'achtgeben':'take care of'},{'abhängig':'dependent'},{'Absatz':'heel'}]
        # for pair in list_of_dict:
        #     for key in pair:
        #         batch.add(insert_sql,(key,pair(key)))

        batch.add(insert_sql, ('Vielfalt', 'variety', 'noun', 'die'))
        batch.add(insert_sql, ('achtgeben', 'take care of', 'thingummy', 'thingummy'))
        batch.add(insert_sql, ( 'abhängig', 'dependent','thingummy', 'thingummy'))
        batch.add(insert_sql, ( 'Absatz', 'heel','thingummy', 'thingummy'))
        self.session.execute(batch)
        self.log.info('Batch Insert Completed')


    def insert_dictionary_data(self,word_dictionary):
        batch = BatchStatement()
        insert_sql = self.session.prepare("INSERT INTO  tbl_wordlist (german, english, partsofspeech, article) VALUES (?,?,'thingummy','thingummy')")
        for german_word,english_word in word_dictionary.items():
            batch.add(insert_sql,(german_word, english_word)) # fill the default partsofspeech & article as 'thingummy'
        self.session.execute(batch)
        self.log.info('Batch Insert Completed')


    def select_data(self):
        rows = self.session.execute('SELECT german,english FROM tbl_wordlist limit 3;') # ToDo: - set the limit dynamically
        for row in rows:
            print(row.english+' -  '+row.german)


    def update_data(self):
        pass


    def delete_data(self):
        pass

if __name__ == '__main__':
    pass
    # print(cass_db_handler.get_session())
    # cassandra_handler.create_session()
    # example1 = PythonCassandraExample()
    # example1.createsession()
    # cass_handler.setlogger()
    # example1.createkeyspace('techfossguru')
    
    
