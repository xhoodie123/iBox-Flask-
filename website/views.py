from posixpath import splitext
import re
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import flash, send_from_directory
from flask_login import login_required, current_user
from . models import Note
from . import db, UPLOAD_FOLDER, FILE_EXT
import json  # for delete note
# for securing uploaded file/download file
from werkzeug.utils import secure_filename, send_file
from flask import Flask, redirect, send_file, abort  # needed for downloads section
import os
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
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in FILE_EXT: # check if file extension is in whitelist
                print('invalid file type')
                flash('File type not allowed', category='error')   
                return redirect(request.url)  
            file.save(os.path.join(UPLOAD_FOLDER, filename))  # fixed this
            print("Saved file successfully")

    return render_template('upload_file.html', user=current_user)

# manange file API section
@views.route('/uploads/<filename>', methods=['GET']) #had to be changed to allow button function
def manage_file(filename):
    return render_template('manage_file.html', user=current_user, value=filename)


@views.route('/return-files/<filename>') 
def return_files(filename):
    file_path = 'uploads/' + filename
    if filename == '<filename>':
        flash('File not found!', category='error')
        return render_template('home.html', user=current_user)
    return send_file(file_path, as_attachment=True, attachment_filename='')
# end download api section

#start delete file
@views.route('/delete-files/<filename>')
def delete_files(filename):
    if filename == '<filename>':
        flash('File not found!', category='error')
        return render_template('manage_file.html', user=current_user)
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    print('delete successful')
    flash('File deleted', category='success')
    return render_template('uploads.html',user=current_user)
#end dlete file


# start view file list
@views.route('/', defaults={'req_path': ''})
@views.route('/<path:req_path>')
def list_file(req_path):
    abs_path = os.path.join('website/', req_path) # joining the base and requested path
    if not os.path.exists(abs_path):
        flash('No files have been uploaded!',
              category='error')  # if path doesn't exist
        return render_template('home.html', user=current_user)
    if os.path.isfile(abs_path):
        #return send_file(req_path, as_attachment=True, attachment_filename='')
        return manage_file(req_path)
    uploads = os.listdir(abs_path)
    return render_template('uploads.html', uploads=uploads, user=current_user)
# end view file list


#start group manager
@views.route('/group_manager', methods=['GET'])
def group_manager():

    return render_template('group_manager.html', user=current_user)
#end group manager