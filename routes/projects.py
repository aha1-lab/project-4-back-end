from flask import Blueprint, request, jsonify, g
from models import db, Project, ProjectType, project_schema, projects_schema, Image, Images_schema
from auth_middleware import token_required
from werkzeug.utils import secure_filename
import os 
from flask import current_app
from datetime import datetime
import random
import string
import time

projects = Blueprint('projects', __name__)

@projects.route('/', methods=['POST'])
@token_required
def create_project():
    current_user_id = g.user["payload"]['id']
    try:
        data = request.get_json()
        project_type = ProjectType[data['type']]
        new_project = Project(name=data['name'], 
                              description=data['description'], 
                              type=project_type,
                              user_id=current_user_id)
        
        db.session.add(new_project)
        db.session.commit()
        return project_schema.jsonify(new_project), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@projects.route('/', methods=['GET'])
@token_required
def get_projects():
    current_user_id = g.user["payload"]['id']
    try:
        # projects = Project.query.all()
        projects = Project.query.filter_by(user_id=current_user_id).all()
        return projects_schema.jsonify(projects), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@projects.route('/<int:id>', methods=['GET'])
@token_required
def get_project(id):
    try:
        project = Project.query.get_or_404(id)
        return project_schema.jsonify(project), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@projects.route('/<int:id>', methods=['PUT'])
@token_required
def update_project(id):
    try:
        data = request.get_json()
        project = Project.query.get_or_404(id)
        
        project.name = data['name']
        project.description = data['description']
        project.type = ProjectType[data['type']]
        
        db.session.commit()
        return project_schema.jsonify(project), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
@projects.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_project(id):
    try:
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@projects.route('/<int:projectId>/images', methods=['GET'])
# @token_required
def getProjectImage(projectId):
    try:
        images = Image.query.filter_by(projectId=projectId)
        return Images_schema.jsonify(images), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENTIONS


def make_unique_filename(filename):
    base, ext = os.path.splitext(secure_filename(filename))
    timestamp = int(time.time())
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{base}_{timestamp}_{rand_str}{ext}"

@projects.route('/<int:projectId>/images', methods=['POST'])
# @token_required
def postProjectImage(projectId):
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
            # filename = secure_filename(file.filename)
            filename = make_unique_filename(file.filename)
            save_path = os.path.join(path, filename)
            file.save(save_path)
            savedPathSeperat = save_path.split('\\')[1] + "/"+ filename
            print(savedPathSeperat)
            success = True
            newImage = Image(imageName=savedPathSeperat,
                             projectId=projectId)
            db.session.add(newImage)
            db.session.commit()
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
    