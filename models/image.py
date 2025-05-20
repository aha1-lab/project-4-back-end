from .base import db, ma

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(225), nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    annotation = db.relationship('Annotation', backref='image', lazy=True)

    def __init__(self, imageName, projectId):
        self.imageName = imageName
        self.projectId = projectId

class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'imageName', 'projectId')
    
    project = ma.Nested('ProjectSchema', only=('id', 'name', 'description', 'type'))

Image_schema = ImagesSchema()
Images_schema = ImagesSchema(many=True )