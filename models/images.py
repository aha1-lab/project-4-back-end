from .base import db, ma
from enum import Enum


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(80), nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    def __init__(self, name, description, type):
        self.name = name
        self.description = description
        self.type = type

class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'type')
    
    type = ma.Method("get_type_value")
    
    def get_type_value(self, obj):
        return obj.type.value if obj.type else None


Images_schema = ImagesSchema()
Imagess_schema = ImagesSchema(many=True )