"""
Description:
    This module stores the tables of the database. These tare:
        * Temperatures, Humidities and Luminosities: Stores the measurements.
        * User: The information about the users registered in the web.
        

"""

# Standard libraries
# Password encryption
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

# App libraries:
from app import db
from app import login


class Temperatures(db.Model):
    """Basic table with the temperature data."""
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer, index=True)



class Humidities(db.Model):
    """Basic table with the humidity data."""
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer, index=True)



class Luminosities(db.Model):
    """Basic table with the Luminosity data."""
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer, index=True)



class User(UserMixin, db.Model):
    """Users table with users information. Notice that the password is saved 
    as a Password Hash for security reasons. This hash is generated with 
    the werkzeug.security functions.
    
    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    def __repr__(self):
        """Print function."""
        
        return '<User {}>'.format(self.username)
    
    
    def set_password(self, password):
        """Takes the password and generates the Hash to store in the row."""
        
        self.password_hash = generate_password_hash(password)
    
    
    def check_password(self, password):
        """Checks if the password and the hash stored are compatible."""
        
        return check_password_hash(self.password_hash, password)
    
    
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))