#include "system.h"


//pinMode(ONDDEMANDPIN, INPUT_PULLUP);

// sd card
bool sd_ready = false;


bool buttonState = LOW;
bool lastButtonState = LOW;
unsigned long buttonPressTime = 0;
const unsigned long longPressDuration = 5000;

bool factory_press = false;
unsigned long factory_time = 0;
unsigned long prev_factory_time = 0;
bool reset_time = false;
volatile bool found_client = false;


unsigned long mainRefresh = obj["mainTime"].as<uint32_t>();
unsigned long mainTime = 1000;

// firebase
const uint32_t connectTimeoutMs = 10000;
unsigned long  s_timestamp;
unsigned long startTime = 0;

// printer
uint32_t startTimeToPrint;

// --------------------------------- printer
const char  end1 = '\r';
const char  end2 = '\n';
uint8_t tempVar = 0;
char tempChar;
uint8_t resultadoBytes[200];
uint32_t pendingPrint = 0;

char resultado[400];

const char* unidades[] = {"", "UNO", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"};
const char* decenas[] = {"", "", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"};
const char* especiales[] = {"DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE"};

//uint32_t unitprice;


const unsigned long intervalo = 10000;
unsigned long tiempoAnterior = 0;
unsigned long tiempoActual;

const unsigned long intervalo2 = 10000;
unsigned long tiempoAnterior2 = 0;
unsigned long tiempoActual2;
volatile bool startCounting2 = false;

// ----------------------------------------GPS intervalos para gps
unsigned long previousMillisGPS = 0;  // Variable para almacenar la última vez que se ejecutó el evento
const long intervalGPS = 60000;  // Intervalo en milisegundos (60,000 milisegundos = 1 minuto)
unsigned long currentMillisGPS;
String gps_name_file;
String gps_str;

// ------------------------------------- wifi flag
bool server_running = false;

uint32_t start_process_time;
float litros;
uint32_t acumulado_litros;
uint32_t target_litros;
float pulsos_litro = 1;
float precio;
float uprice = 9.8; //price of 1 litre
float factor;
uint32_t litros_check;
uint32_t precio_check;

uint32_t folio;
uint32_t reporte;
char b[200];
char buff[200];
int i;
String jsonStr;
unsigned int STATE_DISPLAY = 1;


volatile bool display_reset = false;
volatile bool encoder_reset = false;
volatile bool start_print = false;
volatile bool startCounting = false;
volatile bool startFlowing = false;
volatile bool stopFlowing = false;
volatile bool readyToPrint = false;


volatile uint32_t pesos;


// -------------------------------------------------------------- read_logs
void read_logs(String consult) 
{
  Serial.println("READ ALL LOGS");

  //filelog = "/logs/" + String(anio) + "_" + String(mes) + "_" + String(dia_hoy) + ".json";
  File file = SD.open(consult.c_str(), FILE_READ);
  if (!file) 
  {
    Serial.print("Error al abrir el archivo: ");
    Serial.println(consult);

    printReport();
    
    return;
  }

  uint32_t litros_suma = 0;
  uint32_t servicios = 0;
  uint32_t total_ventas = 0;
  uint32_t folio_ini;
  uint32_t folio_fin;
  uint32_t litros_ini;
  uint32_t litros_fin;
  

  while (file.available()) 
  {
    String line = file.readStringUntil('\n');
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, line);

    if (error) 
    {
      Serial.print("Error al parsear JSON: ");
      Serial.println(error.c_str());
      continue;
    }

    // Extraer los valores del objeto JSON
    uint32_t litros = doc["litros"];
    uint32_t precio = doc["precio"];

    if(servicios == 0)
    {
      folio_ini = doc["folio"];
    }

    folio_fin = doc["folio"];

    servicios++;
    litros_suma += litros;
    total_ventas += precio;
  }

  file.close();
  //printReport (servicios,  ltr,  total, reporte, acumulado_litros, folio_ini, folio_fin, litros_ini, litros_fin)

  litros_ini = acumulado_litros - litros_suma;
  litros_fin = acumulado_litros;

  printReport(servicios, litros_suma, total_ventas, reporte, acumulado_litros, folio_ini, folio_fin, litros_ini, litros_fin);
}

// -------------------------------------------------------------- save_newlog
void saveNewlog()
{
  Serial.println("Make new LOG");
  Serial.print("Litros: ");
  Serial.println(litros);
  Serial.print("Folio: ");
  Serial.println(folio);
  //newLogEntry = obj_log.createNestedObject();
  //newLogEntry["timestamp"] = DateTimeToString(now);

  status_doc["last_service"]["folio"] = folio;
  status_doc["last_service"]["start_timestamp"] = start_process_time;
  status_doc["last_service"]["end_timestamp"] = now.unixtime();
  status_doc["last_service"]["state"] = STATE;
  status_doc["last_service"]["litros"] = litros_check;
  status_doc["last_service"]["precio"] = precio_check;
  status_doc["last_service"]["cliente"] = obj_in["cliente"].as<unsigned int>();

  //if (!obj["gps"]["lat"].isNull())
  //{
  status_doc["last_service"]["lat"] = obj["lat"];
  status_doc["last_service"]["lon"] = obj["lon"];
  //}

  //status_doc["last_service"] = newLogEntry;

  filelog = "/logs/" + String(anio) + "_" + String(mes) + "_" + String(dia_hoy) + ".json";
  consult_filelog = filelog;
  String log_str; //= String((double)status_doc["lon"], 6) + "," + String((double)status_doc["lat"], 6) + "," + String((int)status_doc["time"]);
  //delay(50);
  serializeJson(status_doc["last_service"], log_str);
  //delay(50);
  log_str += '\n'; // O puedes usar gps_str.concat('\n');

  // ------------------------------------------- log de GPS existe?
  //if (testFileIO(SD, gps_name_file.c_str()) == true)
  if (SD.exists(filelog))
  {
    //appendFile(SD, gps_name_file.c_str(), gps_str.c_str());
    appendFile(SD, filelog.c_str(), log_str.c_str());
  }
  else
  {
    //Serial.println("File not found, init SD");
    //sd_ready = false;
    //filelog = "/logs/" + String(anio) + "_" + String(mes) + "_" + String(dia_hoy) + ".json";
    //if (!SD.exists(filelog))
    //{
    Serial.print("File not found, create?: ");
    Serial.println(filelog);
    writeFile(SD, filelog.c_str(), log_str.c_str());
    //}
  }

  //Serial.println(saveJSonArrayToAFile(SD, &obj_log, filelog) ? "{\"log_update_SD\":true}" : "{\"log_update_SD\":false}");
  //if (saveJSonArrayToAFile(SD, &obj_log, filelog))
  //{
  //Serial.println("{\"log_update_SD\":true}");
  //}
  //else
  //{
  //Serial.println("{\"log_update_SD\":false}");
  //sd_ready = false;
  //}



  //if (obj["test"].as<bool>())
  {
    //serializeJsonPretty(newLogEntry, Serial);
    Serial.println(log_str);
  }

  // Litros totales
  acumulado_litros =  obj["acumulado_litros"].as<uint32_t>() + litros_check;
  obj["acumulado_litros"] = acumulado_litros;
  status_doc["acumulado_litros"] = acumulado_litros;

  folio++;
  obj["folio"] = folio;
  status_doc["folio"] = folio; 
  saveConfig = true;
} 

// ------------------------------------------------------------ register_client
void register_client()
{ // Guarda todos los datos de ese cliente en los registros correspondientes


  //serializeJson(obj_in["nombre"], Serial);

  //pulsos_litro = obj_in["pulsos_litro"];
  target_litros = obj_in["litros"];
  uprice = (obj_in["precio"].as<float>());
  factor = (obj_in["factor"].as<float>());
  const char* client_name = obj_in["nombre"].as<const char*>();
  int len = strlen(client_name);

  status_doc["client"]["litros"] = target_litros;
  status_doc["client"]["precio"] = uprice;
  status_doc["client"]["factor"] = factor;
  status_doc["client"]["nombre"] = client_name;
  status_doc["client"]["id"] = obj_in["cliente"];

  Serial.println();
  Serial.print("NAME: ");
  //for (int i = 0; i < len && i < 42; i++) {
  //  name_data[i] = (uint8_t)client_name[i];
  //}

  // Si la longitud de la cadena es menor que 42, rellena el resto del array con 0s
  //for (int i = len; i < 42; i++) {
  //name_data[i] = 0;
  //}

  //Serial.print("NAME2: ");
  //for (int i = 0; i < 42; i++) {
  //  Serial.print(char(name_data[i]));
  //}
  Serial.println();

  Serial.print("Litros: ");
  Serial.println(target_litros);
  //litros = litros * 100;
  //for (int i = 0; i < 4; i++) {
  //litros_num[i] = (litros >> (8 * i)) & 0xFF;
  //Serial.println(litros_num[i]);
  //}
  //Serial.println();

  Serial.print("uPrice: ");
  Serial.println(uprice);
  //litros = litros * 100;
  //for (int i = 0; i < 2; i++) {
  //uprice_data[i] = (uprice >> (8 * i)) & 0xFF;
  //Serial.println(uprice_data[i]);
  //}
  //Serial.println();

  Serial.print("Factor: ");
  Serial.println(factor);
  //litros = litros * 100;
  //for (int i = 0; i < 2; i++) {
  //factor_data[i] = (factor >> (8 * i)) & 0xFF;
  //Serial.println(factor_data[i]);
  //}
  //Serial.println();

}

// -------------------------------------------------------------- search_nclient
void search_nclient(uint32_t aux_client)
{
  //for (int i = 0; i < 4; i++) {
  //  Serial.println(nclient_data[i]);
  //}


  Serial.print("{\"search_client\":"); Serial.print(aux_client); Serial.println("}");

  //new_nclient = 0;
  found_client = false;

  // Buscar el valor de nclient en el array
  for (JsonArray::iterator it = obj_list.begin(); it != obj_list.end(); ++it) {
    obj_in = *it;
    //Serial.println(obj_in["nombre"].as<String>());
    if (obj_in["cliente"].as<uint32_t>() == aux_client) { //-------------------- Cliente encontrado
      Serial.println("{\"client_found\": true}");
      if (obj["test"].as<bool>())
        serializeJson(obj_in, Serial);
      register_client();
      found_client = true;
      break;  // Rompe el bucle una vez que encuentres una coincidencia
    }
  }
  if (!found_client) // ------------- Cliente no encontrado se Busca otra vez el 1
  {
    Serial.println("{\"client_found\": false}");
    for (JsonArray::iterator it = obj_list.begin(); it != obj_list.end(); ++it) {
      obj_in = *it;
      //Serial.println(obj_in["nombre"].as<String>());
      if (obj_in["cliente"].as<uint32_t>() == 0) { //-------------------- Cliente Publico encontrado
        Serial.println("{\"Using Public Client\": true}");
        serializeJson(obj_in, Serial);
        register_client();
        //found_client = true;
        break;  // Rompe el bucle una vez que encuentres una coincidencia
      }
    }
  }
}

// -----------------------------------------------------------system_ init
void system_init()
{

  delay(100);
  Serial.begin(115200);
  Serial.println("Yumiso");
  Serial.print("Version:"); Serial.println(VERSION);
  //delay(5000);


  delay(100);
  I2C_Init();
  Serial.println("i2c_Init");


  status_doc["ver"] = VERSION;



  if (spiffs_init())
  {
    Cfg_get();  // Load File from spiffs
    loadConfig();       // Load and update behaivor of system
    wifi_init();
    mqtt_init();
    mqtt_check();
    rtcUpdated = false;
    ntpConnected = false;
    init_clock();        // I2C for clock
  }

  gps_init();

  // WatchDog Timer
  esp_task_wdt_init(WDT_TIMEOUT, true);  //enable panic so ESP32 restarts
  esp_task_wdt_add(NULL);
  pinMode(BT_REPORT, INPUT_PULLUP);
}

//----------------------------------------------------------------------------------------------------------- reset_config
void reset_config()
{
  //WiFi.disconnect();
  //WiFi.mode(WIFI_OFF);
  //WiFi.mode(WIFI_STA);

  //obj["ssid"] = "";
  //obj["pass"] = "";
  //obj["enable_wifi"] = true;
  //obj["count_wifi"] = 0;
  //obj["registered_wifi"] = false;
  obj = getJSonFromFile(SPIFFS, &doc, filedefault);
  Serial.println(saveJSonToAFile(SPIFFS, &obj, fileconfig) ? "{\"factory_reset\":true}" : "{\"factory_reset\":false}");
  delay(2000);
  //ESP.restart();
  // rp2040.reboot();

}


// ------------------------------------------- strtoBool
/*bool strToBool(String str)
  {
  if (str == "true" || str == "1") {
    return true;
  } else if (str == "false" || str == "0") {
    return false;
  } else {
    // handle invalid input
    return false;
  }
  }*/


// --------------------------------------------------------------------------------------------------- Cfg_get
/*static*/ void Cfg_get(/*struct jsonrpc_request * r*/)
//  {"method":"Config.Get"}
{
  // ----------------------------------------------------- open file to load config
  obj = getJSonFromFile(SPIFFS, &doc, fileconfig);
  if (obj.size() == 0)
  {
    Serial.println("{\"config_file\":\"empty\"}");
    obj = getJSonFromFile(SPIFFS, &doc, filedefault);
    Serial.println(saveJSonToAFile(SPIFFS, &obj, fileconfig) ? "{\"file_default_restore\":true}" : "{\"file_default_restore\":false}");
  }




  if (obj["test"].as<bool>() == true)
  {
    // Comment for production
    serializeJson(obj, Serial);
    Serial.println();

  }

}



// ---------------------------------------------------------------------------------------------------- loadConfig
// Update a new config in the file an change behivor
void loadConfig()
{
  // ----------- Load Counters
  Serial.println("{\"loadConfig\":true}");

  rtc_enable = obj["enable_rtc"].as<bool>();
  ntp_enable = obj["enable_ntp"].as<bool>();

  updated = obj["updated"].as<bool>();

  if (/*(!obj["reboot"].isNull()) && */(obj["reboot"].as<bool>() == true))
  {
    obj["reboot"] = false;
    Serial.println("{\"reboot_upload\":true}");
    saveConfigData();
    Serial.println("{\"reboot\":true}");
    ESP.restart();
  }

  // ------------- ID
  String s_aux = obj["id"].as<String>();
  status_doc["id"] = obj["id"];
  int len = s_aux.length();
  // check for id or mac is the config.json file
  if ((len == 0))
  {
    //(i_aux == 0)
    Serial.println("{\"update_id\":true}");
    Serial.print("{\"ID\":\"");
    //Serial.print(WiFi.macAddress());
    Serial.println("\"}");

    //obj["id"].set( WiFi.macAddress());

    Serial.println(saveJSonToAFile(SPIFFS, &obj, fileconfig) ? "{\"id_file_saved\":true}" : "{\"id_file_saved\":false}" );
  }


  // -------------------------------- mainTime
  // refres time
  JsonVariant objTime = obj["mainTime"];
  if (objTime.isNull())
  {
    Serial.println("{\"mainTime\":NULL}");
    mainTime = 1000;
  }
  else
  {
    mainTime = obj["mainTime"].as<uint32_t>();
    Serial.print("{\"mainTime\":");
    Serial.print(mainTime);
    Serial.println("}");
  }
  mainRefresh = mainTime + 1;


  Serial.println("{\"config\":true}");

}
