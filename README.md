# CNY-Temperature-Scanner

## Introduction
Our target audience is home owners who are expecting visitors over the Chinese New Year. 
Our application takes the temperature of people visiting the house for Chinese New Year. 
Our solution also take into consideration about the rules set by the government that there is a limit of 8 people for house visiting to prevent the spread of CoVid-19. [ Link to Rules ](https://www.straitstimes.com/singapore/visitors-per-household-to-be-capped-at-8-per-day-from-jan-26-limit-cny-visits-to-2-other)

We also made a video showcasing our project [Link to video](https://youtu.be/FMSO4x-2tsA)

## How it works


## System Infrastructure
![System](https://user-images.githubusercontent.com/56866622/108586416-5e9d1a00-7389-11eb-9c79-5c1deca7ce27.jpg)

Uses total of 5 Amazon Web Services (AWS) <br />

1. IoT Core <br /> To connect to RaspberryPi 
2. AWS Elastic Compute Cloud (EC2) <br /> To host web application on cloud server 
3. DynamoDB  <br /> To store data on cloud database 
4. AWS S3 <br /> To store image taken to S3 
5. AWS Rekognition  <br /> Use the image stored on S3 for recognition 

### Flow

1. Starts with Raspberry Pi that runs "temp.py" which takes a photo if motion is detected
2. Upload the photo to AWS S3
3. Image stored on AWS will be used by Amazon Rekognition to determine if human
4. If human is detected, the Infrared Thermometer will take temperature of the person 
5. Arduino will run "temp.ino" and return values from Infrared Thermometer to RaspberryPi
6. Upon receiving the value from Arduino, Raspberry Pi will publish the temperature to "/sensors/temp" topic via MQTT to AWS
7. A rule is created to store the value in a table in DynamoDB
8. Flask webserver hosted on AWS EC2 will obtain values from DynamoDB and display it on the webserver as a graph and a table
9. On the Flask Webserver run on EC2, it is able to remotely control the state of red LED, green LED and the Buzzer.
10. Flask server on EC2 will publish multiple topics, "/sensors/led/red", "/sensors/led/green" and "/sensors/buzzer"
11. "listening_topic.py" will be running on the Raspberry Pi to listen to these topics to control red LED, green LED and the Buzzer.




## Hardware Setup

### List of Hardware needed
1. RaspberryPi x1 <br />
![raspberrypi](https://user-images.githubusercontent.com/56866622/108586730-40d0b480-738b-11eb-80b9-5dc7a5f386cd.jpg) 
2. Arduino x1 <br /> ![arduino](https://user-images.githubusercontent.com/56866622/108586732-429a7800-738b-11eb-829b-7d4bc5202b8b.jpg)
3. MLX90614 Infrared Thermometer x1 <br /> ![tempscanner](https://user-images.githubusercontent.com/56866622/108586756-63fb6400-738b-11eb-84e9-bbd50bc3db30.jpg)
4. Motion Sensor x2 <br /> ![motionsensor](https://user-images.githubusercontent.com/56866622/108586763-6958ae80-738b-11eb-8b8e-66d121059a1c.jpg)
5. LCD 16x2 i2c x1  <br /> ![lcd](https://user-images.githubusercontent.com/56866622/108586766-6d84cc00-738b-11eb-9a2b-c60a73962a2f.jpg)
6. 5V Submersible Water Pump x1 <br /> ![waterpump](https://user-images.githubusercontent.com/56866622/108587060-83df5780-738c-11eb-94dc-180a5f356b93.jpg)
7. 5V 4 Channel Relay x1 <br /> ![Relay](https://user-images.githubusercontent.com/56866622/108587065-8641b180-738c-11eb-809f-c3de8c6066f1.jpg)
8. 5V USB Cable x1 (power supply) <br /> ![usbcable](https://user-images.githubusercontent.com/56866622/108587071-893ca200-738c-11eb-876d-f171c067c7c8.jpg)
9. Red LED x1 <br /> ![redled](https://user-images.githubusercontent.com/56866622/108587075-8c379280-738c-11eb-86ac-3b8141f684aa.png)
10.  Green LED x1 <br /> ![greenled](https://user-images.githubusercontent.com/56866622/108587079-8e99ec80-738c-11eb-8d96-5c596dffd74b.png)
11.  Buzzer x1 <br /> ![buzzer](https://user-images.githubusercontent.com/56866622/108587086-978abe00-738c-11eb-8f71-82e3f337d2f7.jpg)
12.  Silicone Tubing x1 (1 meter) <br /> ![tubing](https://user-images.githubusercontent.com/56866622/108587088-99ed1800-738c-11eb-85d2-55fd308e5d0d.jpg)
13.  Button x1 <br /> ![button](https://user-images.githubusercontent.com/56866622/108587091-9d809f00-738c-11eb-94a2-cbe7590e6fa5.jpg)
14.  Jumper Wires <br /> ![wires](https://user-images.githubusercontent.com/56866622/108587158-0b2ccb00-738d-11eb-9ad3-69d1e8fca9d0.jpg)


### Our Setup
![hardware](https://user-images.githubusercontent.com/56866622/108586368-e8001c80-7388-11eb-8f44-d33ee8e74a10.jpg)
### Fritzing Diagram
![fritzing](https://user-images.githubusercontent.com/56866622/108586438-8d1af500-7389-11eb-9b25-de4f22e43324.jpg)
### Arduino and Relay Setup 
1. Connect the arduino to Raspberry Pi via a USB cable as shown below <br /> ![ardusb](https://user-images.githubusercontent.com/56866622/108587818-e4709380-7390-11eb-954e-3a1ffd4edcf7.jpg)
2. Check the USB cable, that is to be used as power supply to the water pump, with a voltmeter and ensure that it outputs 5V as the submersible water pump requires 5V in order to be powered.  <br /> ![Picture18](https://user-images.githubusercontent.com/56866622/108587819-e5a1c080-7390-11eb-98ba-9ea36d4df21f.jpg)
3. Connect the red wire of the USB cable to COM1 on the relay (center). 
4. Connect the blue wire (ground wire) of the USB cable with the black wire of the water pump by twisting them together. You can tape them with an electrical tape for a stronger connection. 
5. Connect the red wire of the water pump to the NC on the relay (most right). <br />
![Picture19](https://user-images.githubusercontent.com/56866622/108587820-e5a1c080-7390-11eb-9a8c-a397c11d8f89.jpg)





## Software Setup
## Amazon Web Services Setup

