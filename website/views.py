from flask import Blueprint, render_template, request, flash, jsonify, g, session
from flask.helpers import flash, send_from_directory
from flask_login import login_required, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from . models import User, Role, UserRoles
from . import db, UPLOAD_FOLDER, migrate, FILE_EXT
import json  # for delete note
# for securing uploaded file/download file
from werkzeug.utils import secure_filename, send_file
from flask import Flask, redirect, send_file, abort  # needed for downloads section
import os

views = Blueprint("views", __name__)






@views.route('/')
def home():
	return render_template('home.html')


@views.route('/member')
@login_required
def profile():
	return_template ('profile.hmtl')



@views.route("/sign-in")
@login_required  # can only logout in logged in
def logout():
    return redirect(url_for('user.logout'))




@views.route('/profile-page', methods = ['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home'))

    # Process GET or invalid POST
    return render_template('profile.html',
                           form=form)



@views.route('/upload-file', methods=['GET', 'POST'])
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
    
#@views.route('/uploads/<filename>', methods=['GET']) 
#def manage_file(filename):
#    return render_template('manage_file.html', user=current_user, value=filename)
    
#@views.route('/uploads', methods=['GET'])
#def file_viewer():

#	workingdir = os.path.abspath(os.getcwd())
#	filepath = workingdir + UPLOAD_FOLDER
#	return send_from_directory(directory=filepath, path =)
#	return render_template('uploads.html', user=current_user)
	
@views.route('/', defaults={'req_path': ''})
@views.route('/<path:req_path>')
def list_file(req_path):
     #joining the base and requested path
    filename = '<filename>'
    abs_path = os.path.join('website/', req_path)
    if not os.path.exists(abs_path):
        flash('No files have been uploaded!',
              category='error')  # if path doesn't exist
        return render_template('home.html', user=current_user)
    if os.path.isfile(abs_path):
        return return_files_tut('sample.pdf')
    uploads = os.listdir(abs_path)
    return render_template('uploads.html', uploads=uploads, user=current_user)


@views.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = 'uploads/' + filename
    if filename == '<filename>':
        flash('File not found!', category='error')
        return render_template('home.html', user=current_user)
    return send_from_directory(file_path, as_attachment=True, path=filename)
# end download api section



# end view file list


#flask app to display pdf on the browser

 


#start group manager
@views.route('/group_manager', methods=['GET'])
def group_manager():
    return render_template('group_manager.html', user=current_user)
#end group manager
