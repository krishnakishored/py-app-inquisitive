from flask import Flask
from config import Config


app = Flask(__name__) # the app here is wortspiel
app.config.from_object(Config) # separation of concerns

from app import routes

# print(__name__) # o/p: __main__