import json


'''

ToDo

1. To create a method which takes 
    - a list of keys, 
    - reads through a file - delimitter separated, multi-line,
    - return a json file - a list of json objects or an object of json objects

# https://linuxconfig.org/how-to-parse-data-from-json-into-python

https://docs.python.org/3/library/json.html


'''



'''
# Util function to Read lines (with a delimiter) from an input file as keys - values 
    Write to the file_output after interchanging
    args - input_filename, delimiter, output_filename


    http://gowrishankarnath.com/read-write-json-python/

'''

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'a') as fp:
        json.dump(data+',', fp)


def create_json_from_textfile(ip,delimiter):
    data = {}
    word_list = []
    # with open(op, 'w') as file_output:
    with open(ip) as file_input:
        for line_read in file_input:
            german_word,english_word = line_read.split(":") if delimiter in line_read else (line_read,"")
            data["german"] = german_word
            data["english"] = english_word
            # word_list.insert(0,data) #You need to append a copy, otherwise you are just adding references to the same dictionary over and over again:
            word_list.append(data.copy())

    return json.dumps(word_list,ensure_ascii=False)

    # with open('g_e_2.json','a') as f:
        # ','.join(word_list)
        # json.dump(','.join(word_list),f)
    
    
          


if __name__=="__main__":
    wordlist = create_json_from_textfile("./data/input/german_english.txt",":")
    with open("./data/input/ger_eng.json",'a') as fp:
        json.dump(wordlist,fp)