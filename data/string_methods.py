1# https://www.datacamp.com/community/tutorials/python-string-tutorial

single_quote = 'Single quote allow you to embed "double" quotes in your string.'
double_quote = "Double quote allow you to embed 'single' quotes in your string."
triple_quote = """Triple quotes allows to embed "double quotes" as well as 'single quotes' in your string. 
And can also span across multiple lines."""



if __name__ == "__main__":
    print(single_quote)
    print(double_quote)
    print(triple_quote)
    # triple_quote[35] = "'" # Strings are immuatablel; TypeError: 'str' object does not support item assignment
    print(len(triple_quote))

    # Since strings are a sequence of characters, you can access it through slicing and indexing just like you would with Python lists or tuples
    snack = "Chocolate cookie!"
    print(snack[3])
    print(snack[-1])
    # To extract a substring - use range slicing : [Start index (included): Stop index (excluded)]
    print(snack[10:len(snack)])
    print(snack[10:-1])
    print(snack[:])

    # String slicing can also accept a third parameter, the stride, which refers to how many characters you want to move forward after the first character is retrieved from the string.
    # The value of stride is set to 1 by default.
    number_string = "1020304050"
    print(number_string[0:-1:2]) # 12345
    print(number_string[1:8:3]) # 030

    # The value of -1 for the stride allows you to start from the end character and then move one character at a time.
    print(number_string[::-1]) # 0504030201
    print(number_string[::-2]) # 00000


    # Common String Operations

    string1 = 'cream'
    string2 = 'biscuit'
    cost = 14
    snack = string1 + " " + string2
    print(snack)
    # print(snack+" "+cost) #TypeError: can only concatenate str (not "int") to str
    print("The cost of snack is: "+str(cost))

    # To repeat a string, use the * operation.
    single_word = 'hip '
    line1 = single_word * 2 + 'hurray! '
    print(line1 * 3) # hip hip hurray! hip hip hurray! hip hip hurray!

    # You can also check for membership property in a string using in and not in:
    sub_string1 = 'ice'
    sub_string2 = 'glue'
    string1 = 'ice cream'
    if sub_string1 in string1:
        print("There is " + sub_string1 + " in " + string1)
    if sub_string2 not in string1:
        print("Phew! No " + sub_string2 + " in " + string1)


    # Built-in methods
    print(str.capitalize('cookie')) # returns a copy of the string with its first character capitalized.

    print(snack.islower()) # returns true if all characters in the string are lowercase, false otherwise.


    str1 = 'I got you a cookie, do you like cookies?'
    str2 = 'cook'    
    print(str1.find(str2)) # returns the lowest index in the string where the substring is found.Returns -1 if the substring is not found.
    print(str1.find(str2,20,-1))  #You can also specify the start and end index within the string where you want the substring to be searched for. 

    print(str1.count(str2)) # counts how many times a substring occurs in the string. You can also specify the start and the stop index for the string.

    str_tab = '\t'
    str_nextline = '''\n'''

    print(str_tab.isspace()) # returns True if there are only whitespace characters in the string, false otherwise. Whitespace characters are the characters such as space, tab, next line, etc.
    print(str_nextline.isspace())

    str1 = "       I can't hear you. Are you alright?       "
    str2 = "       Yes, all is good.        "
    str3 = str1.lstrip().rstrip() + str2.lstrip().rstrip() # removes all leading/trailing whitespace in string
    print(str3)


    number_string = "1020304050"
    print(number_string.isdigit()) # returns True if string contains only digits and False otherwise.


    string1 = 'hip hip hurray! hip hip hurray! hip hip hurray!'
    string2 = string1.replace('hip', 'Hip') 
    # replaces all occurrences of the substring in string with new. You can also define a third argument max, which replaces at most max occurrences of substring.
    # Remember it's not an inplace replacement, which means the immutable property still holds and a new string is actually formed.
    print(string1)
    print(string2)

    dessert = 'Cake, Cookie, Icecream'
    list_dessert = dessert.split(',') # splits the string according to the delimiter (space if not provided) and returns a list of substrings.
    print(list_dessert)

