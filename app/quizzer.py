'''
 #List of Tasks involved in the creating the "Thesaurus Quiz"
 1. interchange word and definition - to create entries for the thesaurus
 2. Read word-meaning from an input file & write them as meaning-word in output file
 3. Implement sessions & reading from config
 4. picking random n lines and storing them in a dictionary  
 5. Identify duplicates - keys or values in the input_thesauras
 6. Console app - takes user input and matches with key-value

'''

from itertools import islice
import subprocess
import random
import json

# interchange word and definition
'''
mystring = "blue - red"
word,meaning = mystring.split('-')
print(meaning,"-",word)
'''

#file reading writing  - pythonic way
'''
#Notes
with is the nice and efficient pythonic way to read large files. 
 1) file object is automatically closed after exiting from with execution block. 
 2) exception handling inside the with block. 
 3) memory for loop iterates through the f file object line by line. 
 internally it does buffered IO (to optimized on costly IO operations) and memory management.
'''
#with open("op.txt", 'a') as file_output:

'''
item = {
    "meaning":"word",
    "isCorrect":1,
    "frequency":0
}
current_question_list = []
question = {}

'''


def populate_runtime_list(ip,current_question_list):
    num_lines = line_counter(ip)
    #Alternatives : #num_lines = sum(1 for line in open('input_thesaurus.txt')), #num_lines =  len(open('input_thesaurus.txt').read().splitlines())
   
    ###################################
    
    question_count = 3 # read from config or user input to_do
    
    ###################################
    from_line_number = random.randint(1,num_lines-question_count+1)
    #print("num_lines:{0},question_count:{1},from_line_number:{2}".format(num_lines,question_count,from_line_number))
    with open(ip,"r") as thesaurus_file:
        head = list(islice(thesaurus_file, from_line_number, from_line_number+question_count))#start at a random line number & read N lines
        #head = [next(myfile) for x in xrange(N)]# reads first N lines
        for element in head:
            meaning,word = element.split(" - ")
            question = {} # current_list will be list of question
            question[meaning]=word.strip()
            question["isCorrect"]=1
           # question["frequency"]=1#ideally should be incremented
            current_question_list.append(question)

def line_counter(file):
    return int(subprocess.check_output('wc -l {}'.format(file), shell=True).split()[0])


def print_dictionary_2(current_dictionary):
    meaning_list = []
    word_keys = []#temp
    for meaning in current_dictionary.keys():
        meaning_list.append(meaning)
    for word in current_dictionary.values():
        #word_keys = [key, for key in word.keys()] #why not???
        #for key in word.keys():
        word_keys.append(word[0].strip())
    print(meaning_list)
    print(word_keys)


def print_dictionary(current_dictionary):
    #print key-values in the dictionary
    #meaning_list = [meaning, for meaning in current_dictionary.keys()] # try to use list comprehension
    meaning_list = []
    word_keys = []#temp
    for meaning in current_dictionary.keys():
        meaning_list.append(meaning)
    for word in current_dictionary.values():
        #word_keys = [key, for key in word.keys()] #why not???
        for key in word.keys():
            word_keys.append(key)
    print(meaning_list)
    print(word_keys)

    # for key,value in current_dictionary.items():
    #     print(key,"=>",value)
        # print(key,"=>",end="")
        # list_values = [key for key in current_dictionary.values()]      
        # print(list_values)      

'''
# Util function() to Read lines (with a delimiter) from an input file as keys - values 
    Write to the file_output after interchanging
    args - input_filename, delimiter, output_filename
'''
def interchange_key_value_in_file(ip,delimiter,op):
    with open(op, 'w') as file_output:
        with open(ip) as file_input:
            for line_read in file_input:
                word,meaning = line_read.split(delimiter) if delimiter in line_read else (line_read,"")
                #word,meaning = line_read.split(' - ') # 
                line_write = meaning.strip()+delimiter+word.strip()
                #file_output.write(line_write)
                # print(line_write,file=file_output)#to append a newline  
                print(line_write,file=file_output)#to append a newline  


def populate_runtime_dictionary(ip,current_dictionary,num_of_questions,begin_from_question="-1"):
    num_lines = line_counter(ip)
    #Alternatives : #num_lines = sum(1 for line in open('input_thesaurus.txt')), #num_lines =  len(open('input_thesaurus.txt').read().splitlines())
    
    ###################################
    
    # num_of_questions = 3 # read from config or user input to_do
    
    ###################################
    if(begin_from_question == "-1"):
        from_line_number = random.randint(1,num_lines-num_of_questions+1)
    else:
        from_line_number=int(begin_from_question)

    
    #print("num_lines:{0},num_of_questions:{1},from_line_number:{2}".format(num_lines,num_of_questions,from_line_number))
    with open(ip,"r") as thesaurus_file:
        head = list(islice(thesaurus_file, from_line_number, from_line_number+num_of_questions))#start at a random line number & read N lines
        #head = [next(myfile) for x in xrange(N)]# reads first N lines
        for item in head:
            meaning,word = item.split(" - ")
            #current_dictionary[meaning]={word:1}
            current_dictionary[meaning]=word


