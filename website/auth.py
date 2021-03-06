from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql.functions import current_user, user
from .models import User
# encrypts password, no inverse function
from werkzeug.security import generate_password_hash, check_password_hash
from . import UPLOAD_FOLDER, db

# defines blueprint of our app aka a bunch of ursl
auth = Blueprint("auth", __name__)  # defines blueprint

# defines our login page
# URL -> GET request, POST -> Submit button


@auth.route("/", methods=['GET', 'POST'])
def login():
    if "form-submit" in request.form:
        if request.method == 'POST':
            emailLogin = request.form.get('email-login')
            passwordLogin = request.form.get('password-login')

            # filter all the users by email and each user mush have a unique email
            user = User.query.filter_by(email=emailLogin).first()
            if user:
                # if these hashes are the same
                if check_password_hash(user.password, passwordLogin):
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
    if "form2-submit" in request.form:
        if request.method == 'POST':
            # gets all user input for user info
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists!', category='error')
            if len(email) < 4:
                flash('Email too short!', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than one character!',
                      category='error')
            elif password1 != password2:
                flash('Passwords do not match!', category='error')
            elif len(password1) < 7:
                flash('Password too short!', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))  # creates a new user
                if 0 == 2:
                    # placeholder for future check function
                    flash('Account already created, login!', category='error')
                else:
                    # adds the new user to the database
                    db.session.add(new_user)
                    db.session.commit()  # tell the database to update
                    # keep newly created user logged in
                    login_user(new_user, remember=True)
                    flash('Account Created!', category='success')
                    # takes the new user to the home page
                    return redirect(url_for('views.home'))
    return render_template("startup_page.html", user=current_user)
# text is a variable we can access within login.html template

# defines user log out page


@auth.route("/logout")
@login_required  # can only logout in logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
