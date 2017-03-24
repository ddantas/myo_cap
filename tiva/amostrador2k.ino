void setup()
{
  Serial.begin(115200);
  delay(1000); 
}

int x;

void loop()
{
  x = analogRead(A1); // lê dado
  Serial.println(x); //imprime dado na porta serial
  delayMicroseconds(500); //aguarda 0.0005 segundos até a próxima leitura, gerando uma taxa de amostragem de 2 KHz
}
