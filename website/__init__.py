from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_socketio import SocketIO
import socketio
from werkzeug.routing import BaseConverter
import os
from os import path

socketio = SocketIO()
db = SQLAlchemy()  # define a new database
DB_NAME = "database.db"  # give it a name, store this database in the website folder
UPLOAD_FOLDER = 'website/uploads/'  # needed for downloads section
FILE_EXT = ['.mp3', '.ogg', '.wav', '.zip', '.7z', '.jpeg', '.jpg', '.png',
            '.gif', '.ppt', '.py', '.cpp', '.mp4', '.mpeg', '.mpg', '.avi', '.docx', '.doc', '.pdf', '.rtf', '.txt', '.odt']

if not os.path.exists(UPLOAD_FOLDER):  # create upload folder
    os.mkdir(UPLOAD_FOLDER)


def create_application():
    application = Flask(__name__)  # initiallizes flask
    # encrypts or secures cookies and session data realted to th site
    application.config['SECRET_KEY'] = '1997FordFocus'
    # means that our sql database is stored in DB_NAME
    application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # take database and tell it that its going to be used in this app
    db.init_app(application)
    socketio.init_app(application)

    application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    application.config['MAX_CONTENT_LENGTH'] = 1024 * \
        1024 * 32  # 32MB max file size
    application.config['UPLOAD_EXTENSIONS'] = FILE_EXT

    # telling app where the routes are
    from .views import views
    from .auth import auth

    application.register_blueprint(views, url_prefix='/')
    application.register_blueprint(auth, url_prefix='/')

    from .models import User  # defines our classes

    create_database(application)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # take anon user here
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(id):
        # tell flask what user we are looking for
        print("USER ID:")
        print(id)
        return User.query.get(int(id))

    return application


def create_database(application):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=application)
        print('Created Database!')
