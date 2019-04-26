#include "arduinoFFT.h"
#define SAMPLES 512           //Must be a power of 2
#define SAMPLING_FREQUENCY 8000 //Hz, must be less than 10000 due to ADC
arduinoFFT FFT = arduinoFFT();
double dataArray[SAMPLES];
double imagArray[SAMPLES];
int mic = 2;
unsigned long period = 125;
unsigned long previousMicros;
bool running = false;

void setup() {
  Serial.begin(9600);
  pinMode(mic, INPUT);
  Serial.println("starting");
  // put your setup code here, to run once:
  if (!running) {
    running = true;
    previousMicros = micros();
    Serial.println("done setup");
  }
  // sample on time check  // button check or running
}

void loop() {
  if (running) {
    running = false;
    micRecord();
    printRecording();
    runFFT();
  }
} // end of loop


void micRecord() {
  for (int m = 0; m < SAMPLES; m++) {
    while (((micros() - previousMicros) < period)) {
    }
    previousMicros = previousMicros + period; // set up for next time check
    dataArray[m] = (analogRead(mic) - 512); // sample & save
    imagArray[m] = 0;
  }
}

void printRecording() {
  for (int i = 0; i < 50; i++) { //prints first 500 entries in the array
    for (int k = 0; k < 10; k++) {
      Serial.print(dataArray[(i * 10) + (k)], 0);
      Serial.print(",");
    }
    Serial.println("");
  }
  Serial.println("Done");
}

void runFFT() {
  /*FFT*/
  FFT.Windowing(dataArray, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(dataArray, imagArray, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(dataArray, imagArray, SAMPLES);
  double peak = FFT.MajorPeak(dataArray, SAMPLES, SAMPLING_FREQUENCY);

  /*PRINT RESULTS*/
  Serial.println("Freq : Amp");
  for (int i = 0; i < (SAMPLES / 2); i++)
  {
    /*View all these three lines in serial terminal to see which frequencies has which amplitudes*/
    //Serial.print((i * 1.0 * SAMPLING_FREQUENCY) / SAMPLES, 1);
    //Serial.print(" ");
    Serial.println(dataArray[i], 1);    //View only this line in serial plotter to visualize the bins
  }
  Serial.println("peak frequency: ");
  Serial.println(peak);     //Print out what frequency is the most dominant.
}
