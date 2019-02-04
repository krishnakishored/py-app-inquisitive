import json
from difflib import get_close_matches

# data = json.load(open("data/data.json"))
data = json.load(open('data/german_english.json'))

def translate(w):
    w = w.lower()
    if(w in data): #if(w in data.keys()):
        return data[w]
    elif(w.upper() in data):
        return data[w.upper()]    
    elif w.title() in data:
        return data[w.title()]
    elif len(get_close_matches(w,data.keys())) > 0:
        close_match = get_close_matches(w,data.keys())[0]
        yn =  input("Did you mean {0} instead? Enter Y if yes, N if no: ".format(close_match))
        if yn.lower() == "y":
            return data[close_match]
        elif yn.lower() == "n":
            return "Word not found"     
        else:
            return "we didn't understand your query"    
        
    else:
        return "Word not found"

word = input("Enter a word: ")

output = translate(word)
#Handle when the ouput is list or string

if type(output) == list:
    for item in output:
        print(item)
else:
    print(output)


