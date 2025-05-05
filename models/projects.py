from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from enum import Enum

db = SQLAlchemy()
ma = Marshmallow()


class ProjectType(Enum):
    object_detection = 'Object Detection'
    image_classification = 'Image Classification'
    image_segmentation = 'Image Segmentation'




class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(ProjectType), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'type')
    
    type = ma.Method("get_type_value")
    
    def get_type_value(self, obj):
        return obj.type.value if obj.type else None


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True )