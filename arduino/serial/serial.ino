#include <LiquidCrystal_I2C.h>

#define I2C_ADDR    0x27
#define LCD_COLUMNS 16
#define LCD_LINES   2
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_LINES);
const int TRIGPIN = 10;          
const int ECHOPIN = 11;
long timer;
int jarak;

int buttonPin = 2; 
int buttonPin2 = 3;
int buttonPin3 = 4;
int buttonPin4 = 5;
int buttonPin5 = 9;
int buttonState = HIGH;
int buttonState2 = HIGH;
int buttonState3 = HIGH;
int buttonState4 = HIGH;
int buttonState5 = HIGH;

// state
bool detected = false;
long duration;
int distance;
String text;
void setup() {
    // Init
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  for (int i = 0; i < 5; i++) {
    lcd.clear();
    lcd.print("Tunggu yaa -_-");
    delay(500);  // Tampilkan selama 500ms
    lcd.clear();
    lcd.print("Tunggu yaa -_0");
    delay(500);  // Tampilkan selama 500ms
  }
  lcd.clear();
  lcd.print("TABITA :)");
  pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  pinMode(buttonPin4, INPUT_PULLUP);
  // pinMode(buttonPin5, INPUT_PULLUP);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  delay(2000);
}

void loop() {
  digitalWrite(LED_BUILTIN, LOW);
  buttonState = digitalRead(buttonPin);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);
  // buttonState5 = digitalRead(buttonPin5);
  if (buttonState == LOW) {
    Serial.println("up");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
  }
  else if (buttonState2 == LOW) {
    Serial.println("right");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);

  }
  else if (buttonState3 == LOW) {
    Serial.println("down");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
  }
  else if (buttonState4 == LOW) {
    Serial.println("left");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
  } 
  // else if (buttonState5 == LOW) {
  //   Serial.println("click");
  //   digitalWrite(LED_BUILTIN, HIGH);
  //   delay(200);
  // }

  digitalWrite(TRIGPIN, LOW);                   
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, HIGH);                  
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);                   
  duration = pulseIn(ECHOPIN, HIGH);
  // menghitung jarak
  distance = duration * 0.034 / 2; // kecepatan suara dibagi 2 (datang dan kembali)
  
  // Check distance and toggle detection state accordingly
  // Serial.println(distance);
  if (distance < 30 && !detected && distance > 1) {  // Detect when someone hovers for the first time
    Serial.println("jarak.1");
    lcd.clear();
    lcd.print("Arahkan uang anda");
    detected = true;  // Set detected to true to avoid repeating the message
    // Serial.println(detected);
  }

  if (distance >= 30 && detected) {  // Detect when the person moves away for the first time
    Serial.println("jarak.0");
    lcd.clear();
    lcd.print("Goodbye! <3");
    delay(1500);
    lcd.clear();
    lcd.print("TABITA :D");
    detected = false;  // Set detected to false to avoid repeating the message
  }
}