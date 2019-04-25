#define buzz 9
int mic = 3;

int x = 0;
int dataArray[500];
boolean running = true;

boolean playSound = true;

void setup() {
  Serial.begin(9600);
  pinMode(buzz, OUTPUT);
  pinMode(mic, INPUT);
  
}

void loop() {
  if(playSound){
    if (running){
      buzzSound();
      running = false;
      Serial.println("Started");
    }
    if (!running){
      saveRecording();
    } 
  }
  else if (!playSound){
    // calculate distance here
  }
}

void buzzSound(){
    tone(buzz, 1000);
    delay(10);
    noTone(buzz);
}

void saveRecording(){
    dataArray[x] = analogRead(A0); // sample & save
    Serial.println(dataArray[x]);
    x=x+1; // set up for next location
      if (x==500){
        running = true;
        playSound = false;
        Serial.println("Done");
      }
}
