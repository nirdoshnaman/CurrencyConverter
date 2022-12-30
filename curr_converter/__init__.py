from flask import Flask
from flask_pymongo import PyMongo


mongo = PyMongo()


def create_app(config_name):
    app = Flask(__name__,instance_relative_config=False)
    app.config['SECRET_KEY'] = 'naman'
    app.config['MONGO_URI'] = "mongodb://localhost:27017/Users"
    mongo.init_app(app)

    from .appHanlder import appHandler
    from .database import database

    app.register_blueprint(appHandler,url_prefix='/')
    app.register_blueprint(database,url_prefix='/')
    
    return app