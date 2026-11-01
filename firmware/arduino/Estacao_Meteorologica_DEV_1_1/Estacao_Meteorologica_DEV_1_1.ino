// Estacao Meteorologica - DEV 1.1
// Firmware Arduino ESP32 validado em bancada; USB Serial 115200
// Requer Adafruit GFX, Adafruit SSD1306 e DHT sensor library.
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

#define OLED_LARGURA 128
#define OLED_ALTURA 64
#define OLED_SDA 21
#define OLED_SCL 22
#define OLED_ENDERECO 0x3C
#define DHT_PIN 16
#define DHT_TIPO DHT22
#define CHUVA_PIN 17
#define LDR_PIN 5

Adafruit_SSD1306 display(OLED_LARGURA, OLED_ALTURA, &Wire, -1);
DHT dht(DHT_PIN, DHT_TIPO);

const unsigned long INTERVALO_DHT = 2000;
const unsigned long INTERVALO_CHUVA = 200;
const unsigned long INTERVALO_LDR = 200;
const unsigned long INTERVALO_OLED = 200;
const unsigned long INTERVALO_DIAGNOSTICO = 5000;

unsigned long tempoDHT = 0;
unsigned long tempoChuva = 0;
unsigned long tempoLDR = 0;
unsigned long tempoOLED = 0;
unsigned long tempoDiagnostico = 0;
float temperatura = NAN;
float umidade = NAN;
bool chuvaDetectada = false;
bool chuvaInicializada = false;
int estadoLDR = -1;

void atualizarDHT() {
  float novaTemperatura = dht.readTemperature();
  float novaUmidade = dht.readHumidity();
  if (!isnan(novaTemperatura) && !isnan(novaUmidade)) {
    temperatura = novaTemperatura;
    umidade = novaUmidade;
    Serial.print("Temperatura: ");
    Serial.print(temperatura, 1);
    Serial.print(" C | Umidade: ");
    Serial.print(umidade, 1);
    Serial.println(" %");
  } else {
    Serial.println("[ERRO] Falha na leitura do DHT22!");
  }
}

void atualizarChuva() {
  bool novaLeitura = (digitalRead(CHUVA_PIN) == LOW);
  if (!chuvaInicializada || novaLeitura != chuvaDetectada) {
    chuvaDetectada = novaLeitura;
    chuvaInicializada = true;
    Serial.print("Chuva: ");
    Serial.println(chuvaDetectada ? "DETECTADA" : "NAO DETECTADA");
  }
}

void atualizarLDR() {
  int novaLeitura = digitalRead(LDR_PIN);
  if (estadoLDR == -1 || novaLeitura != estadoLDR) {
    estadoLDR = novaLeitura;
    Serial.print("Luminosidade: ");
    Serial.println(estadoLDR == HIGH ? "ESCURO" : "CLARO");
  }
}

void executarDiagnostico() {
  int leituraChuva = digitalRead(CHUVA_PIN);
  Serial.print("[DIAGNOSTICO] Chuva GPIO17: ");
  Serial.print(leituraChuva == LOW ? "LOW" : "HIGH");
  Serial.print(" | Interpretacao: ");
  Serial.println(leituraChuva == LOW ? "AGUA DETECTADA" : "SEM AGUA DETECTADA");
}

void atualizarOLED() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(43, 0);
  display.println("ESTACAO");
  display.setCursor(20, 9);
  display.println("METEOROLOGICA");
  display.drawLine(0, 19, 127, 19, SSD1306_WHITE);

  display.setCursor(0, 22);
  display.print("TEMP: ");
  if (isnan(temperatura)) display.println("--.- C");
  else { display.print(temperatura, 1); display.println(" C"); }

  display.setCursor(0, 32);
  display.print("UMID: ");
  if (isnan(umidade)) display.println("--.- %");
  else { display.print(umidade, 1); display.println(" %"); }

  display.setCursor(0, 42);
  display.print("CHUVA: ");
  if (!chuvaInicializada) display.println("...");
  else display.println(chuvaDetectada ? "SIM" : "NAO");

  display.setCursor(0, 52);
  display.print("LUZ: ");
  if (estadoLDR == -1) display.println("...");
  else display.println(estadoLDR == HIGH ? "ESCURO" : "CLARO");

  display.setCursor(64, 56);
  display.print(" by:makers");
  display.display();
}

void setup() {
  Serial.begin(115200);
  Wire.begin(OLED_SDA, OLED_SCL);
  dht.begin();
  pinMode(CHUVA_PIN, INPUT_PULLUP);
  pinMode(LDR_PIN, INPUT);

  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ENDERECO)) {
    Serial.println("[ERRO] OLED nao encontrada!");
    while (true) delay(1000);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(25, 25);
  display.println("INICIANDO...");
  display.display();

  atualizarDHT();
  atualizarChuva();
  atualizarLDR();
  atualizarOLED();

  unsigned long agora = millis();
  tempoDHT = agora;
  tempoChuva = agora;
  tempoLDR = agora;
  tempoOLED = agora;
  tempoDiagnostico = agora;
  Serial.println("[SISTEMA] Estacao meteorologica iniciada.");
}

void loop() {
  unsigned long agora = millis();
  if (agora - tempoDHT >= INTERVALO_DHT) {
    tempoDHT = agora; atualizarDHT();
  }
  if (agora - tempoChuva >= INTERVALO_CHUVA) {
    tempoChuva = agora; atualizarChuva();
  }
  if (agora - tempoLDR >= INTERVALO_LDR) {
    tempoLDR = agora; atualizarLDR();
  }
  if (agora - tempoOLED >= INTERVALO_OLED) {
    tempoOLED = agora; atualizarOLED();
  }
  if (agora - tempoDiagnostico >= INTERVALO_DIAGNOSTICO) {
    tempoDiagnostico = agora; executarDiagnostico();
  }
}
