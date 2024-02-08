void setup() {
  // Start serial communication at 9600 baud
  Serial.begin(115200);

 

  // Set ADC prescaler to the maximum value (128)
  // This sets the ADC clock frequency to the system clock divided by 128
  // This provides the fastest ADC conversion rate, but may sacrifice accuracy
  ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescaler to 128
}

void loop() {
  // Read analog input from pin A0
  byte sensorValue = analogRead(A0) >>1;

  // Send the sensor value over serial
  Serial.write(sensorValue); // 8-bit value directly

  // Delay for a short interval before reading again
  //delay(10); // Adjust as needed for your application
}
