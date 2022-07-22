from tkinter import W
from flask import Flask, request, jsonify
import json
#import requests
from time import ctime
import itertools
from datetime import datetime
app = Flask(__name__)
cache = []
import time

#List of ip address for catlog servers
IPs=["http://192.168.56.101:6002"]
iterator_IPs = itertools.cycle(IPs)

#List of ip address for order servers
OrdersIPs=["http://192.168.56.102:6001"]
iterator_OrdersIPs = itertools.cycle(OrdersIPs)

#this function for check if the query inside the cache or not 
def checkCache(query):
    for x in cache:
     if query==x['query']:
         x['count']=x['count']+1
         return x['result']
    return "cache miss"

#this function for doing replacement aldorthim if the cash full
#replace liss query used 
def replacmentAlgo():
      min=cache[0]['count']
      index=0
      w=0
      for y in cache:    
        if y['count']<min :
            min=y['count']
            index=w 
        else: w+=1
      return index

#this function for delete certin id from cashe when write request
def updateCache(id):
    removed=False
    for x in cache:
     str=x['query']
     strid=str.split("/")
     for s in strid:
       if id==s:
         cache.remove(x)
         removed=True
    if removed==True:
        return "removed!"
    else: return "cache miss"
@app.route("/")
def home():
    return "hello world"


#for the next request the next() function call the servers on order
@app.route("/info/<id>",methods=['GET'])
def info(id):
    start =  time.time()
    str0="time before send request: "+ str((time.time())*1000)
    print(str0)
    idInt=int(id)
    end=""
    q=checkCache("/info/{}".format(idInt))
    if q=="cache miss":
        if len(cache)==5: 
         index=replacmentAlgo()
         result=requests.get(next(iterator_IPs)+"/info/{}".format(idInt), verify=False)
         cache[index]={"query":"/info/{}".format(idInt),"result":json.loads(result.content),"count":1}
        else :  
         result=requests.get(next(iterator_IPs)+"/info/{}".format(idInt), verify=False)
         cache.append({"query":"/info/{}".format(idInt),"result":json.loads(result.content),"count":1})
        print(cache)
        end =  time.time() 
        str2="time after send request: "+str((time.time())*1000)
        print(str2)
        str3="avarage time: "+str((end-start)*1000)
        print(str3)
        return (result.content)
    else: 
        print(cache)
        end =  time.time() 
        str2="time after send request: "+str((time.time())*1000)
        print(str2)
        str3="avarage time: "+str((end-start)*1000)
        print(str3)
        return (q)
    
    #if cache miss then check if the cache is not full add to cache but if not call repalecment algo
   
@app.route("/search/<topic>",methods=['GET'])
def search(topic):
    start =  time.time()
    print( "time before send request: "+str((time.time()*1000) ))
    q=checkCache("/search/{}".format(topic))
    if q=="cache miss":
        if len(cache)==5: 
         index=replacmentAlgo()
         result=requests.get(next(iterator_IPs)+"/search/{}".format(topic)) 
         cache[index]={"query":"/search/{}".format(topic),"result":json.loads(result.content),"count":1}
        else : 
         result=requests.get(next(iterator_IPs)+"/search/{}".format(topic)) 
         cache.append({"query":"/search/{}".format(topic),"result":json.loads(result.content),"count":1})
        print(cache) 
        end =  time.time() 
        print("time after send request: "+ str((time.time())*1000) )
        str2="avarge time: "+str((end-start)*1000)
        print(str2)
        return (result.content)
    else:
      print(cache)
      end =  time.time() 
      print("time after send request: "+str((time.time())*1000 ))
      str2="avarge time: "+str((end-start)*1000)
      print(str2)
      return(json.dumps(q[0]) )

    





@app.route("/purchase/<id>",methods=['GET'])
def purchase(id):
     idInt=int(id)
     q=updateCache(id)
     print(q)
     print (cache)
     start =  time.time()
     print( "time before send request: "+str((time.time()*1000) ))
     result=requests.get(next(iterator_OrdersIPs)+"/purchase/{}".format(idInt))
     end =  time.time() 
     print("time after send request: "+ str((time.time())*1000) )
     str2="avarge time: "+str((end-start)*1000)
     print(str2)
     return (result.content)


