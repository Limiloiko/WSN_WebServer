# -*- coding: utf-8 -*-
"""
Description:
    Includes all the application inicializations. In python, wherer folder
    contains a __init__.py file, it is considered as a package, so ir can be 
    imported using de folder name (app in this case).


"""

# Standard libraries:
from flask import Flask                   # Global web server librarie
from flask_sqlalchemy import SQLAlchemy   # Dabatase classes and functions
from flask_migrate import Migrate         # Migration resources for the database
from flask_login import LoginManager      # Login manager

# App libraries
from config import Config                 # Configuratin variables

# Flask web server based
app = Flask(__name__)

# Imports and aplicates the configuration
app.config.from_object(Config)
# Loads the database
db = SQLAlchemy(app)   
# Creates the migration engine
migrate = Migrate(app, db)     
# Login manager 
login = LoginManager(app)
login.login_view = 'login'          # Used in tyhe HTML templates


# Define the actions in the web
import routes
# define the structre of the database
import models


