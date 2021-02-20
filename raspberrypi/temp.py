from time import time
from time import sleep
import boto3
import botocore
from gpiozero import MotionSensor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from picamera import PiCamera
import datetime as datetime
import json

from gpiozero import LED,Buzzer,Button
import serial
from rpi_lcd import LCD


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
pir2 = MotionSensor(19, sample_rate=5,queue_len=1)
full_path = '/home/pi/Desktop/image1.jpg'
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
greenLED = LED(20)
redLED = LED(21)
buzzer = Buzzer(5)
button = Button(26, pull_up=False)
lcd = LCD()

ser = serial.Serial("/dev/ttyUSB0",9600)
ser.flush()
ser.baudrate = 9600
human = 0

# Set the filename and bucket name
BUCKET = 'sp-p1828120-s3-bucket' # replace with your own unique bucket name
location = {'LocationConstraint': 'us-east-1'}
file_path = "/home/pi/Desktop"
file_name = "image1.jpg"


def check_fever(temp):

	fever_temp = 37.6
	temperature = temp
	if temperature < fever_temp:
		publish(temp)
	else:
		## do the necessary bipping and lights
		print("lights on")

def publish(temp):
	print(type(temp))
	temp = float(temp)
	print(type(temp))

	message = {}  
	now = datetime.datetime.now()
	message["deviceid"] = "deviceid_weijing"
	message["datetimeid"] = now.isoformat() 
	message["value"] = temp
	my_rpi.publish("sensors/temp", json.dumps(message), 1)
	print("publishing temp")

def upload_to_s3(file_path,file_name,bucket_name,location):
	s3 = boto3.resource('s3') # Create an S3 resource
	exists = True
	
	try:
		s3.meta.client.head_bucket(Bucket=bucket_name)
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])
        	if error_code == 404:
			exists = False

	if exists == False:
		s3.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)

	#upload the file
	full_path = file_path + "/" + file_name
	s3.Object(bucket_name, file_name).put(Body=open(full_path,'rb'))
	print("File upload")


def motion_detection():
	print("detecting motion")
	pir.wait_for_motion()
	print("motion detected")
	#sleep(5)
	return 1

def take_picture():
	camera.capture(full_path)
	print("Photo taken")

def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']

def subcribe():
	print("getting from cloud")
	my_rpi.subscribe("sensors/temp", 1, customCallback)
	
def resetCounter():
	global human
	human = 0

def get_temperature():
	#global human
	temperature = 0
	ser.write(b'TakeTemperature\n')
	sleep(2)
	if ser.in_waiting > 0:
		temperature = ser.readline().rstrip()
		print(type(temperature))
		# if temperature >= str(28):
		# 	print ("You have fever")
		# 	print("Temperature: " + temperature)
		# 	lcd.text('You have fever', 1)
		# 	lcd.text('Temp: '+temperature, 2)
		# 	#ser.write(b"Turn on the water pump for 5 seconds!\n")
		# 	redLED.on()
		# 	buzzer.on()
		# 	sleep(2)
		# 	redLED.off()
		# 	buzzer.off()
		# if temperature < str(28):
		# 	print("Temperature: " + temperature)
		# 	lcd.text('You are ok', 1)
		# 	lcd.text('Temp: '+temperature, 2)
		# 	greenLED.on()
		# 	sleep(2)
		# 	greenLED.off()
		#human += 1
		#print("Number of guests: " + str(human))
		# if human == 8:
		# 	print ("Maximum number of guests allowed is 8.")
		# 	lcd.text('Full house', 1)
		# 	lcd.text('Button to rst.', 2)
		# 	buzzer.on()
		# 	sleep(10)
		# 	buzzer.off()
		# 	while True:
		# 		button.when_pressed = resetCounter
		# 		if human == 0:
		# 			break
		return temperature

def motion_detect2():
	print("detecting hand motion")
	pir2.wait_for_motion()
	print("hand motion detected")
	#sleep(5)
	return 1

def dispense():
	ser.write(b"Turn on the water pump for 5 seconds!\n")

def main():
	global human

	## keeping running 


	if motion_detection() == 1:
		
		highestconfidence = 0
		best_bet_item = "Unknown"

		take_picture()
		upload_to_s3(file_path,file_name, BUCKET,location)

		#image recogn
		for label in detect_labels(BUCKET, file_name):
			if label["Confidence"] >= highestconfidence:
				highestconfidence = label["Confidence"]
				best_bet_item = label["Name"]
		if best_bet_item =="Human" or best_bet_item =="Person":
			print(best_bet_item)
			if highestconfidence > 90:
				print("This is human, take his temp")
			else:
				return
		else:
			return

		#run temp fucntion, return temp
		#temp = get_temperature()
		while True:
				temperature = get_temperature()
				if (temperature is None) or (temperature < str(30) or temperature > str(45)):
					print("get temp agn")
				else:
					if temperature >= str(37.6):
						print ("You have fever")
						print("Temperature: " + temperature)
						lcd.text('You have fever', 1)
						lcd.text('Temp: '+temperature, 2)
						#ser.write(b"Turn on the water pump for 1 second!\n")
						redLED.on()
						buzzer.on()
						sleep(2)
						redLED.off()
						buzzer.off()
						human += 1
					if temperature < str(37.6):
						print("Temperature: " + temperature)
						lcd.text('You are ok', 1)
						lcd.text('Temp: '+temperature, 2)
						greenLED.on()
						sleep(2)
						greenLED.off()
					print("Number of guests: " + str(human))
					if human == 8:
						print ("Maximum number of guests allowed is 8.")
						lcd.text('Full house', 1)
						lcd.text('Button to rst.', 2)
						buzzer.on()
						sleep(10)
						buzzer.off()
						while True:
							button.when_pressed = resetCounter
							if human == 0:
								break
					break
				
		publish(temperature)

		if motion_detect2()  == 1:
				dispense()
				lcd.text('Sanitise your', 1)
				lcd.text('hand', 2)

		##return temp from cloud 
		##subcribe()

		##check temp here


while True:
	ser.flush()
	print("running main ")
	main()
	sleep(10)