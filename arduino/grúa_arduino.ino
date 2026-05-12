#include <AccelStepper.h>

// Pines para motores DC (TB6612FNG)
#define AIN1 2   // Motor A (Carro) - Dirección 1
#define AIN2 4   // Motor A (Carro) - Dirección 2
#define PWMA 3   // Motor A (Carro) - PWM
#define BIN1 7   // Motor B (Elevación) - Dirección 1
#define BIN2 8   // Motor B (Elevación) - Dirección 2
#define PWMB 5   // Motor B (Elevación) - PWM

// Pines para motor Nema 17 (DRV8825)
#define STEP_PIN 9
#define DIR_PIN 10

// Crear instancia del stepper
AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Variables para control
unsigned long lastCommandTime = 0;
const unsigned long TIMEOUT = 2000; // 2 segundos
bool giroActive = false;
int giroDirection = 0; // 0: stop, 1: left, -1: right

void setup() {
  // Configurar pines motores DC
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(BIN1, OUTPUT);
  pinMode(BIN2, OUTPUT);
  pinMode(PWMB, OUTPUT);

  // Configurar stepper
  stepper.setMaxSpeed(1000.0);
  stepper.setAcceleration(500.0);

  // Iniciar comunicación serial
  Serial.begin(9600);

  // Inicializar motores detenidos
  stopAllMotors();
}

void loop() {
  // Leer comandos seriales
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    processCommand(command);
    lastCommandTime = millis();
  }

  // Ejecutar movimiento del stepper si activo
  if (giroActive) {
    stepper.runSpeed();
  }

  // Frenado automático por timeout
  if (millis() - lastCommandTime > TIMEOUT) {
    stopAllMotors();
  }
}

void processCommand(String cmd) {
  if (cmd == "CL") {
    // Carro izquierda
    setMotorA(-255); // Velocidad máxima hacia atrás
  } else if (cmd == "CR") {
    // Carro derecha
    setMotorA(255); // Velocidad máxima hacia adelante
  } else if (cmd == "EU") {
    // Elevación arriba
    setMotorB(255);
  } else if (cmd == "ED") {
    // Elevación abajo
    setMotorB(-255);
  } else if (cmd == "GL") {
    // Giro izquierda
    giroDirection = -1;
    stepper.setSpeed(-500.0); // Velocidad negativa para izquierda
    giroActive = true;
  } else if (cmd == "GR") {
    // Giro derecha
    giroDirection = 1;
    stepper.setSpeed(500.0); // Velocidad positiva para derecha
    giroActive = true;
  } else if (cmd == "S") {
    // Stop
    stopAllMotors();
  }
}

void setMotorA(int speed) {
  // speed: -255 a 255
  if (speed > 0) {
    digitalWrite(AIN1, HIGH);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, speed);
  } else if (speed < 0) {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, HIGH);
    analogWrite(PWMA, -speed);
  } else {
    digitalWrite(AIN1, LOW);
    digitalWrite(AIN2, LOW);
    analogWrite(PWMA, 0);
  }
}

void setMotorB(int speed) {
  // speed: -255 a 255
  if (speed > 0) {
    digitalWrite(BIN1, HIGH);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, speed);
  } else if (speed < 0) {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, HIGH);
    analogWrite(PWMB, -speed);
  } else {
    digitalWrite(BIN1, LOW);
    digitalWrite(BIN2, LOW);
    analogWrite(PWMB, 0);
  }
}

void stopAllMotors() {
  setMotorA(0);
  setMotorB(0);
  giroActive = false;
  giroDirection = 0;
}