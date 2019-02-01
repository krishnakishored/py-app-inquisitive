'''

Game runtime 
- 1. config from yaml or json: 
- 2. Types of game: 
    - Interactive
    - Quiz
- 3. Select words based on 
        - random (query can be a join - like select  random words where toughIndex is low or frequency is high)
        - frequency
        - toughIndex
        - partsofspeech
        - meaning

'''
import sys
sys.path.append(sys.path[0] + "/..")  # To Fix: ValueError Attempted Relative Import Toplevel Package


from utils.word import get_wordpairs_from_file
# from db_handlers.cassandra_db_handler import get_random_wordpairs, update_word_difficulty_freq
from populate_data import capture_results, get_random_wordpairs, get_selected_wordpairs


#ToDo: import 'difflib' to accept close matches
def compare_text(first,second):
    ''' works for unicode chars too'''
    return first.casefold().strip() == second.casefold().strip()


''' ToDo: Needs improvement w.r.t report card & two way quiz'''
def run_quiz_app(database, table, num_of_questions = 10, guess="german"):
    '''
    Picks random words for the quiz
    '''

    runtime_wordlist = get_random_wordpairs(database,table,num_of_questions)
    question_number = 0    
    
    if(compare_text(guess,"german")):
        for word in runtime_wordlist:
            question_number = question_number+1            
            print("{0}: {1}".format(question_number,word.english),end=" ")
            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if compare_text(word.german, answer):
                word.veracity = 1
            elif compare_text(answer,""):
                word.veracity = 0
                print("skip: {0}".format(word.german)) 
            else:
                word.veracity = -1
                print("====> {0}".format(word.german)) 
    else:
        for word in runtime_wordlist:
            question_number = question_number+1
            
            print("{0}: {1}".format(question_number,word.german),end=" ")

            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if compare_text(word.english, answer):
                word.veracity = 1
            elif compare_text(answer,""):
                word.veracity = 0
                print("skip: {0}".format(word.english)) 
            else:
                word.veracity = -1
                print("====> {0}".format(word.english)) 
    report_card_app(database,table,runtime_wordlist)# always updates master


# interactive mode - choose "german" or "english"
def interactive_console_app(database, table, num_of_questions,guess, sql_statement):
    '''
        Selects a list of words based on the given query
    '''
    
    runtime_wordlist = get_selected_wordpairs(database,table,num_of_questions,sql_statement)

    question_number = 0
    results = {}
    if(compare_text(guess,"german")):
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}:{1}".format(question_number,word.english),end=" ")
            answer = str(input(" = "))
            # compare with nearest matches
            if(compare_text(word.german, answer)):
                # results[word.german]=1
                word.veracity = 1
            elif (compare_text(answer, "")):
                # results[word.german] = 0
                word.veracity = 0
                print("skip: {0}".format(word.german)) 
            else:
                # results[word.german]=-1
                word.veracity = -1
                print("====> {0}".format(word.german))  
    else:
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}: {1}".format(question_number,word.german),end=" ")
            answer = str(input(" = "))
            if (compare_text(word.english,answer)):
                # results[word.german]= 1
                word.veracity = 1
            elif compare_text(answer,""):
                # results[word.german] = 0
                word.veracity = 0
                print("skip: {0}".format(word.english)) 
            else:
                # results[word.german]= -1
                word.veracity = -1
                print("====> {0}".format(word.english))  
    report_card_app(database,table,runtime_wordlist)# always updates master


def report_card_app(database,table,word_list):
    '''
    displays results & writes back to db for analytics
    '''
    wrong = sum(word.veracity ==-1 for word in word_list)
    skip = sum(word.veracity == 0 for word in word_list)
    right = sum(word.veracity == 1 for word in word_list)
    print('wrong={0},right={1},skip={2} in {3}'.format(wrong,right,skip, table))
    capture_results(database,table,word_list)



import argparse

def run_inquisitive_with_args(*args,**kwargs):
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='inquisitive app')
    
    parser.add_argument("-m","--mode", help="choose (i)nteractive or (q)uiz ",default="q")
    parser.add_argument("-t","--type", help="choose parts of speech - sentence, verb, noun, preposition, .. ",default="sentence")
    parser.add_argument("-n","--count", help="choose no.of questions",type=int,default=5)
    parser.add_argument("-db","--database", help="select the database",default='./data/sqlite3/inquisitive.db')
    args = parser.parse_args()


    # table = args['type']
    table = args.type
    num_of_questions = args.count
    database = args.database

    print(args)
    if(args.mode=='i'): #     interactive : a specific query with 'where' clause to select the choice of questions
        #  select_query= "SELECT german_word,english_word FROM {0} LIMIT {1}".format(table,num_of_questions)
        select_query= "SELECT german_word,english_word FROM {0} ORDER BY RANDOM() LIMIT {1}".format(table,num_of_questions)
        interactive_console_app(database, table,num_of_questions,guess="english", sql_statement=select_query)
    else:
         #quiz based on random selection
        # run_quiz_app(database,table,num_of_questions,"english")
        run_quiz_app(database,table,num_of_questions,"german")
    


if __name__ == "__main__":
    run_inquisitive_with_args()


    # #defaults
    # database = './data/sqlite3/inquisitive.db'
    # game_mode = "quiz"
    # table= 'noun' # can specify a partsofspeech table name or master
    # num_of_questions = 3

    

    # if(game_mode=='quiz'):
    #     '''
    #     quiz based on random selection
    #     '''
    #     # run_quiz_app(database,table,num_of_questions,"english")
    #     run_quiz_app(database,table,num_of_questions,"german")
    # else:    
    #     '''
    #     interactive 
    #     # a specific query with 'where' clause to select the choice of questions
    #     '''
    #     #  select_query= "SELECT german_word,english_word FROM {0} LIMIT {1}".format(table,num_of_questions)
    #     select_query= "SELECT german_word,english_word FROM {0} ORDER BY RANDOM() LIMIT {1}".format(table,num_of_questions)
    #     interactive_console_app(database, table,num_of_questions,guess="english", sql_statement=select_query)
        
    
   