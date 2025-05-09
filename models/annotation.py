from .base import db, ma

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x1 = db.Column(db.Integer, nullable=False)
    x2 = db.Column(db.Integer, nullable=False)
    y1 = db.Column(db.Integer, nullable=False)
    y2 = db.Column(db.Integer, nullable=False)
    className = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(40), nullable=False)
    classId = db.Column(db.Integer, nullable=False)
    imageId = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    

    def __init__(self, x1, x2, y1, y2, className, classId, imageId, color):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color
        self.className = className
        self.classId = classId
        self.imageId = imageId
        
class AnnotationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'x1', 'x2', 'y1', 'y2', 'className', 'classId', 'imageId', 'color')
    
    image = ma.Nested('ImagesSchema', only=('id', 'imageName', 'projectId'))

annotation_schema = AnnotationSchema()
annotations_schema = AnnotationSchema(many=True )