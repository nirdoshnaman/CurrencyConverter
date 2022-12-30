from flask import Blueprint,jsonify,request
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import requests
import datetime 
from .functions import convert_one
from . import mongo

appHandler = Blueprint('appHandler',__name__)


@appHandler.route('/search/<curr_code>')
def search(curr_code):
    code = str(curr_code).upper()
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    status_code = response.status_code
    result = response.json()['symbols']
    return jsonify({"Country Currency":result[code],"Currency Code":code})


@appHandler.route('/convert')
def convert():
    args = request.args
    to_curr = args.get('to')
    from_curr = args.get('from')
    amount = args.get('amount')
    date = args.get('date')
    #id = args.get('id')


    len_curr=to_curr.split(',')


    if len(len_curr) == 1:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_curr}&from={from_curr}&amount={amount}"
        if date == None:
            res=convert_one(url)
            return jsonify(res)
        else:
            res=convert_one(url,date)
            return jsonify(res)
    elif len(len_curr) >1:
        if date == None:
            res=[]
            for i in range(len(len_curr)):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={len_curr[i]}&from={from_curr}&amount={amount}"
                res.append(convert_one(url))
            return jsonify({"result":res})
        else:
            res=[]
            for i in range(len(len_curr)):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={len_curr[i]}&from={from_curr}&amount={amount}"
                res.append(convert_one(url,date))
            return jsonify({"result":res})
    else:
        return jsonify({"At least Enter one Currency Code"})


@appHandler.route('/get-latest')
def get_latest():
    args = request.args
    to_curr = args.get('to')
    from_curr = args.get('from')

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={to_curr}&base={from_curr}"
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    return result
    


@appHandler.route('/get-history')
def get_history():
    args = request.args
    id = int(args.get('id'))
    tmp = mongo.db.user.find_one({'id':id})
    if tmp != None:
        res = json.loads(dumps(tmp))
        final_result = {"Name":res['name'],"History":res['history']}
        return final_result