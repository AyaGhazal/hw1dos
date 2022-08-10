from crypt import methods
from xml.dom.minidom import TypeInfo
from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "hello"

@app.route("/purchase/<id>",methods=['GET'])
def purchase(id):
    idInt = int(id)
    result=requests.get("http://192.168.56.101:5000/info/{}".format(idInt))
    if(result.json()["info"][0]["NUMBERS"]>0):
        buyResult=requests.put("http://192.168.56.101:5000/queryNumbers/{}".format(idInt),data={'AMOUNTS':1})
        return buyResult.content
    else :return ({"msg":"out of stock!!"})
    
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=6000)