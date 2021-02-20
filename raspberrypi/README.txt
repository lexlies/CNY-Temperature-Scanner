Description of files
------------------------------

listening_topic.py 
------------------ 
listening_topic.py subscribes to 3 topics – sensors/led/green, sensors/led/red and sensors/buzzer 
which was published by the EC2 web server and controls the state of the LED remotely when the user 
turns on or off the actuators via the web application on the cloud.


temp.py
-------------------
temp.py is the main function of the program where it detects for motion (using motion sensor), 
specfically a human moving towards the temperature sensor and captures the temperature of the object only if 
it is recognised as a human (using AWS Rekognition that analyses the photo uploaded to Amazon S3 that was captured
 using the PiCam when a motion is detected). The temperature value will be passed from the Arduino to the Raspberry Pi 
where it checks whether the temperature is higher or lower than 37.6 degree celcius. A temperature value higher than 
37.6 indicates that the visitor has a fever and should not be allowed to enter the house. The red LED lights up and 
the buzzer sounds to alert the owner of the house. Otherwise, a normal and healthy person whose temperature is lower 
than 37.6 will light up the green LED that gives him the green light to enter the house. All visitors MUST sanitise their 
hand via the sanitiser pump once they have their temperature taken. This is done via motion detection. Should there be hand 
movement of the visitor directly under the sanitiser pump, the hand sanitiser will be pumped out to the hands of the visitor. 
Due to Covid-19, Singapore allows only up to 8 visitors per house unit. In line with the Covid-19 restrictions, our program is 
designed to stop taking temperature after the 8th visitor. The LCD outputs “Full house. Button to rst” to refrain any more visitors 
from coming in and the buzzer beeps to notify the owner of the house. The owner has to press the red button to reset the counter back to 0. 


temp.ino
-------------------
temp.ino is a software program created with Arduino that interfaces with the Raspberry Pi and controls the sanitiser pump 
when it receives command from the Raspberry Pi.