from flask import Flask,request,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'naman'
    app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"

    mongo = PyMongo(app)

    from .AppHanlder import endpoints

    app.register_blueprint(AppHanlder,url_prefix='/login/')

    return app