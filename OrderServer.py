from crypt import methods
from xml.dom.minidom import TypeInfo
from flask import Flask, request, jsonify
import json
import requests
import itertools
app = Flask(__name__)

IPs=["http://11.111.11.4:6001"]
iterator_IPs = itertools.cycle(IPs)
@app.route("/")
def home():
    return "hello"

@app.route("/purchase/<id>",methods=['GET'])
def purchase(id):
    idInt = int(id)
    result= requests.get(next(iterator_IPs)+"/info/{}".format(idInt))
    if(result.json()["info"][0]["NUMBERS"]>0):
        buyResult=requests.put(next(iterator_IPs)+"/queryNumbers/{}".format(idInt),data={'AMOUNTS':1})
        buyResult=requests.put(next(iterator_IPs)+"/queryNumbers/{}".format(idInt),data={'AMOUNTS':1})
        return buyResult.content
    else :return ({"msg":"out of stock!!"})
    
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=6001)