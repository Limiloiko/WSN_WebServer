# -*- coding: utf-8 -*-
"""
Description:
    Provide configuration to the APP from enviroment variables
"""

# Standard libraries
import os               # Operating Systems functions 


# Base directory to load the database
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    """Class with enviroment variables used in the application configuration.
    
    """
    
    # Used for security  
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'la-que-quieras'
     
    # Location of the database:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir, 'app.db')
     
    # Disable the notifications from the application every time that
    # a change happens:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     
    