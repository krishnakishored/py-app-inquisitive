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
    print('wrong={0},right={1},skip={2}'.format(wrong,right,skip))
    capture_results(database,table,word_list)

if __name__ == "__main__":
    database = './data/sqlite3/inquisitive.db'
    table= 'verb' # can specify a partsofspeech table name or master
    
    '''
    interactive 
    '''
    # select_query= "SELECT german_word,english_word FROM noun LIMIT 5"
    # num_of_questions = 5
    # interactive_console_app(database, table,num_of_questions,guess="german", sql_statement=select_query)
    

    '''
    quiz
    '''
    run_quiz_app(database,'preposition',5,'german')
    # print(compare_text("baße ","Basse"))
    
    



    # run_quiz_app(database,table,5,"english")