def populate_runtime_dictionary_2(ip,current_dictionary,num_of_questions):
    num_lines = line_counter(ip)
    #Alternatives : #num_lines = sum(1 for line in open('input_thesaurus.txt')), #num_lines =  len(open('input_thesaurus.txt').read().splitlines())
    
    ###################################
    
    #num_of_questions = 3 # read from config or user input to_do
    
    ###################################
    from_line_number = random.randint(1,num_lines-num_of_questions+1)
    #print("num_lines:{0},num_of_questions:{1},from_line_number:{2}".format(num_lines,num_of_questions,from_line_number))
    with open(ip,"r") as thesaurus_file:
        head = list(islice(thesaurus_file, from_line_number, from_line_number+num_of_questions))#start at a random line number & read N lines
        #head = [next(myfile) for x in xrange(N)]# reads first N lines
        for item in head:
            meaning,word = item.split(" - ")
            #current_dictionary[meaning]={word:1}
            current_dictionary[meaning]=[word,0]


#user interaction - console app
def interactive_console_app(num_of_questions,question_bank_file,begin_from_question="-1"):
    current_dictionary = {} #define a dictionary for the session
    #function calls()
    #interchange_key_value_in_file("ip.txt"," - ","input_thesaurus.txt")# should called only while populating db
    populate_runtime_dictionary(question_bank_file,current_dictionary,num_of_questions,begin_from_question)
    #print_dictionary(current_dictionary)
    question_number = 0
    answers = {}
    print("Enter the word which matches the following definition")
    for key,value in current_dictionary.items():
        question_number = question_number+1
        print("{0}: {1}".format(question_number,key),end=" ")
        answer = str(input(" = "))
        if(value.strip() == answer.strip()):
            #print(key,value,"correct")
            answers[question_number]=1
        else:
           answers[question_number]=0
           print("the right answer:{0}".format(value))    
    
    # for key,value in answers.items():
    #     print(key,"-",value,end=",")
        # correct_answers = [key, for key in answers.keys()])

def print_list(current_question_list):
    print(current_question_list)

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
    
        


def run_quiz_app(num_of_questions,question_bank_file="../data"):
    current_dictionary = {} #define a dictionary for the session
    #interchange_key_value_in_file("ip.txt"," - ","input_thesaurus.txt")# should called only while populating db
    populate_runtime_dictionary_2(question_bank_file,current_dictionary,num_of_questions)
    #print_dictionary_2(current_dictionary)
    question_number = 0
    print("Enter the word which matches the following definition")
    for key,value in current_dictionary.items():
        question_number = question_number+1
        print("{0}: {1}".format(question_number,key),end=" ")
        answer = str(input(" ? "))
        if(value[0].strip() == answer.strip()):
            value[1] = 1
            #print(key,value,"correct")
        # else:
           #print("false, the right answer:{0}".format(value[0].strip()))    
    report_card_app(current_dictionary)
        


def start_app_json():
    config_data = json.loads(open('config/defaults.json').read())
    print(config_data)
    num_of_questions = config_data["num_of_questions"]
    question_bank_file = config_data["question_bank_file"]
    quiz_type= config_data["quiz_type"]#"interactive(0) or test (1):
    is_sequential_practice = int(config_data["sequential_practice"])
    begin_from_question = config_data["begin_from_question"]
    # "sequential_practice":0, "begin_from_question" :20
    if(is_sequential_practice):
        interactive_console_app(num_of_questions,question_bank_file,begin_from_question)
    else:    
        if quiz_type:#1
            run_quiz_app(num_of_questions,question_bank_file)
        else:#0
            interactive_console_app(num_of_questions,question_bank_file)

start_app_json()

# current_question_list = []
##populate_runtime_dictionary("input_thesaurus.txt",current_dictionary)
#populate_runtime_list("input_thesaurus.txt",current_question_list)

# #print_dictionary(current_dictionary)
# #print_list(current_question_list)
# report_card_app(current_question_list)


#to try basic file dummy IO
'''
file_input = open("input.txt","r")
#print(file_input.readline())
line_read = file_input.readline()
word,meaning = line_read.split('-')
line_write = meaning.strip()+" - "+word.strip()+'\n'

file_output = open("output.txt","a")
file_output.write(line_write)
file_input.close()
file_output.close()
'''


