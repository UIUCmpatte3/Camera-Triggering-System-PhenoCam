//Code for the Arduino Mega<
#include <Wire.h>
 
void setup()
{
 Wire.begin(); // join i2c bus (address optional for master)
 Serial.begin(115200); // start serial for output
}
 
void loop()
{
 Wire.requestFrom(4, 1); // request 1 byte from slave device address 4
 
while(Wire.available()) // slave may send less than requested
 {
 int x = Wire.read(); // receive a byte as character
 Serial.println(x); // print the character
 }
 
delay(200);
}
