from flask import Flask, jsonify, request, g
import os
from routes import projects, users, bcrypt, annotationRoute, classes
from models import db, ma
from dotenv import load_dotenv
import os
import jwt
from flask_cors import CORS

load_dotenv()

UPLOAD_FOLDER = 'static/uploads'

# Source to create URL to image: https://stackoverflow.com/questions/58341113/why-do-i-need-to-use-static-folder-to-display-images-with-flask
app = Flask(__name__, static_url_path='/images', static_folder='./static/uploads')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.url_map.strict_slashes = False

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)


app.register_blueprint(annotationRoute, url_prefix='/annotations')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(projects, url_prefix='/projects')
app.register_blueprint(classes, url_prefix='/classes')


@app.route('/sign-token', methods=['GET'])
def sign_token():
    user = {
        "id": 1,
        "username": "test",
        "password": "test"
    }
    token = jwt.encode(user, os.getenv('JWT_SECRET'), algorithm="HS256")
    # return token
    return jsonify({"token": token})

@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        return jsonify({"user": decoded_token})
    except Exception as err:
       return jsonify({"err": err})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)