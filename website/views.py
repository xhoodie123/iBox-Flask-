from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import flash, send_from_directory
from flask_login import login_required, current_user
from . models import Note
from . import db
import json  # for delete note
from werkzeug.utils import secure_filename, send_file # for securing uploaded file/download file
from flask import Flask, redirect, send_file  # needed for downloads section
from . import UPLOAD_FOLDER
import os
from flask import current_app

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])  # Note post Method is allowed
@login_required  # cannot get to homepage if not logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is short', category='error')
        else:
            # add note to database and associate with user
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    # ref current user to check if logged in
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # turn string  into python dictionary object
    note = json.loads(request.data)
    noteId = note['noteId']  # access note id
    note = Note.query.get(noteId)  # find the note
    if note:  # if note belongs to the user
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})  # return empty response


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
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            print("saved file successfully")
    # send file name as parameter to downlad
        return redirect('/downloadfile/' + filename)

    return render_template('upload_file.html', user=current_user)

# download API section


@views.route('/downloadfile/<filename>', methods=['GET'])
def download_file(filename):
    return render_template('download_file.html', user = current_user, value = filename)

@views.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
    #return send_from_directory(file_path, as_attachment=True, attachment_filename='')
# end download api section

#@views.route("/files")
#def list_files():
#    files = []
#    for filename in os.listdir(UPLOAD_FOLDER):
#        path = os.path.join(UPLOAD_FOLDER, filename)
#        if os.path.isfile(path):
#            files.append(filename)
#        return jsonify(files)
