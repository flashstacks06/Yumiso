#ifndef SYSTEM_H
#define SYSTEM_H

#include <Arduino.h>
#include <ArduinoJson.h>
//#include <vector>
#include <PubSubClient.h>
#include <WiFi.h>


#define   PRESS   LOW

#define WDT_TIMEOUT     150
//#define BT_REPORT       0



#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager

#include "FS.h"
#include "SPIFFS.h"
#include <Wire.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include "time.h"
#include "RTClib.h"
#include <Wire.h>
#include <TinyGPSPlus.h>
#include <Firebase_ESP_Client.h>
#include <esp_task_wdt.h>
#include <cmath> // 
#include "SPI.h"


#include "version.h"
#include "wifiservice.h"
#include "pins.h"
#include "filespiffs.h"
#include "mqttservice.h"
#include "wireservice.h"
#include "clock.h"
#include "gps_service.h"
#include "firebasedb.h"


//15 seconds WDT

// sd card
//extern bool sd_ready;

extern bool buttonState;
extern bool lastButtonState;
extern unsigned long buttonPressTime;
extern const unsigned long longPressDuration;

extern unsigned long startTime;

extern bool factory_press;
extern unsigned long factory_time;
extern unsigned long prev_factory_time;
//extern bool reset_time;
//extern byte localAddress;     // address of this device
extern unsigned long mainRefresh;
extern unsigned long mainTime;
extern const uint32_t connectTimeoutMs;
extern unsigned long  s_timestamp;
extern volatile bool found_client;


// ----------------------------------------GPS intervalos para gps
extern unsigned long previousMillisGPS;  // Variable para almacenar la última vez que se ejecutó el evento
extern const long intervalGPS;  // Intervalo en milisegundos (60,000 milisegundos = 1 minuto)
extern unsigned long currentMillisGPS; 

// ------------------------------------- wifi flag
extern bool server_running;

extern String gps_name_file;
extern String gps_str;


extern uint32_t start_process_time;
extern float litros;
extern uint32_t acumulado_litros;
extern float pulsos_litro;
extern float precio;
extern float uprice; //price of 1 litre
extern uint32_t litros_check;
extern uint32_t precio_check;

extern uint32_t folio;
extern char b[200];
extern char buff[200];
extern int i;
extern String jsonStr;
extern unsigned int STATE_DISPLAY;

extern volatile bool display_reset;
extern volatile bool encoder_reset;
extern volatile bool start_print;
extern volatile bool startCounting;
extern volatile bool startFlowing;
extern volatile bool stopFlowing;
extern volatile bool readyToPrint;


extern volatile uint32_t pesos;

//void IRAM_ATTR factory_reset3();
void reset_config();
//void check_reset();
bool strToBool(String str);
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max);
void loadConfig();
/*static*/ void Cfg_get(/*struct jsonrpc_request * r*/);
void system_init();


#endif
