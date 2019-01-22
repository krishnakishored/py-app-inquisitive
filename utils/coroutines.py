'''
# ToDo:
http://www.dabeaz.com/coroutines/Coroutines.pdf
'''

def countdown(n):
    print ("Counting down from {0}".format(n))
    while n > 0:
        yield n
        n -=  1

if __name__=="__main__":
    x = countdown(4)
    print(x)
    for i in range(3):
        x.__next__()
    # x.__next__()
    # x.__next__()