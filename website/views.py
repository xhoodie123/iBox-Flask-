from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import flash
from flask_login import login_required, current_user
from . models import Note
from . import db
import json #for delete note
from werkzeug.utils import secure_filename # for secruing uploaded file

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


@views.route('/delete-note', methods=['POST'])
def delete_note():
	note = json.loads(request.data) # turn string  into python dictionary object
	noteId = note['noteId'] # access note id
	note = Note.query.get(noteId) # find the note
	if note: # if note belongs to the user
		if note.user_id == current_user.id:
			db.session.delete(note)
			db.session.commit()
	return jsonify({}) #return empty response


@views.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
	# check if the post request has the file part
		if 'file' not in request.files:
			print('no file')
			return redirect(request.url)
		file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
		if file.filename == '':
			print('no filename')
			return redirect(request.url)
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print("saved file successfully")
	#send file name as parameter to downlad
		return redirect('/downloadfile/'+ filename)

	return render_template('upload_file.html', user = current_user)
