'''
1. Read from config
2. Prepare the runtime settings

'''

# from app import quizzer



#user interaction - console app
# def evaluate(num_of_questions,question_bank_file,begin_from_question="-1"):
def evaluate(current_dictionary,):
    current_dictionary = {} #define a dictionary for the session
    # #function calls()
    #interchange_key_value_in_file("ip.txt"," - ","input_thesaurus.txt")# should called only while populating db
    # populate_runtime_dictionary(question_bank_file,current_dictionary,num_of_questions,begin_from_question)


    # After Populate the runtime question_bank
    current_dictionary = {
        "abstammen von": "descend from",
        "abstauben": "dust",
        "abstimmen": "vote"
    }

    #print_dictionary(current_dictionary)
    question_number = 0
    answers = {}
    print("Enter the word which matches the following definition")
    for key,value in current_dictionary.items():
        question_number = question_number+1
        # print("{0}: {1}".format(question_number,key),end=" ")
        answer = str(input(" = "))
        if(value.strip() == answer.strip()):
            #print(key,value,"correct")
            answers[question_number]=1
        else:
           answers[question_number]=0
           print("the right answer - {0}".format(value))   


if __name__=="__main__":
   pass
    # quizzer.start_app_json()
    # evaluate(5,)
  