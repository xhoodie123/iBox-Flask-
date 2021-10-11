#login page

from flask import Blueprint

# defines blueprint of our app aka a bunch of ursl 

auth = Blueprint("auth", __name__) # defines blueprint

# defines our login page

@auth.route("/login")
def login():
	return "<p>Login</p>" # displays basic text on site with <p> tags </p> 
	
	
	
#defines user log out page
@auth.route("/logout")
def logout():
	return "<p>Logout</p>"
	
	
#defines user sign up page
@auth.route("/signup")
def sign_up():
	return "<P>Sign Up</P>"
	
	

