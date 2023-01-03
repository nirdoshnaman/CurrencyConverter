from flask import Blueprint,jsonify,request
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import requests

from .functions import convert_one,check_hist,create_hist,update_hist,sign_up,delete_hist
from . import mongo

appHandler = Blueprint('appHandler',__name__)

@appHandler.route('/search-code')
def search_code():
    args = request.args
    code = str(args.get('code')).upper()
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    payload = {}
    headers= {
            "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
            }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()['symbols']
    try:
        return jsonify({"Country Currency":result[code],"Currency Code":code})
    except KeyError:
        res = {"error":"Currency Not Found"}
        return jsonify(res)
        

@appHandler.route('/convert')
def convert():
    args = request.args
    mob = args.get('mob')
    if(len(str(mob))!=10):
        return jsonify({"success":False,"message":"Please Enter a Valid 10 Digit Number"})
    mob = int(mob)
    chk = mongo.db.user.find_one({'mob':mob})

    if not chk:
        sign_up(mob)
        chk = mongo.db.user.find_one({'mob':mob})

    to_curr = args.get('to')
    from_curr = args.get('from')
    amount = args.get('amount')
    date = args.get('date')
    
    list_curr = to_curr.split(',')
    len_curr = len(list_curr)
    
    if len_curr == 1:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_curr}&from={from_curr}&amount={amount}"
        if date == None:
            res=convert_one(url)
            if 'error' in res:
                return res
            if(check_hist(chk)):
                update_hist(mob,res)
                chk = mongo.db.user.find_one({'mob':mob})
            else:
                hist=[]
                hist.append(res)
                create_hist(mob,hist)

            delete_hist(mob)
            return jsonify(res)
        else:
            res=convert_one(url,date)
            if 'error' in res:
                return res
            if(check_hist(chk)):
                update_hist(mob,res)
                chk = mongo.db.user.find_one({'mob':mob})
            else:
                hist=[]
                hist.append(res)
                create_hist(mob,hist)

            delete_hist(mob)
            return jsonify(res)
    elif len_curr >1:
        if date == None:
            result=[]
            for i in range(len_curr):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={list_curr[i]}&from={from_curr}&amount={amount}"
                res=convert_one(url)
                if 'error' in res:
                    return res
                if(check_hist(chk)):
                    update_hist(mob,res)
                    chk = mongo.db.user.find_one({'mob':mob})
                else:
                    hist=[]
                    hist.append(res)
                    create_hist(mob,hist)
                    chk = mongo.db.user.find_one({'mob':mob})
                result.append(res)

            delete_hist(mob)
            return jsonify({"result":result})
        else:
            result=[]
            for i in range(len_curr):
                url = f"https://api.apilayer.com/exchangerates_data/convert?to={list_curr[i]}&from={from_curr}&amount={amount}"
                res=convert_one(url,date)
                if 'error' in res:
                    return res
                if(check_hist(chk)):
                    update_hist(mob,res)
                    chk = mongo.db.user.find_one({'mob':mob})
                else:
                    hist=[]
                    hist.append(res)
                    create_hist(mob,hist)
                    chk = mongo.db.user.find_one({'mob':mob})
                result.append(res)
            delete_hist(mob)
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
    return jsonify(final_result)
    

@appHandler.route('/get-history')
def get_history():
    args = request.args
    mob = args.get('mob')
    if(len(str(mob))!=10):
        return jsonify({"success":False,"message":"Please Enter a Valid 10 Digit Number"})
    mob = int(mob)
    chk = mongo.db.user.find_one({'mob':mob})

    if not chk:
        return jsonify({"success":False,"message":"No Record Found"})

    if(check_hist(chk)):
        res = json.loads(dumps(chk))
        final_result = {"Mobile No.":res['mob'],"History":res['history']}
        return jsonify(final_result)
    else:
        return jsonify({"success":False,"message":"History Not Present!!! Do Some Conversion First :)"})


@appHandler.route('/get-diff')
def get_diff():
    args = request.args
    to_curr = args.get('to')
    from_curr = args.get('from')
    start_date = args.get('start_date')
    end_date = args.get('end_date')


    url = f"https://api.apilayer.com/exchangerates_data/fluctuation?start_date={start_date}&end_date={end_date}&base={from_curr}&symbols={to_curr}"
    payload = {}
    headers= {
    "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()
    try:
        final_result = {"start_date":result['start_date'],
                    "end_date":result['end_date'],
                    "start_rate":result['rates'][str(to_curr).upper()]['start_rate'],
                    "end_rate":result['rates'][str(to_curr).upper()]['end_rate'],
                    "input":result['base'],
                    "output":str(to_curr).upper(),
                    "change":result['rates'][str(to_curr).upper()]['change'],
                    "success":result['success']
                    }
        return jsonify(final_result)
    except KeyError:
        return jsonify({"error":"Key Error","success":False})


@appHandler.route('/search-name')
def search_name():
    args = request.args
    name = args.get('name')
    url = "https://api.apilayer.com/exchangerates_data/symbols"
    payload = {}
    headers= {
            "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
            }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()['symbols']
    list_res = []
    for c_code,c_name in result.items():
        if name in c_name.lower() or name in c_code.lower():
            list_res.append(f"{c_code}:{c_name}")

    if(len(list_res)==0):
        return jsonify({"success":False,"message":"No Currency Found"})
    else:
        return jsonify(list_res)

@appHandler.errorhandler(404)
def not_found(error=None):
    result = {
        'status':404,
        'message':"Not Found " + request.url
    }
    return jsonify(result)