'''
% Formatting
The modulo % is a built-in operation in Python.It is known as the interpolation operator. 
You will need to provide % followed by the datatype that needs to be formatted or converted. 
The % operation then substitutes the '%datatype' phrase with zero or more elements of the specified data type:
'''

'''
The formatter class is one of the built-in string class. 
It provides the ability to do complex variable substitutions and value formatting using the format() method. 
It allows you to create and customize your own string formatting behaviors by rewriting the public methods it contains: format(), vformat(). 
It has some methods that are intended to be replaced by subclasses: parse(), get_field(), get_value(), check_unused_args(), format_field() and convert_field(). 
'''


'''
Template Strings
Templates have some methods defined within: substitute() and safe_substitute().
Notice the $$ in the above example? This is because with template $$ is an escape character which is replaced with a single $. 
Another rule for template is how you define the identifier within your template, there is the usual syntax: $identifier, but you also have ${identifier}.
'''


'''
Formatted String Literal (f-string)
A formatted string literal or f-string is a string literal that is prefixed with 'f' or 'F'. 
You can define identifiers to be used in your string within curly braces { }.

f-strings are also faster compared to the other three methods you have seen earlier.

'''

if __name__ == "__main__":
    print("I bought %d Euro worth of %s!" %(200, 'cookies'))

    print("I bought {0} Euro worth of {1}!".format(200,'cookies')) #Accessing values by position
    print("I bought {total} Euro worth of {item}!".format(total = 200, item = 'cookies')) #Accessing values by name
    print('{:#<10}'.format('Cake'))  #Left aligment for word 'Cake' according to right alignment, gaps filled with '#'
    print('{:#^10}'.format('Cake')) #Centre aligment for word 'Cake' according to right alignment, gaps filled with '#'
    print('{:#>10}'.format('Cake')) #Right aligment for word 'Cake' according to right alignment, gaps filled with '#'

    for num in range(1,10):
        print('{0:{width}}'.format(num, width=3), end=' ')


    from string import Template #First you will need to import 'Tempalte' class

    money = dict(who = 'You', to_whom = 'baker')
    print(Template('$who owe the $to_whom a total of $$100').substitute(money))

    fact = Template('$alter_ego is weak but wait till he transforms to $superhero!')
    fact_str = fact.substitute(alter_ego='Bruce Banner', superhero='Hulk')
    print(fact_str)
    hero = dict(alter_ego='Peter Parker',superhero='Spiderman')
    
    fact_str = fact.safe_substitute(hero) # The safe_substitute() is one of the advantage of using template.
    
    print(fact_str)
    alter_ego = 'Peter Parker' 
    superhero = 'spiderman'

    print( f'{alter_ego} is weak but wait till he transforms to {superhero}!')
    print(f'{alter_ego} is weak but wait till he transforms to {superhero.capitalize()}!')

