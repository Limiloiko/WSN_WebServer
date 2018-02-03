# -*- coding: utf-8 -*-
"""config.py

    Provide configuration to the APP from enviroment variables
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
     
     # Location of the database:
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir, 'app.db')
     # Disable the notifications from the application every time that
     # a change happens:
     SQLALCHEMY_TRACK_MODIFICATIONS = False