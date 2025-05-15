from .base import db, ma

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x1 = db.Column(db.Integer, nullable=False)
    x2 = db.Column(db.Integer, nullable=False)
    y1 = db.Column(db.Integer, nullable=False)
    y2 = db.Column(db.Integer, nullable=False)
    imageId = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    classId = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    

    def __init__(self, x1, x2, y1, y2, classId, imageId):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.classId = classId
        self.imageId = imageId
        
class AnnotationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'x1', 'x2', 'y1', 'y2', 'classId', 'imageId')
    
    image = ma.Nested('ImagesSchema', only=('id', 'imageName', 'projectId'))

annotation_schema = AnnotationSchema()
annotations_schema = AnnotationSchema(many=True )