from datetime import timezone
from enum import unique

from sqlalchemy.orm import defaultload
from . import db  # from website import db
from flask_login import UserMixin  # gets user modules
from sqlalchemy.sql import func  # auto add the date


####################################################################################
# THIS IS FOR THE ENGINEERS ONLY, DO NOT UNCOMMENT OTHER TEAM OR APP WILL NOT WORK #
#####################################################################################
#from . import db, migrate, app # from website import db
#from flask_login import UserMixin  # gets user modules
#from sqlalchemy.sql import func  # auto add the date
#from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

#from flask_user.forms import RegisterForm
#from flask_wtf import FlaskForm
#from wtforms import StringField, SubmitField, validators

#from functools import wraps
#from flask import g, flash, redirect, url_for, request


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # identify the note
    data = db.Column(db.String(10000))  # setmax string size of our notes
    # give notes a date when created
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # associate different info for different users
    # foriegn key: column references another column; one to many
    # associate a user to a note
    # one to many relationship, one user, many notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    # define the layouts for our objects
    # setup multiple users with login info
    # primary key, to uniquely id all users
    id = db.Column(db.Integer, primary_key=True)
    # users cannot have same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')  # create list of user's notes
    group = db.relationship('Group')

class Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(150))
    group_password = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
 

####################################################################################
# THIS IS FOR THE ENGINEERS ONLY, DO NOT UNCOMMENT OTHER TEAM OR APP WILL NOT WORK #
#############################################################################################
# we will need these new modes to help determine what role each user has if we want to do   #
# add permissions to files and or set group admins                                          #
#############################################################################################

    

#class User(db.Model, UserMixin):

 #   __tablename__ = 'users'
 #   id = db.Column(db.Integer, primary_key=True)
    # users cannot have same email
 #   email = db.Column(db.String(150), server_default=u'', unique=True)
 #   email_confirmed_at = db.Column(db.DateTime())
 #   password = db.Column(db.String(150))
 #   active = db.Column(db.Boolean(), nullable=False, server_default='0')
    
    #username = db.Column(db.String(150))
    
    #user fields
    
    # active user info
 #   active = db.Column(db.Boolean(), server_default='0')
 #   first_name = db.Column(db.String(150), server_default=u'')
 #   last_name = db.Column(db.String(150), server_default=u'')
    
 #   roles = db.relationship('Role', secondary = 'user_roles', backref=db.backref('users', lazy = 'dynamic'))
    


  
  
#Define the role data-model
#class Role(db.Model):
#	__tablename__ = 'roles'
#	id = db.Column(db.Integer(), primary_key=True)
#	name = db.Column(db.String(150), server_default = u'', unique=True)
#	label = db.Column(db.Unicode(255), server_default=u'') # for display purposes

#Define the UserRoles association table
#class UserRoles(db.Model):
#	__tablename__ = 'user_roles'
#	id = db.Column(db.Integer(), primary_key=True)
#	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete ='CASCADE'))
#	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete = 'CASCADE'))
 
#user profile form
#class UserProfileForm(FlaskForm):
#	first_name = StringField('First name', validators= [ validators.DataRequired('First name is required')])
#	Last_name = StringField('Last name', validators= [ validators.DataRequired('Last name is required')])
#	submit = SubmitField('Save')


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
#class MyRegisterForm(RegisterForm):
#     first_name = StringField('First name', validators=[validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[validators.DataRequired('Last name is required')])        
        
        
        
        
    
