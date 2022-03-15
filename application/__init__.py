from flask import Flask
import sqlalchemy
# from config import Config
import os
from flask_sqlalchemy import SQLAlchemy
# from flask_restplus import Api

# api = Api()


# from flask_mongoengine import MongoEngine

app = Flask(__name__)
# api.init_app(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'university.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or b'\x9f\x94\xb39\x84\x03B\x02h\xdb\x82c:,\xe9\xc8'

db = SQLAlchemy(app)

# db = MongoEngine()
# db.init_app(app)

from application import routes