#include "Adafruit_seesaw.h"
Adafruit_seesaw ss; // Declare the Adafruit seesaw module

void setup()
{
  Serial.begin(115200); Serial.println();
  Serial.println("OK"); // let the python code know we are ready
  beginSeesaw();
  emptySerial();
}

void loop()
{
  // echo back in uppercase what we received
  if (Serial.available() > 0)
  {
    Serial.println(Serial.read());
    sendSensorData();
    emptySerial();
  }
}

void beginSeesaw()
{
  if (!ss.begin(0x36))
  { // Begin seesaw module
    // Serial.write("ERROR! seesaw not found");
    while(1) delay(1);
  }
  else
  {
    // Serial.print("seesaw started! version: ");
    // Serial.println(ss.getVersion(), HEX);
  }
}

void sendSensorData()
{
  float tempC = ss.getTemp();
  uint16_t capread = ss.touchRead(0);

  Serial.print("Temperature:"); Serial.println(tempC);
  Serial.print("Capacitive:");  Serial.println(capread);
}

void emptySerial()
{
  while (Serial.available() > 0) Serial.read();
}