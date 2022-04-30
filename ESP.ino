#include <ESP8266WiFi.h>
#include <Wire.h>
#include <MAX44009.h>

#define LUX 0x4A
#define MC 0x4

MAX44009 light;

//const char* ssid     = "GP25763318";
//const char* password = "2vT-bPS-TzK";

const char* ssid     = "GalaxyA71";
const char* password = "445testing";

int l;
int w;

WiFiServer server(80);

void setup() {
  Wire.begin(2,0);
  
  Serial.begin(115200);
  delay(500);

  if(light.begin())
  {
      Serial.println("Could not find a valid MAX44009 sensor, check wiring!");
      while(1);
  }
  
  // Connecting to WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Starting the web server
  server.begin();
  Serial.println("Web server running. Waiting for the ESP IP...");
  delay(5000);
  
  // Printing the ESP IP address
  Serial.println(WiFi.localIP());
}

void loop() { 
  WiFiClient client = server.available();
  
//  Wire.requestFrom(MC,1);
//  while(Wire.available())
//  {
//    int w = Wire.read();
//  }
//  delay(500);
  
  Wire.requestFrom(LUX,1);
  l = light.get_lux();
  delay(500);
  
  if (client) {
    Serial.println("New client");
    boolean blank_line = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        
        if (c == '\n' && blank_line) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-Type: text/html");
            client.println("Connection: close");
            client.println();
            // your actual web page that displays temperature and humidity
            client.println("<!DOCTYPE HTML>");
            client.println("<html>");
            client.println("<head></head><body><h1>PhenoCam</h1><h3>Wind Speed: ");
            Wire.requestFrom(MC,1);
            while(Wire.available())
            {
              int w = Wire.read();
              client.println(w);
            }
            client.println("MPH</h3><h3>Light Intensity: ");
            client.println(l);
            client.println("Lux"); 
            break;
        }
        if (c == '\n') {
          blank_line = true;
        }
        else if (c != '\r') {
          blank_line = false;
        }
      }
    }  
    // closing the client connection
    delay(1);
    client.stop();
    Serial.println("Client disconnected.");
  }
  }
