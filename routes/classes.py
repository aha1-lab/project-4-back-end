from flask import Blueprint, request, jsonify, g
from models import db, Classes,classes_schema, classess_schema
from auth_middleware import token_required
from werkzeug.utils import secure_filename
from flask import current_app


classes = Blueprint('classes', __name__)

@classes.route('/', methods=['POST'])
@token_required
def addClass():
    try:
        data = request.get_json()
        newClass =  Classes(className=data['className'],
                            projectId=data['projectId'])
        
        db.session.add(newClass)
        db.session.commit()
        return classes_schema.jsonify(newClass), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@classes.route('/<int:projectId>', methods=['GET'])
@token_required
def get_classes(projectId):
    try:
        classes = Classes.query.filter_by(projectId=projectId).all()
        return classess_schema.jsonify(classes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@classes.route('/<int:classId>', methods=['DELETE'])
@token_required
def delete_project(classId):
    try:
        cls = Classes.query.get_or_404(classId)
        db.session.delete(cls)
        db.session.commit()
        return jsonify({"message": "Class deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

