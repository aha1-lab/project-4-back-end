from .base import db, ma

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(225), nullable=False)
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    annotation = db.relationship('Annotation', cascade="all,delete",  backref='classes', lazy=True)

    def __init__(self, className, projectId):
        self.className = className
        self.projectId = projectId

class ClassesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'className', 'projectId')
    
    project = ma.Nested('ProjectSchema', only=('id', 'name', 'description', 'type'))

classes_schema = ClassesSchema()
classess_schema = ClassesSchema(many=True )