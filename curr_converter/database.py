from flask import Blueprint,jsonify,request,redirect,url_for
from flask_pymongo import PyMongo
import json
from bson.json_util import dumps


from . import mongo

database = Blueprint('database',__name__)

@database.route('/sign-up',methods=['POST'])
def sign_up():
    if request.method == "POST":
        id = request.json['id']
        name = request.json['name']
        if id and name:
            id = mongo.db.user.insert_one({'id':id,'name':name})
            return jsonify({"success":True,"message":"User Added Successfully"})
        else:
            return jsonify({"success":False,"message":"Enter Complete Data"})