// Estacao Integrada N2 - Arduino ESP32
// PREPARACAO: instalar PubSubClient, Adafruit SSD1306/GFX, DHT e,
// se ENABLE_BMP280=1, Adafruit BMP280. Copiar local_config.example.h
// para local_config.h e preencher somente localmente.
// NAO substituir DEV 1.1 ate validar esta versao sem sensores novos.
#include <Arduino.h>
#include <WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <time.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include "local_config.h"
#if ENABLE_BMP280
#include <Adafruit_BMP280.h>
#endif

static_assert(sizeof(WIFI_PROFILES) / sizeof(WIFI_PROFILES[0]) >= 2, "Configurar ao menos duas redes");
#define PIN_DHT 16
#define PIN_CHUVA 17
#define PIN_LDR_DIGITAL 5
#define PIN_SDA 21
#define PIN_SCL 22
#define OLED_ADDR 0x3C

DHT dht(PIN_DHT, DHT22);
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
WiFiClient wifiTransport;
PubSubClient mqtt(wifiTransport);
#if ENABLE_BMP280
Adafruit_BMP280 bmp;
bool bmpOk = false;
#endif

const unsigned long SENSOR_INTERVAL = 2000;
const unsigned long DISPLAY_INTERVAL = 500;
const unsigned long SEND_INTERVAL = 10000;
const unsigned long WIFI_TIMEOUT = 12000;
const unsigned long MQTT_RETRY = 5000;

unsigned long lastSensor=0, lastDisplay=0, lastSend=0;
unsigned long wifiAttemptAt=0, mqttAttemptAt=0;
uint8_t selectedWifi=0;
bool wifiConnecting=false, oledOk=false;
float tempC=NAN, humidity=NAN, pressure=NAN;
int mqRaw=-1, ldrPercent=-1;
bool wet=false, dark=false;
bool dhtValid=false;
char telemetryTopic[110];
char digitalTopic[110];

const size_t NETWORK_COUNT=sizeof(WIFI_PROFILES)/sizeof(WIFI_PROFILES[0]);

void connectWifi(size_t networkIndex){
  selectedWifi=networkIndex%NETWORK_COUNT;
  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  Serial.print("[WIFI] Tentando perfil ");
  Serial.println(selectedWifi+1); // Nao imprime SSID nem senha
  WiFi.begin(WIFI_PROFILES[selectedWifi].ssid,WIFI_PROFILES[selectedWifi].password);
  wifiAttemptAt=millis();
  wifiConnecting=true;
}

void maintainWifi(){
  if(WiFi.status()==WL_CONNECTED){
    if(wifiConnecting){
      wifiConnecting=false;
      Serial.print("[WIFI] Conectado no perfil ");
      Serial.print(selectedWifi+1);
      Serial.print(" | IP ");
      Serial.println(WiFi.localIP());
    }
    return;
  }
  if(!wifiConnecting){
    connectWifi(selectedWifi);
  }else if(millis()-wifiAttemptAt>=WIFI_TIMEOUT){
    Serial.println("[WIFI] Falha ou timeout. Tentando proximo perfil.");
    connectWifi((selectedWifi+1)%NETWORK_COUNT);
  }
}

void handleSerialCommand(){
  static char buffer[24];
  static size_t length=0;
  while(Serial.available()){
    char c=(char)Serial.read();
    if(c=='\n'||c=='\r'){
      buffer[length]=0;
      if(length>0){
        int profile=0;
        if(sscanf(buffer,"wifi %d",&profile)==1&&profile>=1&&profile<=(int)NETWORK_COUNT){
          connectWifi((size_t)profile-1);
        }else if(strcmp(buffer,"status")==0){
          Serial.print("[STATUS] wifi=");Serial.print(WiFi.status()==WL_CONNECTED?"online":"offline");
          Serial.print(" mqtt=");Serial.println(mqtt.connected()?"online":"offline");
        }else Serial.println("[COMANDOS] wifi 1 / wifi 2 / wifi 3 / status");
      }
      length=0;
    }else if(length<sizeof(buffer)-1){
      buffer[length++]=c;
    }
  }
}

