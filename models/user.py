from .base import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstName = db.Column(db.String(80), unique=False, nullable=False)
    lastName = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    projects = db.relationship('Project', backref='owner', lazy=True)


    def __init__(self, username, password, email, firstName, lastName):
        self.username = username
        self.password = password
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'firstName', 'lastName')


user_schema = UserSchema()