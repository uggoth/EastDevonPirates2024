/*
  Command protocol test A
*/

const String MY_NAME = "JOLLY";
const int handshake_pin = 12;
int x;
bool finished = false;
String message_in = "";
String serial_no_in = "";
String command_in = "";
String data_in = "";
const int signal_led = 33;
const int flashlight_led = 4;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(handshake_pin, OUTPUT);   // handshake is on digital pin 2
  pinMode(signal_led, OUTPUT);
  pinMode(flashlight_led, OUTPUT);
}

void loop() {
  if (finished) {
    digitalWrite(handshake_pin, LOW);
  } else {
    digitalWrite(handshake_pin, HIGH);
    if(Serial.available() > 0)
    {
      digitalWrite(handshake_pin, LOW);
      message_in = Serial.readStringUntil('\n');
      if (message_in.length() < 8) {
        Serial.println("BADM");
      }
      serial_no_in = message_in.substring(0,4);
      command_in = message_in.substring(4,8);
      if (command_in == "WHOU") {
        Serial.println(serial_no_in + "OKOK" + MY_NAME);
      } else if (command_in == "WAIT") {
        if (message_in.length() < 12) {
          Serial.println(serial_no_in + "BADC" + " Wait duration missing");  
        } else {
          data_in = message_in.substring(8,12);
          x = data_in.toInt();  //  IN MILLISECONDS
          Serial.println(serial_no_in + "OKOK" + " Waiting");
          delay(x);
        }
      } else if (command_in == "EXIT") {
        Serial.println(serial_no_in + "OKOK" + " Exiting");
        finished = true;
      // NOTE1: The signal and flashlight LEDs work with opposite polarity
      // NOTE2: The signal LED is on the back of ESP32 board, hidden by the MB board
      } else if (command_in == "SIG+") {
        Serial.println(serial_no_in + "OKOK" + " Signal LED ON");
        digitalWrite(signal_led, LOW);
      } else if (command_in == "SIG-") {
        Serial.println(serial_no_in + "OKOK" + " Signal LED OFF");
        digitalWrite(signal_led, HIGH);
      } else if (command_in == "FLA+") {
        Serial.println(serial_no_in + "OKOK" + " Flashlight LED ON");
        digitalWrite(flashlight_led, HIGH);
      } else if (command_in == "FLA-") {
        Serial.println(serial_no_in + "OKOK" + " Flashlight LED OFF");
        digitalWrite(flashlight_led, LOW);
      } else {
        Serial.println(serial_no_in + "BADC " + message_in);
      }
    }
  }
}
