from .base import db, ma
from enum import Enum



class ProjectType(Enum):
    object_detection = 'Object Detection'
    image_classification = 'Image Classification'
    image_segmentation = 'Image Segmentation'


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(ProjectType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Image', backref='project', lazy=True)
    classes = db.relationship('Classes', backref='project', lazy=True)

    def __init__(self, name, description, type, user_id):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.type = type

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'type', 'image', 'user_id')
    
    type = ma.Method("get_type_value")
    image = ma.Nested('ImagesSchema', many=True)
    
    def get_type_value(self, obj):
        return obj.type.value if obj.type else None


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True )