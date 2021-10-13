from flask import Flask

def create_app():
	app = Flask(__name__)	# initiallizes flask
	app.config["SECRET_KEY"] = "rsjresgsjfrr!!213!!" # encrypts or secures cookies and session data realted to th site
	
	#telling app where the routes are
	
	from .views import views
	from .auth import auth
	
	app.register_blueprint(views, urL_prefix = "/")
	app.register_blueprint(auth, urL_prefix = "/")
	
	return app 
