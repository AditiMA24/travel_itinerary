from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
#from openai import openai
bootstrap = Bootstrap(app)

app.debug = True

from app import routes #, models

