#include <arduinoFFT.h>

arduinoFFT FFT;

const uint16_t SAMPLES = 64;
const double SAMPLING_FREQUENCY = 1000;

double vReal[Samples];
double vImage[SAMPLES];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i < SAMPLES; i++) {
    vReal[i] = analogRead(A0);
    vImag[i] = 0;
    delayMicroseconds(1000);
  }

  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

  for (int i = 1; i < (SAMPLES / 2); i++) {
    Serial.print((i * SAMPLING_FREQUENCY) / SAMPLES);
    Serial.print(" Hz: ");
    Serial.println(vReal[i]);
  }

  delay(1000);
}
