int n = 7; // Define quantity of LEDs n (only when final layout is defined)
int ledpins[] = {}; // Define all LED pins

void setup() {
  for (int led = 0; led < n; led++){
    pinMode(led, INPUT_PULLUP);
  }
  Serial.begin(9600);
}

void loop() {

  // Line definition
  DefineLine();

  // Combinations of all possible intersections
  
  
  // All line intersection
  LineIntersection();
  
  // x and y coordinates of the average of all line intersections
  float coords[]
  
  coords[0] = (accumulate(begin(coordX),end(coordX),0,plus<int>()))/comb();
  coords[1] = (accumulate(begin(coordY),end(coordY),0,plus<int>()))/comb();
}

int DefineLine() {
    float coordled[][];
    float coordshadow[][];
    float m[];
    float b[];
    
    for (int i = 0; i < n; i++) {
      // Verify if LED is on and calculate line of LED and shade coordinates if so
      if(!digitalRead(ledpins[i])){
        coordled[i][0] = random(-1000,1000);
        coordled[i][1] = 0;
        coordshadow[i][0] = random(-1000,1000);
        coordshadow[i][1] = 1000;

        m[i] = (coordshadow[i][1] - coordled[i][1]) / (coordshadow[i][0] - coordled[i][0]);
        b[i] = coordled[i][1] - m[i]*coordled[i][0];
      }
    }
    return m;
    return b;
}

int LineIntersection() {
    float coordX[];
    float coordY[];

    for (int i = 0; i < comb(); i++){
      coordX[i] = (comb_b[i][1] - comb_b[i][0]) / (comb_m[i][0] - comb_m[i][1]);
      coordY[i] = ((comb_m[i][0]*coordX[i] + comb_b[i][0]) + ((comb_m[i][1]*coordX[i]) + comb_b[i][1])) / 2;
    }
    
    return coordX;
    return coordY;
}
