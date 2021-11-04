from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager
import os


db = SQLAlchemy()  # define a new database
DB_NAME = "database.db"  # give it a name, store this database in the website folder

UPLOAD_FOLDER = 'website/uploads/'  # needed for downloads section
FILE_EXT = ['.mp3', '.ogg', '.wav', '.zip', '.7z', '.jpeg', '.jpg', '.png',
                                       '.gif', '.ppt', '.py', '.cpp', '.mp4', '.mpeg', '.mpg', '.avi', '.docx', '.doc', '.pdf', '.rtf', '.txt']

if not os.path.exists(UPLOAD_FOLDER):  # create upload folder
    os.mkdir(UPLOAD_FOLDER)


def create_app():
    app = Flask(__name__)  # initiallizes flask
    # encrypts or secures cookies and session data realted to th site
    app.config['SECRET_KEY'] = '1997FordFocus'
    # means that our sql database is stored in DB_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # take database and tell it that its going to be used in this app
    db.init_app(app)
    # needed for downloads and uploads section

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16 #16MB max file size
    app.config['UPLOAD_EXTENSIONS'] = FILE_EXT

    
    # telling app where the routes are
    from .views import views
    from .auth import auth

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
