import re
import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from sqlalchemy.sql.functions import current_user, user
from .models import User, UserRoles, Role
# encrypts password, no inverse function
from werkzeug.security import generate_password_hash, check_password_hash
from . import UPLOAD_FOLDER, db
from flask_login import login_user, login_required, logout_user, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
# defines blueprint of our app aka a bunch of ursl

auth = Blueprint("auth", __name__)  # defines blueprint





#initializes db

def init_db():
	db.drop_all()
	db.create_all()
	create_users()
	
#creates users
def create_users():
	db.create_all()
	
	#adding roles
	
	admin_role = find_or_create_role('admin', u'Admin')
	
	#add users
	user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
	user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')
	db.session.commit() 
	


#creates or detemines roles
def find_or_create_role(name, label):
	role = Role.query.filter(Role.name==name).first()
	if not role:
		role = Role(name=name, label = label)
		db.session.add(role)
	return role

#creates or determines users	
def find_or_create_user(first_name, last_name, email, password, role = None):

	user = User.query.filter(User.email == email).first()
	if not user:
		user = User( email=email, first_name = first_name, last_name = last_name, passowrd = current_app.user_manager.password_manager.hash_password(password), active = True, email_confirmed_at = datetime.datetime.utcnow())
	if role:
		user.roles.append(role)
	db.session.add(user)
	return user	
	



#defines user signup-page
	
@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')  # gets all user input for user info
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists!', category = 'error')
        if len(email) < 4:
            flash('Email too short!', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than one character!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(password1) < 7:
            flash('Password too short!', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))  # creates a new user
            if 0 == 2:
                flash('Account already created, login!', category= 'error') #placeholder for future check function
            else:
                db.session.add(new_user)  # adds the new user to the database
                db.session.commit()  # tell the database to update
                # keep newly created user logged in
                login_user(new_user, remember=True)
                flash('Account Created!', category='success')
                # takes the new user to the home page
                return redirect(url_for('views.home'))
    # displays the template created from our sign_up.html file
    return render_template("sign_up.html", user=current_user)



