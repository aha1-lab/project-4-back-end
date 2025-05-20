from autodistill_grounded_sam import GroundedSAM
from autodistill.detection import CaptionOntology
import cv2

def processImage(data):
    # Initialize model
    base_model = GroundedSAM(
        ontology=CaptionOntology(data)
    )

    imagePath = "./static/uploads/1/1/53.jpg"
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

        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)

    return image

# Call the function and get the image
img_with_boxes = processImage({ "a nut with a hexagonal shape and a hole in the middle" : "nut"})

# Show image (optional)
import matplotlib.pyplot as plt

# Convert from BGR to RGB (OpenCV uses BGR)
img_rgb = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)

plt.imshow(img_rgb)
plt.title("Detections")
plt.axis("off")
plt.show()
# Save image
# cv2.imwrite("output_with_boxes.jpg", img_with_boxes)
