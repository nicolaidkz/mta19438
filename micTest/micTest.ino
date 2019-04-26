#include "arduinoFFT.h"
#define SAMPLES 512           //Must be a power of 2
#define SAMPLING_FREQUENCY 8000 //Hz, must be less than 10000 due to ADC
arduinoFFT FFT = arduinoFFT();
double dataArray[SAMPLES];  //currently the program uses these arrays several times per iteration due to memory limitations
double imagArray[SAMPLES];
int intArray[SAMPLES];
int mic = 2;
unsigned long period = 125;
unsigned long previousMicros;
bool running = true;

void setup() {
  Serial.begin(9600);
  pinMode(mic, INPUT);
  Serial.println("starting");
}

void loop() {
  if (running) {
    running = false;
    micRecord();
    printRecording();
    runFFT();
    removeFrequencies(6, 6);
    inverseFFT2();
    printRecording();
  }
} // end of loop


void micRecord() {  //saves some audio from mic to an array
  previousMicros = micros();
  for (int m = 0; m < SAMPLES; m++) { //get SAMPLES number of samples
    while (((micros() - previousMicros) < period)) {  //waits until the defined time period has passed since last sample was taken
    }
    previousMicros = previousMicros + period; // set up for next time check
    dataArray[m] = (analogRead(mic) - 512); // sample & save, -512 for DC offset
    imagArray[m] = 0; //not sure if necessary
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

void inverseFFT() {
  /*Inverts FFT*/
  FFT.Windowing(dataArray, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(imagArray, dataArray, SAMPLES, FFT_FORWARD);
  //FFT.ComplexToMagnitude(dataArray, imagArray, SAMPLES);
  for (int i = 0; i < SAMPLES; i++) {
    //imagArray[i] = imagArray[i] / 512;
    dataArray[i] = dataArray[i] / 512;
  }
}

/*void inverseFFT2() {
  for (int i = 0 ; i < 512 ; i += 2) {
    intArray[i] = dataArray[i];
    intArray[i + 1] = dataArray [i + 1];
    intArray[i] =  (intArray[i] >> 8);
    intArray[i + 1] = -(intArray[i + 1] >> 8);
    dataArray[i] = intArray[i];
    dataArray [i + 1] = intArray[i + 1];
  }
  FFT.Windowing(dataArray, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(dataArray, imagArray, SAMPLES, FFT_FORWARD);
}*/

void removeFrequencies(int low, int high) { //run this after fourier to remove frequencies below low argument and above high argument (bins for the moment)
  for (int i = 0; i < SAMPLES; i++) {
    if (i < low || i > high) {
      dataArray[i] = 0;
    }
    //Serial.println(dataArray[i]);
  }
}
