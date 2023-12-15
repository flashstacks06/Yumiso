import 'dart:math';

import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

class Maintenance1 extends StatefulWidget {
  final String userEmail;
  final String qrId;

  Maintenance1({Key? key, required this.userEmail, required this.qrId}) : super(key: key);

  @override
  _Maintenance1State createState() => _Maintenance1State();
}

MqttServerClient createRandomMqttClient(String broker, int port) {
  final Random random = Random();
  final int randomNumber = random.nextInt(10000);
  final String clientId = 'mqtt_client_$randomNumber';

  final MqttServerClient mqttClient = MqttServerClient.withPort(broker, clientId, port);

  return mqttClient;
}

class _Maintenance1State extends State<Maintenance1> {
  List<bool> functionalOptions = List.generate(6, (index) => false);
  List<int> selectionMatrix = List.generate(6, (index) => 0);

  final MqttServerClient mqttClient = createRandomMqttClient('137.184.86.135', 1883);

  @override
  void initState() {
    super.initState();
    _connectToMQTT();
  }

  void _connectToMQTT() async {
    try {
      await mqttClient.connect();
    } catch (e) {
      print('Error al conectarse a MQTT: $e');
    }
  }

  void enviarDatosMQTT() {
    final message = {
      widget.userEmail,
      widget.qrId,
      selectionMatrix.toString(),
    };

    final builder = MqttClientPayloadBuilder();
    builder.addString(message.toString());

    final payload = builder.payload;

    if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
      mqttClient.publishMessage('users/maintenance', MqttQos.atMostOnce, payload!);
      print('Datos enviados a MQTT');
    } else {
      print('Error: No se pudo enviar datos a MQTT porque la conexión no está activa.');
    }
  }

  Widget largeCheckbox(bool value, ValueChanged<bool?> onChanged, int index, String category) {
    return Transform.scale(
      scale: 2.0,
      child: Checkbox(
        value: value,
        onChanged: onChanged,
      ),
    );
  }

  void mostrarAlerta(String title, String message) {
    Fluttertoast.showToast(
      msg: message,
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.green,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  @override
  Widget build(BuildContext context) {
    List<String> titles = ['Coin Selector', 'Motherboard', 'Joystick'];

    List<Widget> functionalOptionWidgets = [];
    List<Widget> images = [];

    for (var i = 0; i < 3; i++) {
      images.add(
        Column(
          children: [
            Image.asset(
              'img/man${i + 1}.jpg',
              width: MediaQuery.of(context).size.width * 0.3,
              height: MediaQuery.of(context).size.width * 0.3,
            ),
            SizedBox(height: 8),
            Text(
              titles[i],
              style: TextStyle(fontSize: 18, fontFamily: 'Cabin', color: Colors.white),
            ),
          ],
        ),
      );

      functionalOptionWidgets.add(
        Column(
          children: [
            largeCheckbox(
              functionalOptions[i],
              (value) {
                setState(() {
                  functionalOptions[i] = value!;
                  int optionValue = value ? 1 : 0;
                  selectionMatrix[i] = optionValue;
                });
              },
              i,
              'Functional',
            ),
          ],
        ),
      );
    }

    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: [
              Text(
                'Maintenance',
                style: TextStyle(fontSize: 36, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 30),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: images,
              ),
              SizedBox(height: 20),
              Text(
                'Functional',
                style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: functionalOptionWidgets,
              ),
              ElevatedButton(
                onPressed: () {
                  print('Correo Electrónico: ${widget.userEmail}');
                  print('QR ID: ${widget.qrId}');
                  print('Selecciones: $selectionMatrix');
                  enviarDatosMQTT();

                  if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
                    mostrarAlerta('Orden creada', 'La orden de mantenimiento se ha creado correctamente.');
                  } else {
                    mostrarAlerta('Error', 'No se pudieron enviar los datos a MQTT debido a una conexión no activa.');
                  }
                },
                child: Text('Finish'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
