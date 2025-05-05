from flask import Flask, jsonify, request
import os
from routes.projects import projects
from models.projects import db, ma

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)
app.register_blueprint(projects, url_prefix='/projects')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)