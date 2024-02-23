import 'dart:math';

import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:convert';

// Importa las páginas a las que necesitas navegar
import 'route_check.dart';
import 'manteinance.dart';
// Asegúrate de que estas importaciones coincidan con los nombres de archivo y clase en tu proyecto

class QRCodeScannerApp extends StatefulWidget {
  final String mqttResponse; // Agregado para recibir la respuesta MQTT
  final String userEmail;    // Correo electrónico del usuario

  QRCodeScannerApp({Key? key, required this.mqttResponse, required this.userEmail}) : super(key: key);

  @override
  _QRCodeScannerAppState createState() => _QRCodeScannerAppState();
}

MqttServerClient createRandomMqttClient(String broker, int port) {
  final Random random = Random();
  final int randomNumber = random.nextInt(10000);
  final String clientId = 'mqtt_client_$randomNumber';

  final MqttServerClient mqttClient = MqttServerClient.withPort(broker, clientId, port);

  return mqttClient;
}

class _QRCodeScannerAppState extends State<QRCodeScannerApp> {
  late QRViewController _controller;
  final GlobalKey _qrKey = GlobalKey(debugLabel: 'QR');
  String qrId = ''; // Variable para almacenar el número de ID del código QR
  final MqttServerClient mqttClient = createRandomMqttClient('137.184.86.135', 1883);
  bool mqttConnected = false; // Bandera para verificar la conexión MQTT

  @override
  void initState() {
    super.initState();
    _connectToMQTT();
  }

  @override
  void dispose() {
    _controller.dispose();
    mqttClient.disconnect();
    super.dispose();
  }

  void _connectToMQTT() async {
    try {
      await mqttClient.connect();
      mqttConnected = true;
    } catch (e) {
      print('Error al conectarse a MQTT: $e');
      mqttConnected = false;
    }
  }

  void enviarDatosMQTT() {
    const textoEspecifico = 'reporte'; // Reemplaza con tu mensaje
    final builder = MqttClientPayloadBuilder();
    builder.addString(textoEspecifico);
    final payload = builder.payload;
    
    if (mqttConnected && qrId.isNotEmpty && widget.mqttResponse == 'Route') {
      mqttClient.publishMessage('maquinas/$qrId/in/reporte', MqttQos.atMostOnce, payload!);
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Column(
          children: [
            Expanded(
              flex: 5,
              child: QRView(
                key: _qrKey,
                onQRViewCreated: _onQRViewCreated,
                overlay: QrScannerOverlayShape(
                  borderColor: Colors.red,
                  borderRadius: 10,
                  borderLength: 30,
                  borderWidth: 10,
                  cutOutSize: 300,
                ),
                onPermissionSet: (ctrl, p) => _onPermissionSet(context, ctrl, p),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      onChanged: (value) {
                        setState(() {
                          qrId = value;
                        });
                      },
                      decoration: InputDecoration(
                        labelText: 'QR ID',
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ),
                  SizedBox(width: 8.0),
                  ElevatedButton(
                    onPressed: () {
                      _navegarSegunMqttResponse();
                    },
                    child: Text('Confirmar'),
                  ),
                ],
              ),
            ),
            Align(
              alignment: Alignment.bottomCenter,
              child: Container(
                margin: EdgeInsets.all(16.0),
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16.0),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.5),
                      spreadRadius: 1,
                      blurRadius: 2,
                      offset: Offset(0, 1),
                    ),
                  ],
                ),
                child: Text(
                  'Número de Máquina: $qrId',
                  style: TextStyle(fontSize: 18.0),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    _controller = controller;
    _controller.scannedDataStream.listen((scanData) {
      if (qrId.isEmpty) {
        final code = scanData.code;
        try {
          final decodedData = json.decode(code!);
          if (decodedData is Map<String, dynamic> &&
              decodedData.containsKey('id') &&
              decodedData['id'] is String) {
            qrId = decodedData['id'];
            print('QR ID: $qrId');
            setState(() {});
            _navegarSegunMqttResponse(); // Navega según la respuesta MQTT
          } else {
            print('QR code does not have the expected format.');
          }
        } catch (e) {
          print('Error decoding QR code: $e');
        }
      }
    });
  }

  void _navegarSegunMqttResponse() {
    if (qrId.isNotEmpty) {
      switch (widget.mqttResponse) {
        case 'Route':
          enviarDatosMQTT();
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => RouteCheck(userEmail: widget.userEmail, qrId: qrId)),
          );
          break;
        case 'Maintenance':
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => Maintenance1(userEmail: widget.userEmail, qrId: qrId)),
          );
          break;
        // No se necesita manejar 'Arcade' aquí ya que se maneja en MyHomePage
      }
    }
  }

  void _onPermissionSet(BuildContext context, QRViewController ctrl, bool p) {
    if (!p) {
      // Handle permission denied
    }
  }
}
