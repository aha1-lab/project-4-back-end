from flask import Blueprint, request, jsonify, g
from models import Image, Annotation, Project #ClassList
from auth_middleware import token_required
from werkzeug.utils import secure_filename
from flask import current_app
import shutil 
import yaml

generateDataAndTrain = Blueprint('generateDataAndTrain', __name__)

@generateDataAndTrain.route('/generate/<int:projectId>', methods=['POST'])
def generateData(projectId):
    pass
    # # Get image List
    # imageList = Image.query.filter_by(projectId=projectId).all()
    # project = Project.query.get_or_404(projectId)
    # Classes = ClassList.query.filter_by(projectId=projectId).all()
    # if not imageList:
    #     return jsonify({"error": "No images found for this project"}), 404
    
    # userProjectPath = f"output/{project.user_id}/{projectId}"
    # uploadFolder = current_app.config['UPLOAD_FOLDER']
    # # step 2: get the annotations for each image and generate yoloy txt file
    # for image in imageList:
    #     annotationList = Annotation.query.filter_by(imageId=image.id).all()
    #     fileName = image.imageName.split('/')[-1].split('.')[0]+'.txt'
        
    #     filePath = f"{uploadFolder}/{userProjectPath}/train/labels/{fileName}"
    #     with open(filePath, 'w') as f:
    #         for annotation in annotationList:
    #             classId = Classes.index(annotation.className)
    #             center_x = (annotation.x1 + annotation.x2) / 2
    #             center_y = (annotation.y1 + annotation.y2) / 2
    #             width = annotation.x2 - annotation.x1
    #             height = annotation.y2 - annotation.y1
    #             f.write(f"{classId} {center_x} {center_y} {width} {height}\n")

    #     # step 3: copy image to image folder (source: https://www.geeksforgeeks.org/copy-all-files-from-one-directory-to-another-using-python/)
    #     sourceImage = image.imageName
    #     distanationImage = f"{uploadFolder}/{userProjectPath}/train/images/{image.imageName.split('/')[-1]}"
    #     dest = shutil.copy(sourceImage, distanationImage)

    # # step4: generate the yaml file
    # yamlOutput = {
    #     "train" : "../train/images",
    #     "val"   : "../valid/images",
    #     "test"  : "../test/images",
    #     "nc"    : len(Classes),
    #     "names" : Classes
    # }
    # yamlPath = f"{uploadFolder}/{userProjectPath}/"

    # with open(f"{yamlPath}/data.yaml", 'w') as yamlFile:
    #     yaml.dump(yamlOutput, yamlFile, default_flow_style=False)

@generateDataAndTrain.route('/train/<int:projectId>', methods=['GET'])
def getAnnotation(projectId):
    # Training the model
    # step 1: get the project path
    pass