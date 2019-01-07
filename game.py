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

# interactive mode
def interactive_console_app(num_of_questions=10):
    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)

    runtime_wordlist = get_wordpairs_from_db(num_of_questions)

    question_number = 0
    answers = {}

    for word in runtime_wordlist:
        question_number = question_number+1
        print("{0}: {1}".format(question_number,word.german),end=" ")
        answer = str(input(" = "))
        # compare with nearest matches
        if(word.english.strip() == answer.strip()):
            answers[question_number]=1
        else:
            answers[question_number]=0
            print("the right answer:{0}".format(word.english))  


# conduct the game as a quiz & evaluate



''' ToDo: Needs improvement w.r.t report card & two way quiz'''
def run_quiz_app(num_of_questions = 10):

    # runtime_wordlist = get_wordpairs_from_file(num_of_questions)
    runtime_wordlist = get_wordpairs_from_db(num_of_questions)

    question_number = 0    
    current_dictionary={}
    results = {}

    print("Enter the word which matches the following definition")

    for word in runtime_wordlist:
        question_number = question_number+1
        
        current_dictionary[word.german]=word.english
        print("{0}: {1}".format(question_number,word.german),end=" ")
        answer = str(input(" = "))
        #ToDo: write a method to compare with nearest matches
        if(word.english.strip() == answer.strip()):
            # results["rights"].append(word.german)
            results[word.german]= 1
        else:
            results[word.german]= -1
            print("correct answer: {0}".format(word.english)) 
    
    # results[1] = rights
    # results[0] = wrongs
    report_card_app(results)

def report_card_app(results):
    '''
    displays results & writes back to db for analytics
    '''

    wrongs = [i for i in results.values() if i==-1]
    print("wrong answers:{0}/{1}".format(len(wrongs),len(results)))
    update_word_toughness_freq(results)

    # for key,value in current_dictionary.items():
    #     question_number = question_number+1
    #     print("{0}: {1}".format(question_number,key),end=" ")
    #     answer = str(input(" ? "))
    #     if(value[0].strip() == answer.strip()):
    #         value[1] = 1
    #         #print(key,value,"correct")
    #     # else:
    #        #print("false, the right answer:{0}".format(value[0].strip()))    
    # report_card_app(current_dictionary)



# push the result data to DB for analysis - ToDo
if __name__ == "__main__":
    # interactive_console_app()
    run_quiz_app(5)

