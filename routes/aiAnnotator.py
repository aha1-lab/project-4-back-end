from flask import Blueprint, request, jsonify, g
from auth_middleware import token_required

from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology
from autodistill.utils import plot
import cv2

aiAnnotator = Blueprint('aiAnnotator', __name__)

def processImage(data, imagePath_):
    # Initialize model
    base_model = GroundedSAM(
        ontology=CaptionOntology(data)
    )

    imagePath = './static/uploads/'+ imagePath_
    image = cv2.imread(imagePath)

    # Run detection
    results = base_model.predict(imagePath)

    # Get bounding boxes and class IDs
    boxes = results.xyxy  # shape: (N, 4)
    class_ids = results.class_id  # shape: (N,)
    classes = base_model.ontology.classes()  # list of class names

    for i in range(len(boxes)):
        x_min, y_min, x_max, y_max = map(int, boxes[i])
        class_id = int(class_ids[i])
        class_name = classes[class_id] if class_id < len(classes) else "unknown"

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
        cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 0, 0), 2)

    return image

@aiAnnotator.route('/', methods=['POST'])
@token_required
def oneImageDetection():
    try:
        data = request.get_json()
        print(data)
        imagePath = data['imagePath']
        del data['imagePath']
        img_with_boxes = processImage(data, imagePath)
        data = request.get_json()
        newPath = 'detections/'+ imagePath.split('/')[-1]
        savedPath = "static/uploads/"+newPath
        print(savedPath)
        cv2.imwrite(savedPath, img_with_boxes)
        data['imageName'] = newPath
        print(data)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400