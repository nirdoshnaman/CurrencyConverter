import requests
from flask import request,jsonify
from datetime import date
from . import mongo
import json
from bson.json_util import dumps

def convert_one(url,date=str(date.today())):
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    url = f"{url}&date={date}"
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    final_result = {"date":date,
                    "conversion":f"{result['query']['from']} to {result['query']['to']}",
                    "input":f"{result['query']['amount']} {result['query']['from']}",
                    "output":f"{result['result']} {result['query']['to']}",
                    "success":result['success']
                    }
    return final_result


def check(chk):
    res = json.loads(dumps(chk))
    if 'history' in res:
        return True
    else:
        return False


def create_hist(id,hist):
    mongo.db.user.update_one({'id':id},{'$set':{'history':hist}})

def update_hist(id,hist):
    mongo.db.user.update_one({'id':id},{'$push':{'history':hist}})