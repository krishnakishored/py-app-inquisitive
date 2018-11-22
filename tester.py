from  utils.io_handling import build_word_dict_from_file, display_keyvalue_pairs
from models.cassandra_connection import CassandraConnection


if __name__ == "__main__":
    
    filename = './data/german_english.txt'
    word_dictionary={}#may use a existing dictionary also - appends to the items
    delimiter=':'
    build_word_dict_from_file(filename,delimiter,word_dictionary)
    
    # display_keyvalue_pairs(word_dictionary)


    cass_handler = CassandraConnection()
    cass_handler.assign_defaults()
    # cass_handler.create_table()
    # cass_handler.insert_data()
    # cass_handler.insert_dictionary_data(word_dictionary)
    cass_handler.select_data()
