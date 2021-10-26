import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import current_user, user
from .models import User
# encrypts password, no inverse function
from werkzeug.security import generate_password_hash, check_password_hash
from . import UPLOAD_FOLDER, db
from flask_login import login_user, login_required, logout_user, current_user

# defines blueprint of our app aka a bunch of ursl

auth = Blueprint("auth", __name__)  # defines blueprint

# defines our login page


# URL -> GET request, POST -> Submit button
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # filter all the users by email and each user mush have a unique email
        user = User.query.filter_by(email=email).first()
        if user:
            # if these hashes are the same
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)  # keeps user logged in
                # takes user to their home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    data = request.form  # Access form attribute of the request
    print(data)
    # displays basic text on site with <p> tags </p>
    return render_template("login.html", user=current_user)
# text is a variable we can access within login.html template


# defines user log out page
@auth.route("/logout")
@login_required  # can only logout in logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# defines user sign up page
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
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
                flash('Account Created!.', category='success')
                # takes the new user to the home page
                return redirect(url_for('views.home'))
    # displays the template created from our sign_up.html file
    return render_template("sign_up.html", user=current_user)
