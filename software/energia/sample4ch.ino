// Sample 4 analog channels with 1/period_us sample rate and sends a package with the data via serial communication
 
int analog_pin[4] = {26, 27, 28, 29}; // analog pin id
int resolution = 12; //ADC resolution
int baudrate = 115200; // baud rate for serial communication
int period_us = 3000; // period for sample rate
int data[4]; // analog pin data
String package; // package for serial communication

void setup()
{
  // configuring input pins
  pinMode(analog_pin[0], INPUT);
  pinMode(analog_pin[1], INPUT);
  pinMode(analog_pin[2], INPUT);
  pinMode(analog_pin[3], INPUT);

  // configuring ADC
  analogReadResolution(resolution);

  // configuring serial communication
  Serial.begin(baudrate);
}

void loop()
{
  // sampling data from analog pins
  data[0] = analogRead(analog_pin[0]);
  data[1] = analogRead(analog_pin[1]);
  data[2] = analogRead(analog_pin[2]);
  data[3] = analogRead(analog_pin[3]);
  
  // building the package that will be send
  package = String(data[0], DEC) + " " + String(data[1], DEC) + " " + String(data[2], DEC) + " " + String(data[3], DEC);
  
  // send the package via serial communication
  Serial.println(package); 

  // generating sample rate of 1/period_us
  delayMicroseconds(period_us);
}
