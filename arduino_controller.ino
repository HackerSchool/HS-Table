#define nLeds 7 // Define quantity of LEDs (only when final layout is defined)
#define combinations 21 // Combinations of n 2 by 2 (change when numleds is correctly defined)
int m[nLeds];
int b[nLeds];
//int ledpins[] = {}; // Define all LED pins

int left = 7;
int up = 6;
int right = 5;
int down = 4;
unsigned int coords[] = {0,0};
int changed = 0;

void setup() {
  /*
  for (int led = 0; led < numleds; led++){
    pinMode(led, INPUT_PULLUP);
  }
  */
  Serial.begin(9600);
}

int DefineLine() {
    int coordled[nLeds][2];
    int coordshadow[nLeds][2];

    for (int i = 0; i < nLeds; i++) {
      for (int i = 0; i < nLeds; i++){
        coordled[i][0] = random(-1000,1000);
        coordled[i][1] = 0;
        coordshadow[i][0] = random(-1000,1000);
        coordshadow[i][1] = 1000;
        m[i] = (coordshadow[i][1] - coordled[i][1]) / (coordshadow[i][0] - coordled[i][0]);
        b[i] = coordled[i][1] - m[i]*coordled[i][0];
      }
    }
}

void LineIntersection() {
    int aux;
    int CoordX = 0;
    int CoordY = 0;

    for(int i = 0; i < nLeds; i++){       // n
      for(int j = i+1; j < nLeds; j++){   // n-i-1
        aux = (b[j] - b[i]) / (m[i] - m[j]);
        CoordY += ((m[i]*aux + b[i]) + ((m[j]*aux) + b[j])) / 2;

        CoordX += aux;
      }
    }

    // x and y coordinates of the average of all line intersections
    coords[0] = CoordX/combinations;
    coords[1] = CoordY/combinations;
}

void loop() {
  // Line definition
  DefineLine();
  
  // All line intersection
  LineIntersection();

  if(changed){
    SendCoords();
    changed = 0;
  }

  delay(100);
}

void SendCoords()
{ // sends the coordinates via serial
  int byte;

  byte = coords[0] % 256;
  Serial.write(byte);
  byte = coords[0] / 256;
  Serial.write(byte);

  byte = coords[1] % 256;
  Serial.write(byte);
  byte = coords[1] / 256;
  Serial.write(byte);

}
