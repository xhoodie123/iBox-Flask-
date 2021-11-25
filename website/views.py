from posixpath import splitext
from flask import Blueprint, render_template, request, flash, jsonify, g, session, url_for, session
from flask.helpers import flash, send_from_directory
from flask_login import login_required, current_user
from . models import User, LoginForm
from . import db, UPLOAD_FOLDER, FILE_EXT
import json  # for delete note
# for securing uploaded file/download file
from werkzeug.utils import secure_filename, send_file
from flask import Flask, redirect, send_file, abort  # needed for downloads section
import os
# for chat
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import emit, join_room, leave_room
from . import socketio
from flask import session
from flask_socketio import emit, join_room, leave_room
import datetime

views = Blueprint("views", __name__)


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') +
         ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('username') +
         ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('username') +
         ' has left the room.'}, room=room)


@login_required
@views.route('/home', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['room'] = form.room.data
        return redirect(url_for('views.chat'))
    elif request.method == 'GET':
        form.username.data = session.get('username', '')
        form.room.data = session.get('room', '')
    return render_template('home.html', form=form, user=current_user)


@login_required
@views.route('/chat')
def chat():
    username = session.get('username', '')
    room = session.get('room', '')
    # if username == '' or room == '':
    #	return redirect(url_for('views.home'))
    return render_template('chat.html', username=username, room=room, user=current_user)


@login_required
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
            if file_ext not in FILE_EXT:  # check if file extension is in whitelist
                print('invalid file type')
                flash('File type not allowed', category='error')
                return redirect(request.url)
            file.save(os.path.join(UPLOAD_FOLDER, filename))  # fixed this
            print("Saved file successfully")

    return render_template('upload_file.html', user=current_user)


# had to be changed to allow button function
@views.route('/uploads/<filename>', methods=['GET'])
def manage_file(filename):
    return render_template('manage_file.html', user=current_user, value=filename)


@views.route('/return-files/<filename>')
def return_files(filename):
    file_path = 'uploads/' + filename
    if filename == '<filename>':
        flash('File not found!', category='error')
        return render_template('home.html', user=current_user)
    return send_file(file_path, as_attachment=True, attachment_filename='')


@views.route('/delete-files/<filename>')
def delete_files(filename):
    if filename == '<filename>':
        flash('File not found!', category='error')
        return render_template('manage_file.html', user=current_user)
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    print('delete successful')
    flash('File deleted', category='success')
    return render_template('uploads.html', user=current_user)


@views.route('/', defaults={'req_path': ''})
@views.route('/<path:req_path>')
def list_file(req_path):
    # joining the base and requested path
    abs_path = os.path.join('website/', req_path)
    if not os.path.exists(abs_path):
        flash('No files have been uploaded!',
              category='error')  # if path doesn't exist
        return render_template('home.html', user=current_user)
    if os.path.isfile(abs_path):
        return manage_file(req_path)
    uploads = os.listdir(abs_path)
    return render_template('uploads.html', uploads=uploads, user=current_user)


@views.route('/group_manager', methods=['GET'])
def group_manager():
    return render_template('group_manager.html', user=current_user)


@views.route('/create_group', methods=['GET'])
def create_group():
    return render_template('create_group.html', user=current_user)


@views.route('/join_group', methods=['GET'])
def join_group():
    return render_template('join_group.html', user=current_user)
