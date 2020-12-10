#define nLeds 7 // Define quantity of LEDs (only when final layout is defined)
#define combinations 21 // Combinations of n 2 by 2 (change when numleds is correctly defined)
int m[nLeds];
int b[nLeds];
int coords[2];
//int ledpins[] = {}; // Define all LED pins

void setup() {
  /*
  for (int led = 0; led < numleds; led++){
    pinMode(led, INPUT_PULLUP);
  }
  */
  Serial.begin(9600);
}

void loop() {

  // Line definition
  DefineLine();
  
  // All line intersection
  LineIntersection();

}

int DefineLine() {
    int coordled[nLeds][2];
    int coordshadow[nLeds][2];
    
    for (int i = 0; i < nLeds; i++){
      coordled[i][0] = random(-1000,1000);
      coordled[i][1] = 0;
      coordshadow[i][0] = random(-1000,1000);
      coordshadow[i][1] = 1000;

      m[i] = (coordshadow[i][1] - coordled[i][1]) / (coordshadow[i][0] - coordled[i][0]);
      b[i] = coordled[i][1] - m[i]*coordled[i][0];
    }
}

int LineIntersection() {
    int coordX[nLeds-1][nLeds];
    int coordY[nLeds-1][nLeds];
    int CoordX = 0;
    int CoordY = 0;

    for(int i = 0; i < nLeds; i++){       // n
      for(int j = i+1; j < nLeds; j++){   // n-i-1
        coordX[i][j] = (b[j] - b[i]) / (m[i] - m[j]);
        coordY[i][j] = ((m[i]*coordX[i][j] + b[i]) + ((m[j]*coordX[i][j]) + b[j])) / 2;

        CoordX += coordX[i][j];
        CoordY += coordY[i][j];
      }
    }

    // x and y coordinates of the average of all line intersections
    coords[0] = CoordX/combinations;
    coords[1] = CoordY/combinations;

    return coords;
}
