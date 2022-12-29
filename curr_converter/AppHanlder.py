from flask import Blueprint,jsonify,request
import json
import requests
import datetime 
from .functions import convert_one


appHandler = Blueprint('appHandler',__name__)

@appHandler.route('/')
def login():
    return "<h1>Login Page</h1>"

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
    print(to_curr)
    print(type(to_curr))

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={to_curr}&base={from_curr}"
    print(url)
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    return result
    