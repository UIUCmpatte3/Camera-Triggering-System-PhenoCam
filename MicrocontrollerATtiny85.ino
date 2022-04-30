#define analogPinForRV    A2   // change to pins you the analog pins are using
#define analogPinForTMP   A3

#define I2C_SLAVE_ADDRESS 0x4 // Address of the slave, set by user
 
#include <TinyWireS.h> //library needed

const float zeroWindAdjustment =  .2; // negative numbers yield smaller wind speeds and vice versa, adjust if necessary to reach 0mph at characterization

int TMP_Therm_ADunits;  //temp termistor value from wind sensor
float RV_Wind_ADunits;    //RV output from wind sensor 
float RV_Wind_Volts;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;

void setup() {

  TinyWireS.begin(I2C_SLAVE_ADDRESS); // join i2c network
  TinyWireS.onRequest(requestEvent);

}

void loop() { //loop for probing the wind sensor; code based on wind sensor GitHub repos found online
  
  TMP_Therm_ADunits = analogRead(analogPinForTMP);
  RV_Wind_ADunits = analogRead(analogPinForRV);
  RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125);
  
  zeroWind_ADunits = -0.0006*((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172;
  
  zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;  
  WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) /.2300) , 2.7265);

  TinyWireS_stop_check();

}

void requestEvent() //event to request the data as an integer wind speed
{

  TinyWireS.send((int)WindSpeed_MPH);

}
