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
    final_result = {"date":date,
                    "conversion":f"{from_curr.upper()} to {to_curr.upper()}",
                    "input":f"{amount} {from_curr.upper()}",
                    "output":f"{result['result']} {to_curr.upper()}",
                    "success":result['success']}
    return final_result


@appHandler.route('/get-latest')
def get_latest():
    args = request.args
    to_curr = args.get('to')
    from_curr = args.get('from')
    print(to_curr)
    print(type(to_curr))
    '''
        if len(to_curr.split(','))>1:
        tmp=list(to_curr.split(','))
        print(tmp)
        to_curr = ",".join(tmp)
    '''
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={to_curr}&base={from_curr}"
    print(url)
    payload = {}
    headers= {
        "apikey": "xVS82OxCi3LPHFSvNKduOEGUYottHFJT"
        }
    response = requests.request("GET", url, headers=headers, data = payload)
    result  = response.json()
    return result
    