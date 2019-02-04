import codecs
from io import open # for handling german umlauts
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
	'''Collect data into fixed-length chunks or blocks'''
	# grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
	args = [iter(iterable)] * n
	return zip_longest(fillvalue=fillvalue, *args)





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

def line_counter(file):
    return int(subprocess.check_output('wc -l {}'.format(file), shell=True).split()[0])


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



def display_keyvalue_pairs(word_dictionary,delimiter=' - '):
    for k,v in word_dictionary.items():
        print(k+delimiter+v)


def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]

def containsAll(str, set):
    """Check whether 'str' contains ALL of the chars in 'set'"""
    return 0 not in [c in str for c in set]


def discard_lines_with_characters(file_in='./',file_out='./',characters=''):
	with open(file_in,'r',encoding='utf8') as f_in:
		with open(file_out,'a',encoding='utf8') as f_out:
			lines = [line.rstrip().lstrip() for line in f_in] # All lines including the blank ones
			lines = [line for line in lines if line] # Non-blank lines
			lines = [line for line in lines if not containsAny(line,characters)] # discard lines with specific chars
			# for x, y in grouper(lines, 2):
			# 	print (x, y)	
			for line1, line2 in zip(lines[::2],lines[1::2]):
				line = line1+":"+line2+'\n'
				f_out.write(line)

if __name__ == "__main__":
    pass