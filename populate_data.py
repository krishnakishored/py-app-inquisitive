'''
1. Fill the database tables
2. To Supply data to the game runtime
3. Parts of speech tables are filled individually. Master tables gets filled with game results
'''

from db_handlers.sqlite_db_handler import create_connection, insert_row_subtable, insert_row_mastertable,  select_freq_difficulty_mastertable, update_freq_difficulty_mastertable, execute_generic_query
from utils.word import Word, build_word_dict_from_file

def select_random_questions(database,table, question_count):
	conn = create_connection(database)
	with conn:
		sql_select_random_rows = '''SELECT german_word, english_word FROM {0} ORDER BY RANDOM() LIMIT {1}'''.format(table, question_count)
		cur = conn.cursor()
		cur.execute(sql_select_random_rows)
		rows = cur.fetchall()
		return rows

def get_random_wordpairs(database, table ,question_count):
	''' returns a list of random word objects'''  
	wordpair_list = []
	rows_tuple = select_random_questions(database,table,question_count)   
	for row in rows_tuple:
		current_word = Word(row[0],row[1])
		wordpair_list.append(current_word)
	return wordpair_list

def get_selected_wordpairs(database, table, question_count, sql_select_statement):
	''' returns a list of word objects based on a select..where statement '''  
	wordpair_list = []
	# sql_select_query = "SELECT german_word,english_word FROM verb where german_word LIKE 'ver%'"
	rows_tuple = execute_generic_query(database,table,sql_select_statement)   
	for row in rows_tuple:
		current_word = Word(row[0],row[1])
		wordpair_list.append(current_word)
	return wordpair_list

def populate_table_from_file(database,tablename,filename,delimiter=':'):
	'''
	read from a text file and insert into the master table
	'''
	word_dictionary = build_word_dict_from_file(filename,delimiter)
	for ger,eng in word_dictionary.items():
		value_tuple  = (ger,eng,tablename)# 'table' name matches partsofspeech
		insert_row_subtable(database,tablename,value_tuple)
		# if(table == 'master'):
		# 	insert_row_mastertable(database,'master',value_tuple)
		# else:
		# 	insert_row_subtable(database,table,value_tuple)


def populate_subtables(database, table_file_dictionary,delimiter):
	'''
	 	1. accept a dictionary of {tablename_1:filename_1} items & populate all the tables
		2. iterate over the dictionary items & invokes   populate_table_from_file()
	'''
	for tablename,filename in table_file_dictionary.items():
		populate_table_from_file(database,tablename,filename, delimiter)

def capture_results(database,table,word_list):
	'''
	takes a map of words, word:-1 or +1 for incorrect
	 set frequency = frequency + 1 
	 set difficulty = difficulty +1 or -1

	 select freq  & difficulty & update the fields from values of the results
	 
	'''
	
	update_sql= "UPDATE master SET frequency=?, difficulty=? WHERE german_word=?"
	select_sql= "SELECT frequency, difficulty FROM master WHERE german_word=?"
	insert_sql = "INSERT OR IGNORE INTO master(german_word, english_word, partsofspeech,frequency,difficulty) values (?,?,?,0,0)"
	update_values = (2,3,'zu')
	insert_values = ('zu','to','preposition')
	result = execute_generic_query(database,'master',update_sql,update_values)
	if not result:
		print(execute_generic_query(database,'master',insert_sql, insert_values))

	for word in word_list:
		insert_values = ('zu','to','preposition')
		execute_generic_query(database,'master',insert_sql, insert_values)
		row = execute_generic_query(database,table,select_sql,(word.german,))
		print(row)
		word_frequency,word_difficulty =  row[0][0],row[0][1]
		update_values = (2,3,'zu')
		execute_generic_query(database,'master',update_sql,update_values)

	# for word,value in results.items():
	# 	row = select_freq_difficulty_mastertable(database,table,word) # returns a tuple list
	# 	#check if row is empty
	# 	word_frequency,word_difficulty =  row[0][0],row[0][1]
	# 	values = (word_frequency+1,word_difficulty+value,word)
	# 	update_freq_difficulty_mastertable(database,table,values)




if __name__ == "__main__":
	
	database = './data/sqlite3/inquisitive.db'

	'''
	# Populate tables
	'''
	table_file_dictionary = {
		'sentence': './data/sentence.txt',
		'noun': './data/noun.txt', 
		'verb': './data/verb.txt',
		'preposition': './data/preposition.txt',
		'conjunction': './data/conjunction.txt'	
	}	
	delimiter= ":"
	# populate_subtables(database,table_file_dictionary,delimiter)


	'''
	# Random Selections
	'''
	# question_count=4
	# table= 'sentence'
	# rows = select_random_questions(database,table,question_count)
	
	'''
	# Capture results
	'''
	# update_sql= "UPDATE master SET frequency=?, difficulty=? WHERE german_word=?"
	# insert_sql = "INSERT OR IGNORE INTO master(german_word, english_word, partsofspeech,frequency,difficulty) values (?,?,?,0,0)"
	# update_values = (20,30,'zu')
	# insert_values = ('zu','to','preposition')
	# result = execute_generic_query(database,'master',update_sql,update_values)
	# if not result:
	# 	print(execute_generic_query(database,'master',insert_sql, insert_values))
