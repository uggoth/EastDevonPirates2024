//  HandshakeTestA

const int HANDSHAKE_PIN = 12;

void setup() {
  pinMode(HANDSHAKE_PIN, OUTPUT);
}

void loop() {
  digitalWrite(HANDSHAKE_PIN, HIGH);
  delay(500); 
  digitalWrite(HANDSHAKE_PIN, LOW);
  delay(2000); 
}
