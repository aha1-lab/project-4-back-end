from flask import Blueprint, request, jsonify
from models import Project, Image, project_schema
from auth_middleware import token_required
from werkzeug.utils import secure_filename
import os 
from flask import current_app

imagesUpload = Blueprint('images', __name__)


ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS



@imagesUpload.route('/upload/<projectId>', methods=['POST'])
def upload_file(projectId):
    project = Project.query.get(projectId)
    if not project:
        return jsonify({"status": "error", "message": "Project not found"}), 404
    
    userProjectPath = f"{project.user_id}/{projectId}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, userProjectPath)
    
    if not os.path.exists(path):
        os.makedirs(path)

    if 'files[]' not in request.files:
        response = jsonify({
            "status": "error",
            "message": "No file part in the request"
        })
        response.status_code = 400
        return response
    
    files = request.files.getlist('files[]')

    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(path, filename)
            file.save(save_path)
            success = True
        else:
            response = jsonify({
                "status": "error",
                "message": "File type not allowed"
            })

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        errors['status'] = 'failed'
        response = jsonify(errors)
        response.status_code = 500
        return response
    if success:
        response = jsonify({
            "message": "File(s) successfully uploaded",
            "status": "success",
        })
        response.status_code = 201
        return response
    else:
        response = jsonify(errors)
        response.status_code = 500
        return response
    