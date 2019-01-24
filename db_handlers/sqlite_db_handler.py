#
# Connecting to Sqlite
#
import sqlite3
from sqlite3 import Error

import sys
sys.path.append(sys.path[0] + "/..")  # To Fix: ValueError Attempted Relative Import Toplevel Package


from utils.word import Word, build_word_dict_from_file
 
def create_connection(database):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(database)
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

def select_random_questions(database,table='conjunction', question_count=10):
    conn = create_connection(database)

    with conn:
        sql_select_random_rows = '''SELECT german_word, english_word FROM {0} ORDER BY RANDOM() LIMIT {1}'''.format(table, question_count)
        cur = conn.cursor()
        cur.execute(sql_select_random_rows)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
        return rows

def select_freq_difficulty_mastertable(database,table='master',where_key=''):
    conn = create_connection(database)

    with conn:
        sql_select_freq_difficulty = ''' SELECT frequency, difficulty FROM {0} WHERE german_word=?  '''.format(table)
        cur = conn.cursor()
        cur.execute(sql_select_freq_difficulty,(where_key,)) # pass it as tuple; To Fix: Incorrect number of bindings supplied. The current statement uses 1, and there are 4 supplied.
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
        return rows        

def insert_row_subtable(database, table, values):
    conn = create_connection(database)
    with conn:
        # sql_insert_row =  'INSERT INTO '  + table+ '(german_word,english_word,partsofspeech) VALUES(?,?,?)'
        sql_insert_row =  """ INSERT INTO {0} (german_word,english_word,partsofspeech) VALUES(?,?,?) """.format(table)
        cur = conn.cursor()
        cur.execute(sql_insert_row,values)
        return cur.lastrowid

def insert_row_mastertable(database, table, values):
    conn = create_connection(database)
    with conn:
        sql_insert_row =  """ INSERT INTO {0} (german_word,english_word,partsofspeech,frequency,difficulty) VALUES(?,?,?,0,0) """.format(table)
        cur = conn.cursor()
        cur.execute(sql_insert_row,values)
        return cur.lastrowid

def populate_db_from_file(database='./data/sqlite3/inquisitive.db',table='master', filename='',delimiter=':'):
    '''
    read from a text file and insert into to the master table
    '''
    word_dictionary = build_word_dict_from_file(filename,delimiter)
    for ger,eng in word_dictionary.items():
        value_tuple  = (ger,eng,table)
        insert_row_mastertable(database,'master',value_tuple)


def populate_subtables_from_master(database='./data/sqlite3/inquisitive.db',subtable='conjunction', filename='',delimiter=':'):
	'''
		ToDo: populate the subtables(partsofspeech tables) w.r.t any insertion into the master
	'''
	pass
def get_wordpairs_from_table(database= './data/sqlite3/inquisitive.db', table='conjunction',question_count=10):
    ''' returns a list of word objects reading from the database'''  
    wordpair_list = []
    rows_tuple = select_random_questions(database,table,question_count)   
    for row in rows_tuple:
        current_word = Word(row[0],row[1])
        wordpair_list.append(current_word)
    return wordpair_list

def update_freq_difficulty_mastertable(database, table, values):
    conn = create_connection(database)
    with conn:
        sql_update_freq_difficulty =  """ UPDATE {0} SET frequency = ?,difficulty= ? WHERE german_word= ? """.format(table)
        cur = conn.cursor()
        cur.execute(sql_update_freq_difficulty,values)
        return cur.lastrowid

def capture_results(database,table,results={}):
    '''
    takes a map of words, word:-1 or +1 for incorrect
     set frequency = frequency + 1 
     set difficulty = difficulty +1 or -1

     select freq  & difficulty & update the fields from values of the results
    '''
    for word,value in results.items():
        row = select_freq_difficulty_mastertable(database,table,word) # returns a tuple
        word_frequency,word_difficulty =  row[0][0],row[0][1]
        values = (word_frequency+1,word_difficulty+value,word)
        update_freq_difficulty_mastertable(database,table,values)
    

if __name__ == '__main__':
	database = './data/sqlite3/inquisitive.db'
    # table= 'noun'
    # filename='./data/noun.txt'
	# table = 'verb'
	# filename='./data/verb.txt'
	# table='conjunction'
	# filename='./data/conjunction.txt'

	sql_create_tbl_master = """ CREATE TABLE IF NOT EXISTS master (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text,
                                        frequency integer,
                                        difficulty integer
                                    ); """
    
	sql_create_tbl_conjunction = """ CREATE TABLE IF NOT EXISTS conjunction (
                                        id integer PRIMARY KEY,
                                        german_word text UNIQUE NOT NULL,
                                        english_word text NOT NULL,
                                        partsofspeech text
                                    ); """

    # create_table(database,sql_create_tbl_conjunction)
    # create_table(database,sql_create_tbl_master) # ToDo - auto insert with insertion in any of the partsofspeech tables
    
    # value_tuple = ('bevor','before','conjunction')
    # insert_row_subtable(database,table, value_tuple)
    

	# populate_db_from_file(database,table,filename,delimiter=':')
	populate_db_from_file(database,'noun','./data/noun.txt',delimiter=':')
	populate_db_from_file(database,'verb','./data/verb.txt',delimiter=':')
	populate_db_from_file(database,'conjunction','./data/conjunction.txt',delimiter=':')

    # select_all_rows(database,table)
    # select_random_questions(database,table,3)

    # runtime_wordlist = get_wordpairs_from_table(database,table,5)
    # for word in runtime_wordlist:
    #     print(word.german,"=",word.english)

    # capture_results(database,table)
    # delete_all_rows(database,table)