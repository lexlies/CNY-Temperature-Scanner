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
### Install AWS Python Library On Raspberry Pi
On RaspberryPi, install the following: <br /> _sudo pip install --upgrade --force-reinstall pip==9.0.3_ <br /> _sudo pip install AWSIoTPythonSDK --upgrade --disable-pip-version-check_ <br /> _sudo pip install --upgrade pip_
### Install AWS CLI On Raspberry Pi
On RaspberryPi, run : <br /> _sudo pip install awscli_ <br /> _sudo pip install awscli --upgrade_
### Install Boto
On RaspberryPi, run : <br /> _sudo pip install botocore_ <br /> _sudo pip install botocore --upgrade_ <br />
_sudo pip install boto3 --upgrade_ <br />
### Install Putty
Download [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html)
### Install WinSCP
Downlaod [WinSCP](https://winscp.net/eng/download.php)


## Amazon Web Services Setup
### Getting an Amazon Web Service Account
Get your own Amazon Web Service Account 
[Register Here](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start)
### AWS Credential File
This file is needed to be stored in the Raspberry Pi and EC2 
1. On AWS Account, click "Account Details"
2. Click show button and copy the whole text <br /> ![awscred](https://user-images.githubusercontent.com/56866622/108590357-0cb2bf00-739e-11eb-845d-900073a93db2.jpg)
3. Copy and store it in file "credentials"
4. Create a directory in and store it in ~/.aws/credentials
### Connect Raspberry Pi to AWS
1. Go to "IOT Core" Services > Click "Get Started" <br />
2. Go "Manage" then choose "Things" and then "Register a thing"
3. A thing represents a device whose status or data is stored in the AWS cloud <br /> Your Raspberry Pi will be your "thing"
4. Give your Raspberry Pi a name and Create Certificates for it (Important!)
5. Download all four links and keep it save
6. For root, open it in a new tab and do a right-click, “Save As” when clicking on the link <br /> ![certs](https://user-images.githubusercontent.com/56866622/108588829-39fb6f00-7396-11eb-9595-f5df7124e2bc.JPG)
7. Activate it
### Create Security Policy for RPi
1. On the left IOT Core dashboard, select Policies under the Secure sub-menu
2. On the next page, choose “Create new policy”
3. On the Create a policy page, key in the following configuration, can rename policy name to whatever you want <br /> ![policies](https://user-images.githubusercontent.com/56866622/108588953-e178a180-7396-11eb-9994-fed48ac13a7c.JPG)
4. Then Create
### Attach Security Policy and Thing to your certificate
1. Click Security > Certificates
2. You should see the X.509 certificate you created earlier
3. Click the checkbox beside it, then click “Actions” button and choose “Attach Policy” 
4. Check the policy you created earlier and click “Attach” button.
5. Click “Actions” button and choose “Attach Thing” and attach your RaspberryPi to it.
### Creating a DynamoDB
1. Open Amazon DynamoDB console and "Create Table"
2. Name your table
3. Follow the attributes below <br /> ![atributes](https://user-images.githubusercontent.com/56866622/108589277-a7100400-7398-11eb-9679-635eeb43805b.JPG) 
### Create rule to store MQTT message to DB
1. In the AWS IoT console, in the left navigation pane, choose “Act”, then “Create a rule”
2. Name the rule and add description (optional)
3. For Rule Query statement : <br /> _SELECT * FROM 'sensors/temp'_
4. Set action by choosing "Add action"
5. Configure action and choose "Split Message into multiple columns of a DynamoDB table)
6. It will look like <br /> ![dynamo](https://user-images.githubusercontent.com/56866622/108589481-66fd5100-7399-11eb-8318-784ff5adea8e.JPG)
### Create bucket on S3
1. Go to S3 and create bucket
2. Enter name for bucket
3. Choose "US East 1(North Virginia)" and create
### Creating a new EC2 Instance
1. Go to EC2
2. Make sure server is on US East (N. Virginia)
3. Launch Instance
4. Choose a Amazon Machine Image (AMI) <br /> We choose Amazon Linux 2 AMI 64-bit (x86).
5. For instance type, choose t2.mirco
6. Then click “Next: Configure Instance Details”
7. Enable "Auto-assign Pubic IP"
8. Scroll till "Advanced Details and enter the follwing : <br /> 
_sudo yum check-update_ <br /> 
_sudo yum install -y amazon-linux-extras_ <br /> 
_sudo amazon-linux-extras enable python3.8_ <br /> 
_sudo yum clean metadata_ <br /> 
_sudo yum install python38 -y_ <br /> 
9. Add sufficient storage
10. Add relevant tags <br /> We enter “Name” for the Key and “Python Web Server” as the Value
11. Configure security group <br /> We did it with the following settings <br /> ![secgrp](https://user-images.githubusercontent.com/56866622/108590770-41277a80-73a0-11eb-8596-3ced0c6475f3.JPG)
12. A SSH rule has by default been added for you so that you can SSH into the server later
13. We will add a second rule to allow HTTP traffic as well.
14. Click the “Add Rule” button. 
15. Select “Custom TCP”, enter Port as “8001” and Source as “Anywhere” then "Save rules"
16. Choose "Create a new key pair" and give it a name. <br /> We will use this to SSH into the EC2 server.





  

