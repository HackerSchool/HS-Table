int left = 7;
int up = 6;
int right = 5;
int down = 4;
unsigned int coords[] = {0,0};
int changed = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(left, INPUT_PULLUP);
  pinMode(up, INPUT_PULLUP);
  pinMode(right, INPUT_PULLUP);
  pinMode(down, INPUT_PULLUP);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if(!digitalRead(left)){ 
    coords[0] -= 1;
    changed = 1;
  }
  if(!digitalRead(right)){ 
    coords[0] += 1;
    changed = 1;
  }
  if(!digitalRead(up)){ 
    coords[1] -= 1;
    changed = 1;
  }
  if(!digitalRead(down)){ 
    coords[1] += 1;
    changed = 1;
  }

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
