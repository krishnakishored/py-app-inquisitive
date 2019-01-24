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
# from db_handlers.cassandra_db_handler import get_wordpairs_from_table, update_word_difficulty_freq

from db_handlers.sqlite_db_handler import get_wordpairs_from_table, capture_results


#ToDo: import 'difflib' to accept close matches
def compare_text(first,second):
    ''' works for unicode chars too'''
    return first.casefold().strip() == second.casefold().strip()

# interactive mode - choose "german" or "english"
def interactive_console_app(database, table, num_of_questions=10,guess="german"):
    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)

    runtime_wordlist = get_wordpairs_from_table(database,table,num_of_questions)

    question_number = 0
    results = {}
    if(compare_text(guess,"german")):
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}:{1}".format(question_number,word.english),end=" ")
            answer = str(input(" = "))
            # compare with nearest matches
            if(compare_text(word.german, answer)):
                results[word.german]=1
            elif (compare_text(answer, "")):
                results[word.german] = 0
                print("skip: {0}".format(word.german)) 
            else:
                results[word.german]=-1
                print("correct:{0}".format(word.german))  
    else:
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}: {1}".format(question_number,word.german),end=" ")
            answer = str(input(" = "))
            if (compare_text(word.english,answer)):
                results[word.german]= 1
            elif compare_text(answer,""):
                results[word.german] = 0
                print("skip: {0}".format(word.english)) 
            else:
                results[word.german]= -1
                print("correct:{0}".format(word.english))  
    report_card_app(results=results)# always updates master


# conduct the game as a quiz & evaluate


''' ToDo: Needs improvement w.r.t report card & two way quiz'''
def run_quiz_app(database, table, num_of_questions = 10, guess="german"):

    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)
    runtime_wordlist = get_wordpairs_from_table(database,table,num_of_questions)

    question_number = 0    
    # current_dictionary={}
    results = {}
    if(compare_text(guess,"german")):
        for word in runtime_wordlist:
            question_number = question_number+1
            
            print("{0}: {1}".format(question_number,word.english),end=" ")

            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if compare_text(word.german, answer):
                # results["rights"].append(word.german)
                results[word.german]= 1
            elif compare_text(answer,""):
                results[word.german] = 0
                print("skip: {0}".format(word.german)) 
            else:
                results[word.german]= -1
                print("correct: {0}".format(word.german)) 
    else:
        for word in runtime_wordlist:
            question_number = question_number+1
            
            print("{0}: {1}".format(question_number,word.german),end=" ")

            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if compare_text(word.english, answer):
                results[word.german]= 1
            elif compare_text(answer,""):
                results[word.german] = 0
                print("skip: {0}".format(word.english)) 
            else:
                results[word.german]= -1
                print("correct: {0}".format(word.english)) 

    report_card_app(results=results)# always updates master

def report_card_app(database='./data/sqlite3/inquisitive.db',table='master',results={}):
    '''
    displays results & writes back to db for analytics
    '''
    wrong,skip,right =  sum(value == -1 for value in results.values()), sum(value == 0 for value in results.values()), sum(value == 1 for value in results.values())
    print('wrong={0},right={1},skip={2}'.format(wrong,right,skip))
    capture_results(database,table,results)


if __name__ == "__main__":
    database = './data/sqlite3/inquisitive.db'
    table= 'master'
    # interactive_console_app(database,table,3,"english")
    run_quiz_app(database,table,3,"german")
    # print(compare_text("baße ","Basse"))