void maintainMqtt(){
  if(WiFi.status()!=WL_CONNECTED||mqtt.connected())return;
  if(millis()-mqttAttemptAt<MQTT_RETRY)return;
  mqttAttemptAt=millis();
  char clientId[64];
  snprintf(clientId,sizeof(clientId),"esp32-%06lx",(unsigned long)(ESP.getEfuseMac()&0xffffff));
  bool ok=mqtt.connect(clientId,MQTT_USERNAME,MQTT_PASSWORD);
  Serial.println(ok?"[MQTT] Conectado":"[MQTT] Falha. Nova tentativa em 5s.");
}

void readSensors(){
  float t=dht.readTemperature();
  float h=dht.readHumidity();
  dhtValid=isfinite(t)&&isfinite(h)&&t>=-40&&t<=80&&h>=0&&h<=100;
  tempC=dhtValid?t:NAN;
  humidity=dhtValid?h:NAN;
  wet=(digitalRead(PIN_CHUVA)==LOW);
  dark=(digitalRead(PIN_LDR_DIGITAL)==HIGH);
#if ENABLE_BMP280
  if(bmpOk){
    pressure=bmp.readPressure()/100.0f;
    if(!isfinite(pressure)||pressure<=0)pressure=NAN;
  }
#endif
#if ENABLE_MQ135
  mqRaw=analogRead(MQ135_ADC_PIN); // 0..4095, somente se entrada protegida
#endif
#if ENABLE_LDR_ANALOG
  // TODO: registrar orientacao escuro/claro e extremos aferidos na bancada
  // antes de autorizar percentuais. Nao inventar calibracao.
  ldrPercent=-1;
#endif
  Serial.print("Temperatura: ");
  if(dhtValid)Serial.print(tempC,1);else Serial.print("ERRO");
  Serial.print(" C | Umidade: ");
  if(dhtValid)Serial.print(humidity,1);else Serial.print("ERRO");
  Serial.print(" % | Chuva: ");Serial.print(wet?"SIM":"NAO");
  Serial.print(" | Luz: ");Serial.println(dark?"ESCURO":"CLARO");
}

void redraw(){
  if(!oledOk)return;
  oled.clearDisplay();oled.setTextSize(1);oled.setTextColor(SSD1306_WHITE);
  oled.setCursor(43,0);oled.println("ESTACAO");
  oled.setCursor(20,9);oled.println("METEOROLOGICA");
  oled.drawLine(0,19,127,19,SSD1306_WHITE);
  oled.setCursor(0,22);oled.print("TEMP: ");
  if(dhtValid){oled.print(tempC,1);oled.println(" C");}else oled.println("--.- C");
  oled.setCursor(0,32);oled.print("UMID: ");
  if(dhtValid){oled.print(humidity,1);oled.println(" %");}else oled.println("--.- %");
  oled.setCursor(0,42);oled.print("CHUVA: ");oled.println(wet?"SIM":"NAO");
  oled.setCursor(0,52);oled.print("LUZ: ");oled.println(dark?"ESCURO":"CLARO");
  oled.setCursor(64,56);oled.print(" by:makers");
  oled.display();
}

String numberOrNull(float n,unsigned int decimals){
  if(!isfinite(n))return "null";
  return String(n,decimals);
}

