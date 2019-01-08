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

from word import get_wordpairs_from_file
from cass_db_talker import CassandraConnection, get_wordpairs_from_db, update_word_toughness_freq

# get the runtime question_list

# interactive mode - choose "german" or "english"
def interactive_console_app(num_of_questions=10,guess="german"):
    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)

    runtime_wordlist = get_wordpairs_from_db(num_of_questions)

    question_number = 0
    results = {}
    if(guess=="german"):
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}: {1}".format(question_number,word.english),end=" ")
            answer = str(input(" = "))
            # compare with nearest matches
            if(word.german.strip() == answer.strip()):
                results[word.german]=1
            elif(answer.strip()==""):
                results[word.german] = 0
                print("pass: {0}".format(word.german)) 
            else:
                results[word.german]=-1
                print("correct ans:{0}".format(word.german))  
    else:
        for word in runtime_wordlist:
            question_number = question_number+1    
            print("{0}: {1}".format(question_number,word.german),end=" ")
            answer = str(input(" = "))
            if(word.english.strip() == answer.strip()):
                results[word.german]= 1
            elif(answer.strip()==""):
                results[word.german] = 0
                print("pass: {0}".format(word.english)) 
            else:
                results[word.german]= -1
                print("correct ans:{0}".format(word.english))  
    report_card_app(results)


# conduct the game as a quiz & evaluate


''' ToDo: Needs improvement w.r.t report card & two way quiz'''
def run_quiz_app(num_of_questions = 10, guess="german"):

    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)
    runtime_wordlist = get_wordpairs_from_db(num_of_questions)

    question_number = 0    
    # current_dictionary={}
    results = {}
    if(guess=="german"):
        for word in runtime_wordlist:
            question_number = question_number+1
            
            print("{0}: {1}".format(question_number,word.english),end=" ")

            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if(word.german.strip() == answer.strip()):
                # results["rights"].append(word.german)
                results[word.german]= 1
            elif(answer.strip()==""):
                results[word.german] = 0
                print("pass: {0}".format(word.german)) 
            else:
                results[word.german]= -1
                print("correct ans: {0}".format(word.german)) 
    else:
        for word in runtime_wordlist:
            question_number = question_number+1
            
            print("{0}: {1}".format(question_number,word.german),end=" ")

            answer = str(input(" = "))
            #ToDo: write a method to compare with nearest matches
            if(word.english.strip() == answer.strip()):
                # results["rights"].append(word.german)
                results[word.german]= 1
            elif(answer.strip()==""):
                results[word.german] = 0
                print("pass: {0}".format(word.english)) 
            else:
                results[word.german]= -1
                print("correct ans: {0}".format(word.english)) 

    report_card_app(results)

def report_card_app(results):
    '''
    displays results & writes back to db for analytics
    '''

    wrongs = [i for i in results.values() if i==-1]
    print("wrong answers:{0}/{1}".format(len(wrongs),len(results)))
    update_word_toughness_freq(results)

# push the result data to DB for analysis - ToDo
if __name__ == "__main__":
    # interactive_console_app(3,"german")
    run_quiz_app(5,"english")

