
from time import time
from time import sleep
import boto3
import botocore
from gpiozero import MotionSensor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime as datetime
import json

from gpiozero import LED,Buzzer,Button
import serial
from rpi_lcd import LCD


host = "a7a2q7mpz3rzq-ats.iot.us-east-1.amazonaws.com"
rootCAPath = "AmazonRootCA1.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("p1828120basicPubSub1")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	object = message.payload
	print(object)
	#print(message.payload.temperature)
	#print(message[temperature])
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

my_rpi.connect()
pir = MotionSensor(27, sample_rate=5,queue_len=1)
full_path = '/home/pi/Desktop/image1.jpg'
greenLED = LED(20)
redLED = LED(21)
buzzer = Buzzer(5)
button = Button(26, pull_up=False)
lcd = LCD()


human = 0

# Set the filename and bucket name
BUCKET = 'sp-p1828120-s3-bucket' # replace with your own unique bucket name
location = {'LocationConstraint': 'us-east-1'}
file_path = "/home/pi/Desktop"
file_name = "image1.jpg"

def listen_topic():
	my_rpi.subscribe("sensors/led/red",1, customCallback1)
	my_rpi.subscribe("sensors/led/green",1, customCallback2)
	my_rpi.subscribe("sensors/buzzer",1, customCallback3)
		

# Custom MQTT message callback
def customCallback1(client, userdata, message):
	print("Received a new message: ")
	object = message.payload
	print(object)
	#print(message.payload.temperature)
	#print(message[temperature])
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	print(message.payload)
	str = '{\"state\": 1}'
	msg = message.payload
	print("str is" + str)
	if msg == str:
		print("red turn on")
		redLED.on()
		
	else:
		print("red turn off")
		redLED.off()

def customCallback2(client, userdata, message):
	print("Received a new message: ")
	object = message.payload
	print(object)
	#print(message.payload.temperature)
	#print(message[temperature])
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	print(message.payload)
	str = '{\"state\": 1}'
	msg = message.payload
	print("str is" + str)
	if msg == str:
		print("green turn on")
		greenLED.on()
		
	else:
		print("green turn off")
		greenLED.off()

def customCallback3(client, userdata, message):
	print("Received a new message: ")
	object = message.payload
	print(object)
	#print(message.payload.temperature)
	#print(message[temperature])
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	print(message.payload)
	str = '{\"state\": 1}'
	msg = message.payload
	print("str is" + str)
	if msg == str:
		print("bz turn on")
		buzzer.on()
		
	else:
		print("bz turn off")
		buzzer.off()
		
		


def main():
	listen_topic()


while True:
	main()
	sleep(2)	
