from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

db = SQLAlchemy() #define a new database
DB_NAME = "database.db" #give it a name, store this database in the website folder

def create_app():
	app = Flask(__name__)	# initiallizes flask
	app.config['SECRET_KEY'] = '1997FordFocus' # encrypts or secures cookies and session data realted to th site
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # means that our sql database is stored in DB_NAME
	db.init_app(app) # take database and tell it that its going to be used in this app

	#telling app where the routes are
	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/') 

	from .models import User, Note #defines our classes
	
	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login' # take anon user here
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id)) # tell flask what user we are looking for

	return app 


def create_database(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
		print('Created Database!')