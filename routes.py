# -*- coding: utf-8 -*-
"""
Description:
    This module defines the routes and the code that needs to be executed with 
    the user interactions in the web pages. These html pages are generated 
    using tamplates, that are stored in the "app/templates" folder, and they 
    have a basic base.html design that are common in all the pages. 
    
        * index.html: First and main page.
        * login.html: Login page that includes the login form.
        * register.html: Register form.
        * subscribe.html: Subscrioption form
        
        

"""

# Standard libraries:
import flask                         # Web server library
from werkzeug.urls import url_parse
import pygal                         # Graphics for the index page
import aux_func                      # Auxiliary functions 


# App libraries
from app import app, db
# Web forms:
from app.forms import LoginForm, RegistrationForm, SubscriptionForm
# Database tables
from app.models import User, Temperatures, Humidities, Luminosities
# Login resources
from flask_login import logout_user, login_required, current_user, login_user


# Home page, first page when you access
@app.route('/index')
@app.route('/')
@login_required     # To see this page, you have to be logged
def index():
    """Creates the graphics with the last five data stored in the database 
    for each variable measured.
    
    """
    
    # Create the graphs from pygal library:
    graph_t = pygal.StackedLine(fill=True)
    graph_l = pygal.StackedLine(fill=True)
    graph_h = pygal.StackedLine(fill=True)
    
    # Titles:
    graph_t.title = 'Temperature values'
    graph_l.title = 'Luminosity values'
    graph_h.title = 'Humidity values'
    
    # Labels for the X labels:
    graph_t.x_labels = ['1','2','3','4','5']
    graph_l.x_labels = ['1','2','3','4','5']
    graph_h.x_labels = ['1','2','3','4','5']
    
    # Gets the information from the Database
    data_temp_base = Temperatures.query.all()
    data_lum_base = Luminosities.query.all()
    data_hum_base = Humidities.query.all()
    
    data_temp = []
    data_lum = []
    data_hum = []
    
    for d1 in data_temp_base:
        data_temp.append(d1.data)
    
    for d2 in data_lum_base:
        data_lum.append(d2.data)
    
    for d3 in data_hum_base:
        data_hum.append(d3.data)
    
    
    graph_t.add('Temp',  data_temp[-5:])
    graph_l.add('Lum',  data_lum[-5:])
    graph_h.add('Hum',  data_hum[-5:])
    
    graph_data_t = graph_t.render_data_uri()
    graph_data_l = graph_l.render_data_uri()
    graph_data_h = graph_h.render_data_uri()
    
    return flask.render_template('index.html',
                           graph_data_t = graph_data_t,
                           graph_data_l = graph_data_l,
                           graph_data_h = graph_data_h,
                           title='WSN Practical Work')
    
    

# Login page    
@app.route('/login', methods=['GET', 'POST']) # Only get by default
def login():
    """Loads and renders the template for the login form. It defines the code 
    for both methods GET and POST.
    
    """
    
    # Allows weird situation when user clicks on Login
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    
    # Loads the login form
    form = LoginForm()
    if form.validate_on_submit(): # Returns true on POST method
        # Load the user from the database
        user = User.query.filter_by(username=form.username.data).first() 
        
        # Checks the password, if failed, reset page with error message
        if user is None or not user.check_password(form.password.data):
            flask.flash('Invalid username or password')
            return flask.redirect(flask.url_for('login'))
        
        # Redirect if you get this page trying to go another page
        login_user(user, remember=form.remember_me.data)
        next_page = flask.request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('index')
            
        return flask.redirect(next_page)
    
    return flask.render_template('login.html', 
                           title='Sign In',
                           form=form,
                           current_user=current_user)



# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Loads and renders the template for the register form. It defines the
    code for both methods GET and POST.
    
    """    
    
    # If the user is currently loaded, goes to the index page
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    
    # Loads the registration form
    form = RegistrationForm()
    if form.validate_on_submit(): # Returns true on POST method
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flask.flash('Congratulations, you are now a registered user!')
        return flask.redirect(flask.url_for('login'))
    
    return flask.render_template('register.html', title='Register', form=form,
                           current_user=current_user)



# Subscribe page 
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe_service():
    """Loads and renders the template for the subscribe form. It defines the 
    code for both methods GET and POST.
    
    """
    
    # If the user is not currently loaded, goes to the login page
    if not current_user.is_authenticated:
        return flask.redirect(flask.url_for('login'))

    # Loads the subscription form
    form = SubscriptionForm()
    if form.validate_on_submit(): # Returns true on the POST method
        
        # Take data
        hum = form.humidity.data
        temp = form.temperature.data
        lum = form.luminosity.data
        MAC = form.MAC.data
        print '   MAC: %s\r'%MAC    # To check the MAC easier
        
        # Sends unicast messages if required
        # Variable followed by the time
        if lum is not None:
            string = "AT+UCAST:%s,L%s\r"%(MAC,lum)
            aux_func.write_to_telegesis(string.encode())
            print "Luminosidad cada: %s segundos"%lum
        
        if hum is not None:
            string = "AT+UCAST:%s,H%s\r"%(MAC,hum)
            aux_func.write_to_telegesis(string.encode())
            print "Humedad cada: %s segundos"%hum
        
        if temp is not None:
            string = "AT+UCAST:%s,T%s\r"%(MAC,temp)
            aux_func.write_to_telegesis(string.encode())
            print "Temperatura cada: %s segundos"%temp
        
        
        # Message showed when the page is reloaded
        flask.flash('Subscription succesfully changed!')
        return flask.redirect(flask.url_for('index'))
    
    return flask.render_template('subscribe.html', 
                                 title='Subscription Service', 
                                 form=form,
                                 current_user=current_user)



@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('index'))
