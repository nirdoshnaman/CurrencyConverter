from flask import Flask
from flask_pymongo import PyMongo


mongo = PyMongo()


def create_app():
    app = Flask(__name__,instance_relative_config=False)
    app.config['SECRET_KEY'] = 'naman'
    app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"
    mongo.init_app(app)

    from .appHanlder import appHandler

    app.register_blueprint(appHandler,url_prefix='/')
    
    return app