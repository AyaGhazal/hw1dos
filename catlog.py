from crypt import methods
from flask import Flask, request, jsonify
import json
import json


app = Flask(__name__)

@app.route("/")
def home():
    return "hello world"

@app.route("/info/<id>",methods=['GET'])
def info(id):
    with open('C:\Users\Google Tech\Downloads\BazarProject_Amna_Rawan-master\BazarProject_Amna_Rawan-master\BookDB2.json', 'r') as DBfile:
        data = DBfile.read()
        jsonObject = json.loads(data)
        BooksRecords = jsonObject['BOOK']
        idInt = int(id)
        result=[BooksRecordsItem for BooksRecordsItem in BooksRecords if BooksRecordsItem['ID'] == idInt]
        if len(result)==0:
            return  "No such Book Found!!"
        return jsonify({"info":[{"NUMBERS":result[0]['NUMBERS'],"Title":result[0]['NAME'],"COST":result[0]['COST']}]})

@app.route("/search/<topic>",methods=['GET'])
def search(topic):
    with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'r') as DBfile:
        data = DBfile.read()
        jsonObject = json.loads(data)
        BooksRecords = jsonObject['BOOK']
        result=[BooksRecordsItem for BooksRecordsItem in BooksRecords if BooksRecordsItem['TOPIC'] == topic]
        arr=[]
        i=0
        for x in result:
            arr.append({"ID":result[i]["ID"],"NAME":result[i]['NAME']})
            i=i+1
        if len(result)==0:
            return  "No Such Book That Have The Same Topic Found!!"
        return jsonify([arr])

@app.route("/updateCost/<id>",methods=['PUT'])
def updateCost(id):
    bodyData=request.data
    with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'r') as DBfile:
        data = DBfile.read()
        jsonObject = json.loads(data)
        BooksRecords = jsonObject['BOOK']
    DBfile.close() 
    idInt = int(id)
    for items in BooksRecords:
      if items["ID"] == idInt:
        items["COST"]=int(request.form.get('COST'))   
        newJson=({"BOOK": BooksRecords})
        with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'w') as DBfileWrite:
         json.dump(newJson, DBfileWrite,indent=3)
        return "success"

@app.route("/queryNumbers/<id>",methods=['PUT'])
def queryNumbers(id):
    bodyData=request.data
    with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'r') as DBfile:
        data = DBfile.read()
        jsonObject = json.loads(data)
        BooksRecords = jsonObject['BOOK']
    DBfile.close() 
    idInt = int(id)
    amountInt = int(request.form.get('AMOUNTS'))
    for items in BooksRecords:
      if items["ID"] == idInt:
            items["NUMBERS"]=items["NUMBERS"]-amountInt
            newJson=({"BOOK": BooksRecords})
            with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'w') as DBfileWrite:    
             json.dump(newJson, DBfileWrite,indent=3)
            return "success!the name of book you buied is [{}".format(items["NAME"]+"]")
    else: return "NO such book that have same id"

@app.route("/IncreaseNumbers/<id>",methods=['PUT'])
def IncreaseNumbers(id):
    with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'r') as DBfile:
        data = DBfile.read()
        jsonObject = json.loads(data)
        BooksRecords = jsonObject['BOOK']
    DBfile.close() 
    idInt = int(id)
    amountInt = int(request.form.get('AMOUNTS'))
    for items in BooksRecords:
      if items["ID"] == idInt:
            items["NUMBERS"]=items["NUMBERS"]+amountInt 
            newJson=({"BOOK": BooksRecords})
            with open('/home/aya/Desktop/pyth/venv/hwdos/BooksDB.json', 'w') as DBfileWrite:
             json.dump(newJson, DBfileWrite,indent=3)
            return jsonify("success")
      else: return "NO such book that have same id"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6002)
