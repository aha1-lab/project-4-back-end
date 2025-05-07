from flask import Blueprint, request, jsonify
from models import db, user_schema, User
import os
import jwt
from dotenv import load_dotenv
load_dotenv()

from flask_bcrypt import Bcrypt
users = Blueprint('users', __name__)

bcrypt = Bcrypt()

@users.route('/sign-up', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        hashPassword = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        newUser = User(
            username=data['username'],
            email=data['email'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            password=hashPassword)
        
        db.session.add(newUser)
        db.session.commit()
        return user_schema.jsonify(newUser), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@users.route('/sign-in', methods=['POST'])
def sign_in():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        if not bcrypt.check_password_hash(user.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Construct the payload
        payload = {"username": user.username, "id": user.id}
        # Create the token, attaching the payload
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
        return jsonify({"token": token}), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users.route('/', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        return user_schema.jsonify(users, many=True), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400