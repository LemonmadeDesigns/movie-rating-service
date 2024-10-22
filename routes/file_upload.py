# routes/file_upload.py
import os
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from forms import FileUploadForm  # We'll create this

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/uploads')

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_bp = Blueprint('files', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = FileUploadForm()
    
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('files.upload_file'))
        else:
            flash(f'Allowed file types are: {", ".join(ALLOWED_EXTENSIONS)}', 'danger')
    
    # Get list of uploaded files
    uploaded_files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            uploaded_files.append(filename)
    
    return render_template('upload.html', form=form, uploaded_files=uploaded_files)

@file_bp.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    if current_user.role != 'admin':
        flash('Only admins can delete files', 'danger')
        return redirect(url_for('files.upload_file'))
    
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully!', 'success')
    else:
        flash('File not found', 'danger')
    
    return redirect(url_for('files.upload_file'))