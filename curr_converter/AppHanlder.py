from flask import Blueprint,jsonify,request
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import requests,time

from .functions import convert_one,check_hist,create_hist,update_hist
from . import mongo

appHandler = Blueprint('appHandler',__name__)


@appHandler.route('/search')
def search():
    args = request.args
    code = str(args.get('code')).upper()
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()['symbols']
    return jsonify({"Country Currency":result[code],"Currency Code":code})


@appHandler.route('/convert')
def convert():
    args = request.args
    id = int(args.get('id'))
    chk = mongo.db.user.find_one({'id':id})

    if not chk:
        return jsonify({"success":False,"message":"Please Enter Valid ID"})

    to_curr = args.get('to')
    from_curr = args.get('from')
    amount = args.get('amount')
    date = args.get('date')
    
    len_curr=to_curr.split(',')


    if len(len_curr) == 1:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_curr}&from={from_curr}&amount={amount}"
        if date == None:
            res=convert_one(url)
            if(check_hist(chk)):
                update_hist(id,res)
            else:
                hist=[]
                hist.append(res)
                create_hist(id,hist)

            return jsonify(res)
        else:
            res=convert_one(url,date)
            if(check_hist(chk)):
                update_hist(id,res)
            else:
                hist=[]
                hist.append(res)
                create_hist(id,hist)
            return jsonify(res)
    elif len(len_curr) >1:
        if date == None:
            result=[]
            for i in range(len(len_curr)):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={len_curr[i]}&from={from_curr}&amount={amount}"
                res=convert_one(url)
                if(check_hist(chk)):
                    update_hist(id,res)
                else:
                    hist=[]
                    hist.append(res)
                    create_hist(id,hist)
                    chk = mongo.db.user.find_one({'id':id})
                result.append(res)
            return jsonify({"result":result})
        else:
            result=[]
            for i in range(len(len_curr)):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={len_curr[i]}&from={from_curr}&amount={amount}"
                res=convert_one(url,date)
                if(check_hist(chk)):
                    update_hist(id,res)
                else:
                    hist=[]
                    hist.append(res)
                    create_hist(id,hist)
                    chk = mongo.db.user.find_one({'id':id})
                result.append(res)
            return jsonify({"result":result})
    else:
        return jsonify({"success":False,"message":"At least Enter one Currency Code :("})


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
    final_result = {"date":result['date'],
                    "base currency":result['base'],
                    "rate":result['rates'],
                    "success":result['success']
                    }
    return final_result
    return result
    


@appHandler.route('/get-history')
def get_history():
    args = request.args
    id = int(args.get('id'))
    chk = mongo.db.user.find_one({'id':id})

    if not chk:
        return jsonify({"success":False,"message":"Please Enter Valid ID"})

    if(check_hist(chk)):
        res = json.loads(dumps(chk))
        final_result = {"Name":res['name'],"History":res['history']}
        return final_result
    else:
        return jsonify({"success":False,"message":"History Not Present!!! Do Some Conversion First :)"})