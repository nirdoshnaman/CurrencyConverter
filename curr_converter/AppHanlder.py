from flask import Blueprint,jsonify,request
import requests
import datetime
endpoints = Blueprint('endpoints',__name__)

@endpoints.route('/')
def login():
    return "<h1>Login Page</h1>"

@endpoints.route('/search/<curr_code>')
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