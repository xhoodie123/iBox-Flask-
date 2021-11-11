from datetime import timezone
from enum import unique

from sqlalchemy.orm import defaultload
from . import db, migrate, app # from website import db
from flask_login import UserMixin  # gets user modules
from sqlalchemy.sql import func  # auto add the date
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

from functools import wraps
from flask import g, flash, redirect, url_for, request






    
    

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # users cannot have same email
    email = db.Column(db.String(150), server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(150))
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    
    #username = db.Column(db.String(150))
    
    #user fields
    
    # active user info
    active = db.Column(db.Boolean(), server_default='0')
    first_name = db.Column(db.String(150), server_default=u'')
    last_name = db.Column(db.String(150), server_default=u'')
    
    roles = db.relationship('Role', secondary = 'user_roles', backref=db.backref('users', lazy = 'dynamic'))
    


  
  
#Define the role data-model
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(150), server_default = u'', unique=True)
	label = db.Column(db.Unicode(255), server_default=u'') # for display purposes

#Define the UserRoles association table
class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete ='CASCADE'))
	role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete = 'CASCADE'))
 
#user profile form
class UserProfileForm(FlaskForm):
	first_name = StringField('First name', validators= [ validators.DataRequired('First name is required')])
	Last_name = StringField('Last name', validators= [ validators.DataRequired('Last name is required')])
	submit = SubmitField('Save')


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
     first_name = StringField('First name', validators=[validators.DataRequired('First name is required')])
     last_name = StringField('Last name', validators=[validators.DataRequired('Last name is required')])        
        
        
        
        
        
