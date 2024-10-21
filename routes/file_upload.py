# routes/file_upload.py
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads/'

file_bp = Blueprint('files', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify(message="No selected file"), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify(message="File uploaded successfully"), 201

    return jsonify(message="File type not supported"), 400