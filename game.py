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
from cass_db_talker import CassandraConnection, get_wordpairs_from_db

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

def report_card_app(current_dictionary):
    number_of_correct_answers = 0 
    print("\n>>>>>>>>Correct answers<<<<<<<<<<:")
    for key,value in current_dictionary.items():
        if value[1]==1:
            print(key," = ",value[0].strip(),"| 1")
            number_of_correct_answers+=1
        else:
            print(key," = ",value[0].strip(),"| 0")
    print("Result:{0}/{1}".format(number_of_correct_answers,len(current_dictionary)))
    
        

''' Needs improvement w.r.t report card'''
def run_quiz_app(num_of_questions = 10):

    runtime_wordlist = get_wordpairs_from_file()
    question_number = 0    
    current_dictionary={}
    answers = {}
    print("Enter the word which matches the following definition")

    for word in runtime_wordlist:
        question_number = question_number+1
        
        current_dictionary[word.german]=word.english
        print("{0}: {1}".format(question_number,word.german),end=" ")
        answer = str(input(" = "))
        # compare with nearest matches
        if(word.english.strip() == answer.strip()):
            answers[question_number]=1
        else:
            answers[question_number]=0
            print("the right answer:{0}".format(word.english))  
    report_card_app(current_dictionary)

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
    interactive_console_app()
    # run_quiz_app()

