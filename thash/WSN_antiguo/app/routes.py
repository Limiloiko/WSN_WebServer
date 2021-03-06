# -*- coding: utf-8 -*-
"""routes.py

"""
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import logout_user, login_required, current_user, login_user


@app.route('/index')
@app.route('/')
@login_required
def index():
    return render_template('index.html',
                           title='WSN Practical Work')
    
    
@app.route('/login', methods=['GET', 'POST']) # Only get by default
def login():
    
    # Allows weird situation when user clicks on Login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit(): # Returns false on GET
        user = User.query.filter_by(username=form.username.data).first() # Load the user from the database
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            
        return redirect(next_page)
    
    return render_template('login.html', 
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
