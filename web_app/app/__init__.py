from flask import Flask

app = Flask(__name__) # the app here is wortspiel

from app import routes

# print(__name__) # o/p: __main__