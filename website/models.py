from datetime import timezone
from enum import unique

from sqlalchemy.orm import defaultload
from . import db  # from website import db
from flask_login import UserMixin  # gets user modules
from sqlalchemy.sql import func  # auto add the date


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

#class Group(db.Model, UserMixin):
    #id = db.Column(db.Integer, primarykey = True)
    #group_name = db.Column(db.String(150))
    #group_password = db.Column(db.String(150))
    #user_id = db.Column(db.integer, db.ForeignKey('user.id'))
