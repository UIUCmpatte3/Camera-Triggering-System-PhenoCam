#include "MAX44009.h" //defined within this folder

MAX44009 Lux(0x4A);

void setup() {
  Serial.begin(9600);
  
  PrintInitialStatment(); //Just printing initial statment to show Serial is working (and inspire of course)
  
  Lux.Begin(0, 18800); //Begin with full range min and max values
}

void loop() {
  Serial.print("Brightness = ");
  Serial.print(Lux.GetLux());
  Serial.print(" Lux \t");

  Serial.print("Power = ");
  Serial.print(Lux.GetWpm());
  Serial.print(" W/m^2\n\n");
  
  delay(500);

}

/////Ignore, Just pretty string printing
void PrintString(String Val) {
  for(int i = 0; i < Val.length(); i++) {
      Serial.print(Val[i]);
      delay(75);
    }
}

void PrintInitialStatment(void) {
    String Ent = "Is this thing on?\n\n";
    String Think = "Booting...\n";
    String Data = "\nLooking For Da Lite\n\n";
    
    PrintString(Ent);
    for(int x = 0; x < 5; x++) {
      PrintString(Think);
    }
    PrintString(Data);
}
