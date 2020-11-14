# WSN_WebServer

Wireless Sensor Networks example developed for Lab homework in 2017. Master on Industrial Electronics.

This script execute a web server to control a ZigBee node using a Telegesis module and a RaspBerry Pi model b.

## Requirements

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


## Getting started
It is recommended to execute and install all the required packages in a virtual enviroment, in order to keep the current versions safe:

    $ pip install virtualenv

Once you have installed the virtualenv library, create the project folder:

    $ cd path\to\project

Now, create the enviroment:

    $ virtualenv venv

To activate it, type (note the change in the promt):

    $ source venv\bin\activate
    $ venv\bin\activate  (Windows only)

Once inside the virtual enviroment, the required packages to install are included in the requirements.txt

    (venv) $ pip install -r requirements.txt

- flask
- flask-wtf
- flask-sqlalchemy
- flask-migrate
- flask-login
- pygal
- pySerial

To run the application, add the main script as flask enviroment variable:

    (venv) $ export FLASK_APP=main.py(use set instead of export on windows)

Initialize the application with:

    (venv) $ flask run

Now you only have to type http:s\\localhost:5000 on your web navigator.

## NOTES:

* Windows can give an error when the activate script is executed due to the ExecutionPolicy, to solve it, you should type with administrator privileges:

    $ Set-ExecutionPolicy AllSigned 

- For doing this demo, the tutorial followed was:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


## Authors
* **David Lima** - *davidlimaastor@gmail.com* - [Bitbucket](https://bitbucket.org/d_lima) - [GitHub](https://github.com/Limiloiko0) 

## License 

See LICENSE file.