# -*- coding: utf-8 -*-
"""__init__.py
    WSN Practical Work web server

"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)           # Represents the Database
migrate = Migrate(app, db)     # Migration engine

login = LoginManager(app)
login.login_view = 'login'


#from app import routes
import routes
import models
#from app import models
# routes: Define the actions in the web
# models: define the structre of the database

