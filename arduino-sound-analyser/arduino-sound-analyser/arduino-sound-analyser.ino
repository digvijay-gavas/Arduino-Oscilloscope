#include <LiquidCrystal.h>
#include "arduinoFFT.h"

arduinoFFT FFT;

#define CHANNEL A0
const uint16_t samples = 128; 

double vReal[samples];
double vImag[samples];

const int rs = 9, en = 10, d4 = 4, d5 = 5, d6 = 6, d7 = 7;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

String padString(String str, int width) {
  int padding = width - str.length();

  // If padding is needed
  if (padding > 0) {
    // Add leading spaces
    for (int i = 0; i < padding; i++) {
      str = " " + str;
    }
  }
  return str;
}

void setup()
{
  ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescaler to 128
  analogReference(INTERNAL);
  Serial.begin(115200);
  while(!Serial);
  lcd.begin(16, 2);
  byte b=B100000;
  for (int i = 0; i < 6; i++) {
    b |= 1 <<(5-i);
    byte ba[]={ b, b, b, b, b, b, b, b };
    lcd.createChar(i,ba );
  }
  lcd.print("   <<<<-->>>>");
  lcd.setCursor(0, 1);
  lcd.print("    \\\-->///");
}

long lastNativeFFTMillis=millis();
long lastRemoteFFTMillis=millis();
void loop()
{
  if( (millis() -lastNativeFFTMillis ) > 500)
  {
    unsigned long timeStart = micros();
    for(int i=0; i<samples; i++)
    {
        vReal[i] = analogRead(CHANNEL);
        vImag[i] = 0;
    }
    float samplingFrequency = 1000000.0 / ((micros() - timeStart) /(float)samples);

    FFT = arduinoFFT(vReal, vImag, samples, samplingFrequency);

    double x = FFT.MajorPeak();
    //Serial.println(padString(String((int)x),4)+" Hz/"+padString(String((int)samplingFrequency),4)+" Hz"); 
    lcd.setCursor(0, 0);
    lcd.print(padString(String((int)x),4)+" Hz/"+padString(String((int)samplingFrequency),4)+" Hz");
    lcd.setCursor(0, 1);
    printSlider(map(x, 0, samplingFrequency, 0, 96));

    lastNativeFFTMillis=millis();
  }

  if( (millis() -lastRemoteFFTMillis ) > 5)
  {

    if (Serial.available() > 1) {
      while(Serial.available() > 1)
        byte command = Serial.read();

      int rSampleSize=512;
      byte rSamples[rSampleSize];
      unsigned long timeStart = micros();
      for(int i=0; i<rSampleSize; i++)
      {
          rSamples[i]= analogRead(CHANNEL)/4;
      }
      unsigned long rSampleMicros=micros() - timeStart;

      for(int i=0; i<rSampleSize; i++)
      {
          Serial.write(rSamples[i]);
      }
      Serial.println(rSampleMicros);
    }

    lastRemoteFFTMillis=millis();
  }
  
}


void printSlider(int position) {
  lcd.setCursor(0, 1);
  for(int i=0;i<position/6;i++)
  {
    lcd.write(5);
  }
  lcd.write(position%6);
  for (int i = 1; i <= 15 - position/6; i++) {
    lcd.write(' ');
  }
}



