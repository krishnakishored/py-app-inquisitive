import codecs
from io import open # for handling german umlauts

def build_word_dict_from_file(filename='./',delimiter=':',word_dictionary={}):
    # word_dictionary={}
    # todo : exception handling
    with open(filename,'r',encoding='utf8') as f_in:
        lines = [line.rstrip().lstrip() for line in f_in] # All lines including the blank ones
        lines = [line for line in lines if line] # Non-blank lines
        for line in lines:
            key_word = line[:line.find(delimiter)]
            value_word = line[line.find(delimiter)+1:len(line)]
            word_dictionary[key_word.rstrip()] = value_word.lstrip()
    return word_dictionary


def display_keyvalue_pairs(word_dictionary,delimiter=' - '):
    for k,v in word_dictionary.items():
        print(k+delimiter+v)

if __name__ == "__main__":
    pass