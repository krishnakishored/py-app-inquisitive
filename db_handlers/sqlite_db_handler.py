#
# Connecting to Sqlite
#
import sqlite3
from sqlite3 import Error

import sys
sys.path.append(sys.path[0] + "/..")  # To Fix: ValueError Attempted Relative Import Toplevel Package

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

def execute_generic_query(database,table,sql_statement):
	conn = create_connection(database)
	with conn:
		cur = conn.cursor()
		cur.execute(sql_statement)
		rows = cur.fetchall()
		# for row in rows:
		#     print(row)
		return rows

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


def update_freq_difficulty_mastertable(database, table, values):
	conn = create_connection(database)
	with conn:
		sql_update_freq_difficulty =  """ UPDATE {0} SET frequency = ?,difficulty= ? WHERE german_word= ? """.format(table)
		cur = conn.cursor()
		cur.execute(sql_update_freq_difficulty,values)
		return cur.lastrowid		

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
		
		

		'''
		# create tables
		'''
		# create_table(database,sql_create_tbl_conjunction)
		# create_table(database,sql_create_tbl_master) # ToDo - auto insert with insertion in any of the partsofspeech tables
		
		# value_tuple = ('bevor','before','conjunction')
		# insert_row_subtable(database,table, value_tuple)
		
		'''
		# execute queries
		# '''
		# sql_select_query = "SELECT german_word,english_word FROM verb where german_word LIKE 'ver%'"
		# rows = execute_generic_query(database,'verb',sql_select_query)
		# for row in rows:
		# 	print(row[0],'=',row[1])

		# sql_select_query = "SELECT german_word,english_word FROM sentence WHERE german_word LIKE 'Ich kann das nicht%';"
		# rows = execute_generic_query(database,'sentence',sql_select_query)
		# for row in rows:
		# 	print(row[0],'=',row[1])
	

		# select_all_rows(database,table)
		# select_random_questions(database,table,3)

		# runtime_wordlist = get_random_wordpairs(database,table,5)
		# for word in runtime_wordlist:
		#     print(word.german,"=",word.english)

		# delete_all_rows(database,table)