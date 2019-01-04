'''
class for a german word
    - deutsch word
    - english word
    - parts of speech
    - plural
    - article
    - toughIndex
    - frequency
    - synonyms
    - antonyms
    - criteria : tech, edu, food, weather

'''


'''

'''

import random

class Word:
    """ Word class represents a german-english pair """

    def __init__(self, german="", english="", article=""):
        """ Create a new word """
        self.german = german
        self.english = english
        self.article = article


'''
populate a list of (key,value) for the quiz
- read from a file - words separated by delimiters
- read from a database
    - random list ?
    - based on a select criteria

'''
# /Users/kishored/coding/python-coding/py-app-inquisitive/data/german_english.txt

def build_word_dict_from_file(filename='./data/german_english.txt',delimiter=':',word_dictionary={}):
    '''
        reads german:english pairs from files and returns a dictionary of words
    '''
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

'''
populate the runtime question list
'''

def get_wordpairs_for_quiz(num_of_questions=10):
    ''' returns a list of word objects'''
    full_wordlist = build_word_dict_from_file()
    wordpair_list = []
    # #populate all the pairs
    german_english_pairs = build_word_dict_from_file()
    
    for n in range(num_of_questions):
        current_word = Word()
        current_word.german,current_word.english = random.choice(list(german_english_pairs.items()))
        wordpair_list.append(current_word)
    return wordpair_list



if __name__ == "__main__":
    word_1 = Word("abstammen von", "descend from")
    word_2 = Word("abstauben","dust")
    word_3 = Word("abstimmen", "vote")
    # print(word_2.german,":",word_2.english)
    word_list = []
    #replace this with a loop
    word_list.append(word_1)
    word_list.append(word_2)
    word_list.append(word_3)
    
    

    # # choose random (german,english) for the quiz
    # k,v = random.choice(list(german_english_pairs.items()))
    # print(k,v)
    # k,v = random.choice(list(german_english_pairs.items()))
    # print(k,v)
    
    # keys = random.choice(list(german_english_pairs.keys()))
    # print(keys)
    # values = random.choice(list(german_english_pairs.values()))
    # print(values)

    
    # # print (german=english) pairs
    runtime_wordlist = get_wordpairs_for_quiz()
    for word in runtime_wordlist:
        print(word.german,"=",word.english)







        
        