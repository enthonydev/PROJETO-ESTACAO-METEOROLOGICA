#pragma once
// COPIE para local_config.h e preencha SOMENTE na sua maquina.
// Nunca envie SSIDs, senhas ou credenciais reais ao GitHub.
// Wi-Fi 2.4 GHz WPA2-Personal. Portal cativo/802.1X exige outra integracao.
struct WifiProfile { const char* ssid; const char* password; };
const WifiProfile WIFI_PROFILES[] = {
  {"REDE_1", "SENHA_1"},
  {"REDE_2", "SENHA_2"},
  {"REDE_3", "SENHA_3"}
};
const char* STATION_ID = "estacao-esp32-real";
const char* MQTT_HOST = "192.168.1.100"; // IP LAN real do broker, nunca localhost
const uint16_t MQTT_PORT = 1883;
const char* MQTT_USERNAME = "estacao";
const char* MQTT_PASSWORD = "SENHA_DO_BROKER";

// Sensor de pressao: ativar so apos soldar, revisar 3V3, pinagem e modulo.
#define ENABLE_BMP280 0
// MQ-135: nao ativar sem alimentacao 5V correta e saida analogica
// medida/limitada a faixa segura do ESP32. Usar somente GPIO ADC1 livre.
#define ENABLE_MQ135 0
#define MQ135_ADC_PIN 34
// LDR analogico futuro: nao ativar sem fiação real em ADC1 e caracterizacao.
#define ENABLE_LDR_ANALOG 0
#define LDR_ADC_PIN 35
