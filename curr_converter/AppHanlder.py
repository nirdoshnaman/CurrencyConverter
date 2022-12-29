from flask import Blueprint,jsonify,request
import requests
import datetime


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
    if date == None:
        date = str(datetime.datetime.now()).split()[0]
    url = "https://api.apilayer.com/exchangerates_data/convert?to="+to_curr+"&from="+from_curr+"&amount="+amount+"&date="+date
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    return result