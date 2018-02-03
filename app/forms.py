# -*- coding: utf-8 -*-
"""
Description:
    Defines the forms used to get data from the user in POST requests in the 
    web browser. The forms here are:
        * Subscription
        * Login
        * Registration
    
    
NOTES:
    * You will have to change the data in the MAC select field with the slave 
    MAC you are using.
    
    
"""

# Standard libraries
from flask_wtf import FlaskForm 
# Basic fields used in the forms
from wtforms import StringField, SelectField, IntegerField
from wtforms import PasswordField, BooleanField, SubmitField
# Methods to validate the information
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

# App libraries
from app.models import User



class SubscriptionForm(FlaskForm):
    """Form used in the Subscription page. Needs the time in seconds desired 
    for gatering the data. It has:
        * 3 integer fields for the time 
        * select field to choose the slave MAC
        * The submit button to make the POST
    
    """
    
    humidity = IntegerField('Humidity')
    temperature = IntegerField('Temperature')
    luminosity = IntegerField('Luminosity')
    MAC = SelectField('Slave MAC Address',
                      choices=[("000D6F00003DEF30","MAC 1"),   # CHANGE 
                               ("123456789ABCDEF5","MAC 2")])  # CHANGE

    submit = SubmitField('Subscribe')
    


class LoginForm(FlaskForm):
    """Form used to Login page. Needs the username and password data.It has:
        * String field to user name
        * Password field, hide the content 
        * Boolean field to remember the inputs
        * Submit to make the POST

    """    
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    """Form used in the registration page. It gets the data related with the 
    username, email and password. Also checks if the username or the email
    is already registred in the database. It has:
        * Two string fields for username and email data.
        * Two password fields for the password.
        * Submit field to make the POST.


    Functions:
        validate_username:  Checks if the username already exists.
        validate_email:     Checks if the email areadt exists.
        
    NOTE:
        All the class methods that begins with "validate_" will be executed on 
        the submit event.
        
    """
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')
    
    
    def validate_username(self, username):
        """Checks if the username already exists in the database. It shows an 
        error message if true using a ValidationError that will be treated by
        the FlaskForm class.
        
        Args:
            username (str): Username that will be checked
        
        """
        
        # Gets the entries on the database with the username 
        user = User.query.filter_by(username=username.data).first()
        # If not none, already exists 
        if user is not None:
            raise ValidationError('Please use a different name')
        
        
    def validate_email(self, email):
        """Checks if the email already exists in the database. Same codigication 
        as in the case of the username.
        
        Args:
            email (str): Email that will be checked
        
        """
        
        # Gets the entries on the database with the same email
        user = User.query.filter_by(email=email.data).first()
        # If not none, areaday exists
        if user is not None:
            raise ValidationError('Email address already registred')