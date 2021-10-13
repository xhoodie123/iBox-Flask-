

from flask import Blueprint, render_template

# defines blueprint of our app aka a bunch of ursl 

auth = Blueprint("auth", __name__) # defines blueprint

# defines our login page

@auth.route("/login")
def login():
	return render_template("login.html", boolean = True) # displays basic text on site with <p> tags </p> 
#text is a variable we can access within login.html template
	
	
#defines user log out page
@auth.route("/logout")
def logout():
	return "<p>Logout</p>"
	
	
#defines user sign up page
@auth.route("/sign-up")
def sign_up():
	return render_template("sign_up.html") # displays the template created from our sign_up.html file
	
	
