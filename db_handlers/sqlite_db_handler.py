#
# Connecting to Sqlite
#
import sqlite3
from sqlite3 import Error

import sys
sys.path.append(sys.path[0] + "/..")  # To Fix: ValueError Attempted Relative Import Toplevel Package


from utils.word import Word, build_word_dict_from_file
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        # conn = sqlite3.connect(':memory:') # it will create a new database that resides in the memory (RAM) instead of a database file on disk.
        # print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
        # conn.close() # do not do it!!
    return None


def create_table(database='./data/sqlite3/inquisitive.db', sql_create_table=''):
    '''
    take db & create table sql as args
    '''
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
        except Error as e:
            print(e)
    else:
        print("Error! cannot create the database connection.")

def delete_all_rows(database,table):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql_delete_all_rows =  'DELETE FROM ' + table
        cur = conn.cursor()
        cur.execute(sql_delete_all_rows)

def select_all_rows(database,table):
    conn = create_connection(database)
    with conn:
        sql_select_all_rows =  'SELECT * FROM ' + table
        cur = conn.cursor()
        cur.execute(sql_select_all_rows)
        rows = cur.fetchall()
        for row in rows:
            print(row)

def insert_row_subtable(database, table, values):
    conn = create_connection(database)
    with conn:
        sql_insert_row =  'INSERT INTO '  + table+ '(german_word,english_word,partsofspeech) VALUES(?,?,?)'
        cur = conn.cursor()
        cur.execute(sql_insert_row,values)
        return cur.lastrowid

def populate_db_from_file(database='./data/sqlite3/inquisitive.db',table='conjunction', filename='./data/german_english.txt',delimiter=':'):
    '''
    ToDo: populate the tbl_deutsch w.r.t any insertion into the partsofspeech tables as auto-sync
    read from a text file and insert into to the database
    '''

    word_dictionary = build_word_dict_from_file(filename,delimiter)
    for ger,eng in word_dictionary.items():
        value_tuple  = (ger,eng,'conjunction')
        insert_row_subtable(database,table, value_tuple)

def get_wordpairs_from_db(question_count=10,):
    ''' returns a list of word objects reading from the database'''  
    pass

    # wordpair_list = []
    # # where(gte('frequency',1)) message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
    # # statement_select_words = (QueryBuilder.select_from("tbl_deutsch").columns('german_word', 'english_word').limit(question_count))

    # # random_uniqueId = uuid.uuid4() # Random
    # #To get random set of words
    # ticks = time.time()
    # rand_time = lambda: float(random.randrange(0,10000)+ticks)
    # random_uniqueId = uuid.uuid5(uuid.NAMESPACE_DNS,str(rand_time()))

    # statement_select_words = "SELECT german_word,english_word FROM tbl_deutsch WHERE id>%s LIMIT %s ALLOW FILTERING"
    # future = session.execute_async(statement_select_words, [random_uniqueId,question_count])

    # try:
    #     rows = future.result()
    #     for row in rows:
    #        current_word = Word(row.german_word,row.english_word)
    #        wordpair_list.append(current_word)
    # except ReadTimeout:
    #     log.exception("Query timed out:")
    
    # return wordpair_list




if __name__ == '__main__':
    database = './data/sqlite3/inquisitive.db'
    table= 'conjunction'

    sql_create_tbl_deutsch = """ CREATE TABLE IF NOT EXISTS tbl_deutsch (
                                        id integer PRIMARY KEY,
                                        german_word text NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text,
                                        frequency integer,
                                        toughness integer
                                    ); """
    
    sql_create_tbl_conjunction = """ CREATE TABLE IF NOT EXISTS conjunction (
                                        id integer PRIMARY KEY,
                                        german_word text NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text
                                    ); """

    create_table(database,sql_create_tbl_conjunction)
    # create_table(database,sql_create_tbl_deutsch) # ToDo - auto insert with insertion in any of the partsofspeech tables
    
    # value_tuple = ('bevor','before','conjunction')
    # insert_table_sub(database,table_name, value_tuple)
    # insert_row_subtable(database,table, value_tuple)
    

    populate_db_from_file(database,table,filename='./data/conjunction.txt',delimiter=':')
    select_all_rows(database,table)
    delete_all_rows(database,table)