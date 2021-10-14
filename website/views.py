from flask import Blueprint, render_template, request, flash
from flask.helpers import flash
from flask_login import login_required, current_user
from . models import Note
from . import db
views = Blueprint("views", __name__)

@views.route("/", methods = ['GET', 'POST']) #Note post Method is allowed
@login_required # cannot get to homepage if not logged in
def home():
	if request.method == 'POST':
		note = request.form.get('note')
		if len(note) < 1:
			flash('Note is short', category= 'error')
		else:
			new_note = Note(data = note, user_id = current_user.id) # add note to database and associate with user
			db.session.add(new_note)
			db.session.commit()
			flash('Note added', category= 'success')
	return render_template("home.html", user = current_user) # ref current user to check if logged in