void publishTelemetry(){
  if(!mqtt.connected())return;
  time_t current=time(nullptr);
  if(current<1704067200){
    Serial.println("[NTP] Aguardando hora UTC valida. Nao transmitir timestamp inventado.");
    return;
  }
  struct tm utc;
  gmtime_r(&current,&utc);
  char timestamp[30];
  strftime(timestamp,sizeof(timestamp),"%Y-%m-%dT%H:%M:%SZ",&utc);

  String tempJson=numberOrNull(tempC,2);
  String humidJson=numberOrNull(humidity,2);
  String pressureJson=numberOrNull(pressure,2);
  String mqJson=mqRaw<0?"null":String(mqRaw);
  String ldrJson=ldrPercent<0?"null":String(ldrPercent);

  char json[850];
  int written=snprintf(json,sizeof(json),
    "{\"schema_version\":\"1.0\",\"station_id\":\"%s\","
    "\"timestamp\":\"%s\",\"location\":{\"latitude\":null,\"longitude\":null},"
    "\"measurements\":{\"temperature_c\":%s,\"humidity_pct\":%s,"
    "\"pressure_hpa\":%s,\"air_quality_raw\":%s,\"luminosity_pct\":%s,\"rain_mm\":null},"
    "\"quality\":{\"temperature\":\"%s\",\"humidity\":\"%s\","
    "\"pressure\":\"%s\",\"air_quality\":\"%s\",\"luminosity\":\"%s\",\"rain\":\"error\"}}",
    STATION_ID,timestamp,tempJson.c_str(),humidJson.c_str(),
    pressureJson.c_str(),mqJson.c_str(),ldrJson.c_str(),
    dhtValid?"ok":"error",dhtValid?"ok":"error",
    isfinite(pressure)?"ok":"error",
    mqRaw>=0?"suspect":"error",
    ldrPercent>=0?"suspect":"error");
  if(written<=0||(size_t)written>=sizeof(json)){
    Serial.println("[MQTT] Payload excedeu tamanho seguro");return;
  }
  bool ok=mqtt.publish(telemetryTopic,json);
  Serial.println(ok?"[MQTT] Telemetria publicada":"[MQTT] Falha ao publicar");
  // Estados digitais em topico diagnostico separado (fora do schema numerico v1.0).
  char digital[170];
  snprintf(digital,sizeof(digital),
    "{\"station_id\":\"%s\",\"timestamp\":\"%s\",\"rain_detected\":%s,\"dark\":%s}",
    STATION_ID,timestamp,wet?"true":"false",dark?"true":"false");
  mqtt.publish(digitalTopic,digital);
}

void setup(){
  Serial.begin(115200);
  dht.begin();
  pinMode(PIN_CHUVA,INPUT_PULLUP);
  pinMode(PIN_LDR_DIGITAL,INPUT);
  Wire.begin(PIN_SDA,PIN_SCL);
  oledOk=oled.begin(SSD1306_SWITCHCAPVCC,OLED_ADDR);
  if(!oledOk)Serial.println("[OLED] Display indisponivel, sensores continuam.");
#if ENABLE_BMP280
  bmpOk=bmp.begin(0x76)||bmp.begin(0x77);
  Serial.println(bmpOk?"[BMP280] Encontrado":"[BMP280] Nao encontrado");
#endif
#if ENABLE_MQ135
  analogReadResolution(12);
  analogSetPinAttenuation(MQ135_ADC_PIN,ADC_11db);
#endif
  snprintf(telemetryTopic,sizeof(telemetryTopic),"estacao/%s/telemetry",STATION_ID);
  snprintf(digitalTopic,sizeof(digitalTopic),"estacao/%s/digital",STATION_ID);
  mqtt.setServer(MQTT_HOST,MQTT_PORT);
  mqtt.setBufferSize(1024);
  configTime(0,0,"pool.ntp.org","time.google.com");
  readSensors();redraw();
  connectWifi(0);
  Serial.println("[SISTEMA] Digite wifi 1, wifi 2, wifi 3, status no Monitor Serial.");
}

void loop(){
  handleSerialCommand();
  maintainWifi();
  maintainMqtt();
  if(mqtt.connected())mqtt.loop();
  unsigned long now=millis();
  if(now-lastSensor>=SENSOR_INTERVAL){lastSensor=now;readSensors();}
  if(now-lastDisplay>=DISPLAY_INTERVAL){lastDisplay=now;redraw();}
  if(now-lastSend>=SEND_INTERVAL){lastSend=now;publishTelemetry();}
}
