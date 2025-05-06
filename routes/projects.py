from flask import Blueprint, request, jsonify
from models import db, Project, ProjectType, project_schema, projects_schema
from auth_middleware import token_required


projects = Blueprint('projects', __name__)

@projects.route('/', methods=['POST'])
@token_required
def create_project():
    try:
        data = request.get_json()
        project_type = ProjectType[data['type']]
        new_project = Project(name=data['name'], 
                              description=data['description'], 
                              type=project_type)
        
        db.session.add(new_project)
        db.session.commit()
        return project_schema.jsonify(new_project), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



@projects.route('/', methods=['GET'])
@token_required
def get_projects():
    try:
        projects = Project.query.all()
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