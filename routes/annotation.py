from flask import Blueprint, request, jsonify, g
from models import Image, Annotation, annotation_schema, annotations_schema, db
from auth_middleware import token_required
from werkzeug.utils import secure_filename
from flask_cors import cross_origin

annotation = Blueprint('Annotation', __name__)



@annotation.route('/annotations', methods=['POST', 'OPTIONS'])
def addAnnotation():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    print(data)
    try:
        new_annotation = Annotation(x1=data['x1'],
                               y1=data['y1'],
                               x2=data['x2'],
                               y2=data['y2'],
                               imageId=data['imageId'],
                               className=data['className'],
                               classId=data['classId'],
                               color=data['color'])
        
        db.session.add(new_annotation)
        db.session.commit()
        return annotation_schema.jsonify(new_annotation), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@annotation.route('/<int:imageId>', methods=['GET'])
def getAnnotation(imageId):
    try:
        currentAnnoptation = Annotation.query.filter_by(imageId=imageId).all()
        return annotations_schema.jsonify(currentAnnoptation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@annotation.route('/<int:annotationId>', methods=['DELETE'])
def deleteAnnotation(annotationId):
    try:
        currentAnnotation = Annotation.query.get_or_404(annotationId)
        db.session.delete(currentAnnotation)
        db.session.commit()
        return jsonify({"message": "Annotation deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

