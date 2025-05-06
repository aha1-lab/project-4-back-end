from flask import Flask, jsonify, request, g
import os
from routes import projects, users, bcrypt
from models import db, ma
from dotenv import load_dotenv
import os
import jwt

load_dotenv()


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(projects, url_prefix='/projects')


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
       return jsonify({"err": err.message})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)