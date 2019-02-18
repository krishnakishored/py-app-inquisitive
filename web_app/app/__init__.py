from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__) # the app here is wortspiel
app.config.from_object(Config) # separation of concerns
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import routes,models

# print(__name__) # o/p: __main__