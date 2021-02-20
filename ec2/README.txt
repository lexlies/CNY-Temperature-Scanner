Do take note that you must have the following files in this directory to be able to run the 
web application.

AmazonRootCA1.pem
certificate.pem.crt
private.pem.key
public.pem.key

Description of Files
--------------------------

static (contain resources like images for index.html)

templates (contain index.hmtl) 
---------------------------
index.html is affiliated with server.py. It outputs the values and data and enable the owner to control and view them.  


server.py
--------------------------
server.py is a web server hosted on AWS EC2 where the owner of the house can monitor the real-time status of the temperature 
reading of the visitors. He can control both LEDs and the  Buzzer via the web server interface. Historical temperature values 
are displayed as a graph that shows the last 10 recorded values and in a tabular format too.


dynamodb.py
--------------------------
dynamodb.py gets the last 10 values stored in DynamoDB as well as the last value stored in DynamoDB


jsonconverter.py 
---------------------------
jsonconverter.py is used to convert data received from DynamoDB to JSON format.





