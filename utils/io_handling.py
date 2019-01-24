import codecs
from io import open # for handling german umlauts

def build_word_dict_from_file(filename='./',delimiter=':',word_dictionary={}):
    # word_dictionary={}
    # todo : exception handling
    with open(filename,'r',encoding='utf8') as f_in:
        lines = [line.rstrip().lstrip() for line in f_in] # All lines including the blank ones
        lines = [line for line in lines if line] # Non-blank lines
        for line in lines:
            key_word = line[:line.find(delimiter)]
            value_word = line[line.find(delimiter)+1:len(line)]
            word_dictionary[key_word.rstrip()] = value_word.lstrip()
    return word_dictionary


# def swap_words_on_delimiter(file_in='./',delimiter=':',file_out='./'):
#     '''
#     1. swaps words on delimiter -  "post:man" becomes "man:post"
#     2. write to a new output file
#     '''    
#     with open(file_in,'r',encoding='utf8') as f_in:
# 		with open(file_out,'a',encoding='utf8') as f_out:
# 			lines = [line.rstrip().lstrip() for line in f_in] # All lines including the blank ones
# 			lines = [line for line in lines if line] # Non-blank lines
# 			for line in lines:
# 				key_word = line[:line.find(delimiter)]
# 				value_word = line[line.find(delimiter)+1:len(line)]
# 				new_word = value_word+delimiter+key_word+'\n'
# 				word_trimmer(new_word)
# 				f_out.write(new_word)

def swap_words_on_delimiter(file_in='./',delimiter=':',file_out='./'):
	with open(file_in,'r',encoding='utf8') as f_in:
		with open(file_out,'a',encoding='utf8') as f_out:
			lines = [line.rstrip().lstrip() for line in f_in] # All lines including the blank ones
			lines = [line for line in lines if line] # Non-blank lines
			for line in lines:
				
				key_word=line[:line.find(delimiter)]
				value_word = line[line.find(delimiter)+1:len(line)]
				new_word = value_word+delimiter+key_word+'\n'
				# print(new_word)
				new_word = word_trimmer(new_word)
				# print(new_word)
				f_out.write(new_word)
				# key_word = line[:line.find(delimiter)]
				# value_word = line[line.find(delimiter)+1:len(line)]
				# new_word = value_word+delimiter+key_word+'\n'
				# word_trimmer(new_word)
				# f_out.write(new_word)


def word_trimmer(word="",delimiter1="~",delimiter2=":"):
	'''
    remove the word between the delimiter1 & delimiter2
	leaves the delimiter2 but removes the delimiter1 (for this specific use-case)
    '''
	w1 = word[:word.find(delimiter1)]
	# w2 = word[word.find(delimiter1):word.find(delimiter2)]
	word= w1+ word[word.find(':'):]
	# print(word)
	return word



def display_keyvalue_pairs(word_dictionary,delimiter=' - '):
    for k,v in word_dictionary.items():
        print(k+delimiter+v)

if __name__ == "__main__":
    pass