# -*- coding: utf-8 -*-
"""

Description:
    This script execute a web server to control a ZigBee node using a Telegesis 
    module and a RaspBerry Pi model b. 

Requirements:
    - Python 2.7.13
    
    Libraries:
    - flask 0.12.2              (Global library)
    - flask_sqlalchemy 2.3.2    (Forms templates)
    - flask_wtf 0.14.2          (Database)
    - flask_migrate             (Database migration tools)
    - flask_login 0.4.1         (Login resources)
    - pygal 2.4.0               (Graph functions)
    - pySerial 3.4              (USB USART functions)


Example:
    It is recommended to execute and install all the required packages in a 
    virtual enviroment, in order to keep the current versions safe:
    
        $ pip install virtualenv     (install)
        
        
    Once you have installed the virtualenv library, create the project folder:
        
        $ cd path\to\project        
        
        
    Now, create the enviroment:
        
        $ virtualenv venv            (venv is the name of the enviroment)
        
        
    To activate it, type (note the change in the promt):
        
        $ source venv\bin\activate   
        $ venv\bin\activate  (Windows only)


    Once inside the virtual enviroment, the required packages to install are:
    
        (venv) $ pip install <package-name>
        
    * flask             
    * flask-wtf         
    * flask-sqlalchemy  
    * flask-migrate     
    * flask-login       
    * pygal             
    * pySerial
    
    
    To run the application, add the main script as flask enviroment variable:
    
        (venv) $ export FLASK_APP=main.py(use set instead of export on windows)
        
        
    Initialize the application with:
        
        (venv) $ flask run

    
    Now you only have to type http:s\\localhost:5000 on your web navigator.



    NOTES:
        * Windows could give an error when the activate script is executed due
        to the ExecutionPolicy, to solve it, you should type with administrator
        privileges:
            
            $ Set-ExecutionPolicy AllSigned 


        * For doing this demo, the tutorial followed was:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


"""


__author__ = 'David Lima (limiloiko@gmail.com)'
__version__ = '1.0'
__all__ = []


from app import app, db
from app.models import User 


@app.shell_context_processor
def make_shell_context():
    """Creates a shell context that adds the database instance and models to 
    the shell session. The app.shell_context_processor decorator registers 
    the function as a shell context function. When the flask shell command 
    runs, it will invoke this function and register the items returned by 
    it in the shell session.
        
    """
    
    return {'db':db, 'User': User}


# Init:
print "Initializing configuration...\r"

import aux_func  # Auxiliary functions 


