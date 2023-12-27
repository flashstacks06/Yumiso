#include "system.h"





// ------------------------------------------------------ (CONFIG) setup
void setup()
{
  system_init();

  buttonState = LOW;
  lastButtonState = HIGH;
}


// ------------------------------------------------------ loop
void loop()
{
  // PRead button for report
  buttonState = digitalRead(BT_REPORT);



  // ---------------------------------------------------------------- MAIN TIME
  if (millis() - mainRefresh > mainTime)
  {
    mainRefresh = millis();

    gps_update();
    read_clock();

    // -------------------------------------------solo si no esta en proceso de surtido




    // ----------------------------------------- check internet

    if (wifi_check())
    {
      update_clock();
      if (mqtt_check())
      {
        // ------------------------------------------- Send Log
        if (send_log == true)
        {
          mqtt_send_file(file_to_send);
        }

        // ------------------------------------------- Send STATUS
        //if (send_log == true)
        {
          Serial.println("{\"mqtt_status\":\"sending\"}");

          //saveNewlog();

          strcpy(buffer_union_publish, obj["id"].as<const char*>());
          strcat(buffer_union_publish, publish_topic);
          strcat(buffer_union_publish, status_topic);

          //JsonArray logObject = obj_log;
          //size_t serializedLength = measureJson(logObject) + 1;
          char tempBuffer[STATUS_SIZE];
          serializeJson(status_doc, tempBuffer);
          strcpy(buffer_msg_status, tempBuffer);

          Mclient.publish(buffer_union_publish, buffer_msg_status);
          //send_log = false;
        }

        // ------------------------------------------- Send LIST
        if (send_list == true)
        {
          mqtt_send_list();
          send_list = false;
        }
      }
    }

  }




  // ----------------------------------------- save new List
  if (flag_new_list == true)
  {
    flag_new_list = false;

    Serial.print("Saving List on Loop: ");
    //serializeJson(doc_list,Serial);
    //Serial.println();
    //saveListData();
  }



  // ----------------------------------------- save new data
  if (saveConfig == true)  // Data change
  {
    saveConfig = false;

    //Serial.println("{\"upload_config_from_loop\":true}");
    //saveConfigData();

    //Serial.println("saving config");


    //DynamicJsonDocument json(1024);

    //for (WiFiManagerParameter* p : customParams) {
    //  doc[p->getID()] = p->getValue();
    //}

    //File configFile = SPIFFS.open("/config.json", "w");
    //if (!configFile) {
    //  Serial.println("failed to open config file for writing");
    //}

    //serializeJson(obj, Serial);
    //serializeJson(obj, configFile);
    //configFile.close();
    //end save
    //ESP.restart();

    //loadConfig();

    // ----------------------------------------- save new data
    //if (flag_newList)
    //{
    //Serial.println("{\"upload_list\":true}");
    //saveListData();
    //flag_newList = false;
    //loadConfig();
    //saveConfig = false;
    //ESP.restart();
    //return;
    //}
    //else
    //{
    Serial.println("{\"upload_config\":true}");
    saveConfigData();
    loadConfig();
    //
    //}

  }


  // leer boton para imprimir reporte diario
  // Si el botón cambia de no presionado a presionado
  if (lastButtonState == HIGH && buttonState == LOW)
  {
    Serial.println("PUSH");
    buttonPressTime = millis();

  }

  // Si el botón cambia de presionado a no presionado
  if (lastButtonState == LOW && buttonState == HIGH)
  {
    if (millis() - buttonPressTime < longPressDuration)
    {
      Serial.println("Short press detected!");
      read_clock();
      consult_filelog = "/logs/" + String(anio) + "_" + String(mes) + "_" + String(dia_hoy) + ".json";
      print_log = true;
    }
    else if (millis() - buttonPressTime >= (4 * longPressDuration)) // Reinicio de fabrica
    {
      Serial.println("Super Long press detected!");

      obj.clear();
      obj = getJSonFromFile(SPIFFS, &doc, filedefault);


      //print_log = false;
      //clear_log = true;
      //folio = 1;
      //obj["folio"] = folio;

      consult_filelog = "/logs/" + String(anio) + "_" + String(mes) + "_" + String(dia_hoy) + ".json";
      deleteFile(SD, consult_filelog.c_str());


      saveConfig = true;
      Serial.println("{\"default_config\":true}");
      saveConfigData();
      ESP.restart();

    }
    else if (millis() - buttonPressTime >= longPressDuration) // Reinicia el log
    {

      Serial.println("Long press detected!");
      wifiAP(true);
    }


  }

  lastButtonState = buttonState;

  esp_task_wdt_reset();
}
