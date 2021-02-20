#include <Wire.h>
#include <Adafruit_MLX90614.h>
#define MLX90614_I2CADDR 0x0E
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
int pump = 8;
void setup() {
  Serial.begin(9600);
  pinMode(pump, OUTPUT); 
  mlx.begin();  
}
void loop() {

  if (Serial.available() > 0) {
    String dataFromPi = Serial.readStringUntil('\n');
    if (dataFromPi == "Turn on the water pump for 1 second!") {
        digitalWrite(pump, HIGH);
        delay(1000);  //run pump for 5 seconds;
        digitalWrite(pump, LOW);
        Serial.println("pump off");
    }
    if (dataFromPi == "TakeTemperature") {
        Serial.println(mlx.readObjectTempC());
    }
  }
}
