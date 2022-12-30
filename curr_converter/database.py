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
            return jsonify("User Added Successfully")
        else:
            return jsonify("Enter Complete Data")


@database.route('/update/<int:id>')
def update(id):
    history=[]
    history.append({"hii":"demo"})
    tmp = mongo.db.user.find_one({'id':id})
    if tmp != None:
        mongo.db.user.update_one({'id':id},{'$set':{'history':history}})
        return "User Updated Successfully"
    else: 
        return "User Not Found"


@database.route('check/<int:id>')
def check(id):
    tmp = mongo.db.user.find_one({'id':id})
    if tmp != None:
        res = json.loads(dumps(tmp))
        if 'history' in res:
            return "History Present"
        else:
            return "History not Present"
    else:
        return "Not valid ID"
