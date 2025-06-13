#include <arduinoFFT.h>

const uint16_t SAMPLES = 128;
const double SAMPLING_FREQUENCY = 960;

double vReal[SAMPLES];
double vImag[SAMPLES];

ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, SAMPLES, SAMPLING_FREQUENCY);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i < SAMPLES; i++) {
    vReal[i] = analogRead(A0);
    vImag[i] = 0;
    delayMicroseconds(1000);
  }

  FFT.windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.compute(vReal, vImag, SAMPLES, FFT_FORWARD);
  FFT.complexToMagnitude(vReal, vImag, SAMPLES);

  for (int i = 1; i < (SAMPLES / 2); i++) {
    Serial.print((i * SAMPLING_FREQUENCY) / SAMPLES);
    Serial.print(" ");
    Serial.println(vReal[i]);
  }

  delay(1000);
}
