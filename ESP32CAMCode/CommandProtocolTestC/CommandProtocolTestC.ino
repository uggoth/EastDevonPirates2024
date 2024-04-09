/*
  CommandProtocolTestC

Connect an LED to pin 13 on the ESP32-CAM
(or if no LED monitor on Raspberry Pi)
Open the serial monitor at 115200 baud
Upload this program
Type commands into the serial monitor
Watch the LED

LED should be on except when actioning a command 
that takes some time (i.e. WAIT)

*/

const String MY_NAME = "ZOMBI";
const int HANDSHAKE_PIN = 13;
int x;
bool finished = false;
String message_in = "";
String serial_no_in = "";
String command_in = "";
String data_in = "";
const int BUILT_IN_LED = 33;
const int FLASHLIGHT_LED = 4;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(HANDSHAKE_PIN, OUTPUT); 
  pinMode(BUILT_IN_LED, OUTPUT);
  pinMode(FLASHLIGHT_LED, OUTPUT);
}

void loop() {
  if (finished) {
    digitalWrite(HANDSHAKE_PIN, LOW);
  } else {
    digitalWrite(HANDSHAKE_PIN, HIGH);
    if(Serial.available() > 0)
    {
      digitalWrite(HANDSHAKE_PIN, LOW);
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
        digitalWrite(BUILT_IN_LED, LOW);
      } else if (command_in == "SIG-") {
        Serial.println(serial_no_in + "OKOK" + " Signal LED OFF");
        digitalWrite(BUILT_IN_LED, HIGH);
      } else if (command_in == "FLA+") {
        Serial.println(serial_no_in + "OKOK" + " Flashlight LED ON");
        digitalWrite(FLASHLIGHT_LED, HIGH);
      } else if (command_in == "FLA-") {
        Serial.println(serial_no_in + "OKOK" + " Flashlight LED OFF");
        digitalWrite(FLASHLIGHT_LED, LOW);
      } else {
        Serial.println(serial_no_in + "BADC " + message_in);
      }
    }
  }
}
