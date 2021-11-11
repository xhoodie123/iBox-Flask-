# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import smtplib
import email.utils
from flask_login import LoginManager, login_manager
from flask_user import UserManager
from flask_mail import Mail

from werkzeug.routing import BaseConverter
import os
from flask_migrate import Migrate

_basedir_ = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)  # initiallizes flask
   # app.config.from_object('config')

db = SQLAlchemy(app)  # define a new database
DB_NAME = "database.db"  # give it a name, store this database in the website folder
migrate = Migrate()
mail = Mail(app)

FILE_EXT = ['.mp3', '.ogg', '.wav', '.zip', '.7z', '.jpeg', '.jpg', '.png', '.gif', '.ppt', '.py','.cpp', '.mp4', '.mpeg', '.mpg', '.avi', '.docx', '.doc', '.pdf', '.rtf', '.txt']

@app.before_first_request
def create_tables():
	db.create_all()




UPLOAD_FOLDER = 'website/uploads/'  # needed for downloads section

if not os.path.exists(UPLOAD_FOLDER):  # create upload folder
    os.mkdir(UPLOAD_FOLDER)

def create_app():

   
    # encrypts or secures cookies and session data realted to th site
    app.config['SECRET_KEY'] = 'Rsjr4vr!!'
    # means that our sql database is stored in DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['CSRF_ENABLED']= True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Avoids a SQLAlchemy Warning
    #flask-User app settings
    app.config['USER_APP_NAME']="Ibox"
    app.config['USER_ENABLE_EMAIL'] = True
    app.config['USER_ENABLE_CONFRIM_EMAIL']=True
    app.config['USER_ENABLE_CHANGE_PASSWORD']= True
    app.config['USER_ENEABLE_CHANGE_USERNAME']= False
    app.config['USER_ENABLE_CONFIRM_EMAIL']= True   
    app.config['USER_ENABLE_FORGOT_PASSWORD']=  True  
    app.config['USER_ENABLE_USERNAME'] = False
        
    
    app.config['USERNAME_SMPT']="AKIARKAILXQ7F377STLL" # smtp username
    app.config['PASSWORD_SMPT']="BGcK3WhRPNi+JEbEa2rMuyj/AbbUikPbfzYh+XNkvf9t" # smtp password
    app.config['CONFIGURATION_SET']="ConfigSet"
    app.config['HOST']="email-smpt-.us-west-1.amazonaws.com"
    app.config['PORT']=587
    
    app.config['USER_EMAIL_SENDER_NAME'] = "Ibox"    
    app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@gmail.com"
    app.config['USER_ENABLE_REGISTER']= True
    app.config['USER_REQUIRE_RETYPE_PASSWORD']= True   

    app.config['USER_AFTER_LOGIN_ENDPOINT']= "views.profile"
    app.config['USER_AFTER_LOGOUT_ENDPOINT']= "views.logout"
    app.config['USER_ENABLE_AUTH0'] = False       
    app.config['USER_INTIVE_USER_URL'] = "/user/invite"
    
    
    app.config['MAX_CONTENT_LENGTH']= 1024*1024*16 #16mb max file size
    app.config['UPLOAD_EXTENTIONS']= FILE_EXT
   
    from .models import User
    
    
    # seting up flask-user	
    user_manager = UserManager(app, db, User)       
        
    # take database and tell it that its going to be used in this app
    db.init_app(app)
    migrate.init_app(app,db)
    
    # needed for downloads and uploads section

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # telling app where the routes are
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User # defines our classes


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # take anon user here
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        # tell flask what user we are looking for
        return User.query.get(int(id))
    


    

    return app

