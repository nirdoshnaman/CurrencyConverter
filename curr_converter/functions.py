import requests
from flask import request,jsonify
from datetime import date

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