from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
import os

####################################################################################
# THIS IS FOR THE ENGINEERS ONLY, DO NOT UNCOMMENT OTHER TEAM OR APP WILL NOT WORK #
#####################################################################################
# if your using ubuntu you wont need to install 
#import smptlib
#import email.utils

# you will need to pip install flask-user
#from flask_user import Usermanager
# you will need to pip install flask-mail
#from flask_mail import Mail
#you will need to pip install flask-migrate
#from flask_migrate import Migrate

#app = Flask(__name__)

db = SQLAlchemy()  # define a new database
DB_NAME = "database.db"  # give it a name, store this database in the website folder

#mail = Mail(app)
UPLOAD_FOLDER = 'website/uploads/'  # needed for downloads section
FILE_EXT = ['.mp3', '.ogg', '.wav', '.zip', '.7z', '.jpeg', '.jpg', '.png',
                                       '.gif', '.ppt', '.py', '.cpp', '.mp4', '.mpeg', '.mpg', '.avi', '.docx', '.doc', '.pdf', '.rtf', '.txt']

#migrate=Migrate()
#mail-Mail(app)




if not os.path.exists(UPLOAD_FOLDER):  # create upload folder
    os.mkdir(UPLOAD_FOLDER)

#@app.before_first_request
#def create_tables():
    #db.create_all()
  
def create_app():
    app = Flask(__name__)  # initiallizes flask
    # encrypts or secures cookies and session data realted to th site
    app.config['SECRET_KEY'] = '1997FordFocus'
    # means that our sql database is stored in DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # take database and tell it that its going to be used in this app
    db.init_app(app)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16 #16MB max file size
    app.config['UPLOAD_EXTENSIONS'] = FILE_EXT

####################################################################################
# THIS IS FOR THE ENGINEERS ONLY, DO NOT UNCOMMENT OTHER TEAM OR APP WILL NOT WORK #
#####################################################################################
    # app configurations for email authentication 
      #flask-User app settings
   # app.config['USER_APP_NAME']="Ibox"
    #app.config['USER_ENABLE_EMAIL'] = True
    #app.config['USER_ENABLE_CONFRIM_EMAIL']=True
    #app.config['USER_ENABLE_CHANGE_PASSWORD']= True
    #app.config['USER_ENEABLE_CHANGE_USERNAME']= False
    #app.config['USER_ENABLE_CONFIRM_EMAIL']= True   
    #app.config['USER_ENABLE_FORGOT_PASSWORD']=  True  
    #app.config['USER_ENABLE_USERNAME'] = False
        
    
    #app.config['USERNAME_SMPT']="AKIARKAILXQ7F377STLL" # smtp username
    #app.config['PASSWORD_SMPT']="BGcK3WhRPNi+JEbEa2rMuyj/AbbUikPbfzYh+XNkvf9t" # smtp password
    #app.config['CONFIGURATION_SET']="ConfigSet"
    #app.config['HOST']="email-smpt-.us-west-1.amazonaws.com"
    #app.config['PORT']=587
    
    #app.config['USER_EMAIL_SENDER_NAME'] = "Ibox"    
    #app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@gmail.com"
    #app.config['USER_ENABLE_REGISTER']= True
    #app.config['USER_REQUIRE_RETYPE_PASSWORD']= True   

    #app.config['USER_AFTER_LOGIN_ENDPOINT']= "views.profile"
    #app.config['USER_AFTER_LOGOUT_ENDPOINT']= "views.logout"
    #app.config['USER_ENABLE_AUTH0'] = False       
    #app.config['USER_INTIVE_USER_URL'] = "/user/invite"
    
    
    
    
    # telling app where the routes are
    from .views import views
    from .auth import auth
    
    #setting up flask-user
    #user_manager=UserManager(app,db,User)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Group  # defines our classes

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # take anon user here
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # tell flask what user we are looking for
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
