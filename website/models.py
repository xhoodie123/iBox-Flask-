from enum import unique
from sqlalchemy.orm import defaultload
from . import db  # from website import db
from flask_login import UserMixin  # gets user modules
from sqlalchemy.sql import func  # auto add the date
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from functools import wraps
from flask import g, flash, redirect, url_for, request


class User(db.Model, UserMixin):
    # define the layouts for our objects
    # setup multiple users with login info
    # primary key, to uniquely id all users
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # users cannot have same email
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))


class LoginForm(Form):

    username = StringField('Username', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Room')
