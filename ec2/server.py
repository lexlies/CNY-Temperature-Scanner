from flask import Flask, render_template, jsonify,request
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime as datetime
from time import time

app = Flask(__name__)

import dynamodb
import jsonconverter as jsonc
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

import botocore


host = "a7a2q7mpz3rzq-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "AmazonRootCA1.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("p1828120basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

my_rpi.connect()
@app.route("/api/getdata",methods=['POST','GET'])
def apidata_getdata():
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb.get_data_from_dynamodb()), 
             'title': "IoT Data"}
            print (data)
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

@app.route("/")
def home():
    return render_template("index.html")

#Control red LED
def redledOn():
    #publish to somewhere
    #code to publish to cloud
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 1
    my_rpi.publish("sensors/led/red", json.dumps(message), 1)
    return "red LED is on"

def redledOff():
    #publish to somwhere
    #code to publish to cloud
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 0
    my_rpi.publish("sensors/led/red", json.dumps(message), 1)
    return "red LED is Off"


@app.route("/writeredLED/<status>")
def writePin(status):

   if status == 'On':
     response = redledOn()
   else:
     response = redledOff()

   return response

#Control green LED
def greenledOn():
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 1
    my_rpi.publish("sensors/led/green", json.dumps(message), 1)
    return "green LED is on"

def greenledOff():
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 0
    my_rpi.publish("sensors/led/green", json.dumps(message), 1)
    return "green LED is Off"


@app.route("/writegreenLED/<status>")
def writePin1(status):

   if status == 'On':
     response = greenledOn()
   else:
     response = greenledOff()

   return response


#Control Buzz
def BuzzOn():
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 1
    my_rpi.publish("sensors/buzzer", json.dumps(message), 1)
    return "Buzzer is buzzing"

def BuzzOff():
    message = {}  
    now = datetime.datetime.now()
    message["state"] = 0
    my_rpi.publish("sensors/buzzer", json.dumps(message), 1)
    return "Buzzer is Off"


@app.route("/writeBuzzer/<status>")
def writePin2(status):

   if status == 'On':
     response = BuzzOn()
   else:
     response = BuzzOff()

   return response

@app.route("/getTemp",methods = ['POST', 'GET'])
def getTemp():
    #suscribe from Cloud
    #humidity, temperature = Adafruit_DHT.read_retry(11, pin)
    if request.method == 'POST' or request.method == 'GET':
        try:
            data = {'chart_data': jsonc.data_to_json(dynamodb.get_data_from_dynamodb1()), 
             'title': "IoT Data"}
            print (data)
            return jsonify(data)

        except:
            import sys
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

    data = {'temperature': temperature}

    #print(data)
    #return jsonify(data)


app.run(debug=True,port=8001,host="0.0.0.0")
