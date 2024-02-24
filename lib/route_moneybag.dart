import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';


class MoneybagPage extends StatefulWidget {
  final String userEmail;
  final String qrId;
  final String combinedValues;
  final String bagid;

  MoneybagPage({
    Key? key,
    required this.userEmail,
    required this.qrId,
    required this.combinedValues, 
    required this.bagid,
  }) : super(key: key);

  @override
  State<MoneybagPage> createState() => _MoneybagPageState();

}

MqttServerClient createRandomMqttClient(String broker, int port) {
  final Random random = Random();
  final int randomNumber = random.nextInt(10000);
  final String clientId = 'mqtt_client_$randomNumber';

  final MqttServerClient mqttClient = MqttServerClient.withPort(broker, clientId, port);

  return mqttClient;
}

class _MoneybagPageState extends State<MoneybagPage> {
  late TextEditingController _timeController;
  late TextEditingController _moneybagController;
  late Timer _timer;
  final MqttServerClient mqttClient = createRandomMqttClient('137.184.86.135', 1883);

  @override
  void initState() {
    _connectToMQTT();
    super.initState();
    _timeController = TextEditingController(text: _getCurrentTime());   //Actualizo en tiempo real el tiempo
    _moneybagController = TextEditingController(text: widget.bagid);       //Seteo el valor que irá en moneybag

    _timer = Timer.periodic(const Duration(seconds: 1), _updateTime);
  }

  String _getCurrentTime() {
    final now = DateTime.now();
    return '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';
  }

  void _updateTime(Timer timer) {
    setState(() {
      _timeController.text = _getCurrentTime();
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    _timeController.dispose();
    _moneybagController.dispose();
    super.dispose();
  }

  void _connectToMQTT() async {
    try {
      await mqttClient.connect();
    } catch (e) {
      if (kDebugMode) {
        print('Error al conectarse a MQTT: $e');
      }
    }
  }

void enviarDatosMQTT() {
  final Map<String, dynamic> message = {
    'Correo': widget.userEmail,
    'qrid': widget.qrId,
    'bag': widget.bagid,
    'data': widget.combinedValues.toString(),
  };
  //final formattedMessage = '{${message.join(', ')}}';
  final builder = MqttClientPayloadBuilder();
  builder.addString(json.encode(message));
  final payload = builder.payload;
  
  const textoEspecifico = 'reporte'; // Reemplaza con tu mensaje
  final builder2 = MqttClientPayloadBuilder(); // Aquí se debe usar builder en lugar de builder2
  builder2.addString(textoEspecifico); // Aquí se debe usar builder en lugar de builder2
  final payload2 = builder2.payload; // Aquí se debe usar builder en lugar de builder2

  if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
    mqttClient.publishMessage('users/route/moneybag/${widget.qrId}', MqttQos.atMostOnce, payload!);
    //mqttClient.publishMessage('maquinas/${widget.qrId}/in/reporte', MqttQos.atMostOnce, payload2!);   //maquinas/id/in/reporte
    Fluttertoast.showToast(
      msg: 'Datos enviados a MQTT',
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.green,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  } else {
    Fluttertoast.showToast(
      msg: 'Error: No se pudo enviar datos a MQTT porque la conexión no está activa.',
      toastLength: Toast.LENGTH_SHORT,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.red,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.center,
                  child: const Text(
                    'Moneybag',
                    style: TextStyle(fontSize: 36, color: Colors.white, fontFamily: 'Cabin'),
                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    const Text(
                      'MoneyBag',
                      style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                    ),
                    Container(
                      width: 120,
                      height: 40,
                      margin: const EdgeInsets.only(left: 10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: TextField(
                        controller: _moneybagController,
                        enabled: false,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 22, color: Colors.black, fontFamily: 'Cabin'),
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    const Text(
                      'Cut-off-time',
                      style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                    ),
                    Container(
                      width: 120,
                      height: 40,
                      margin: const EdgeInsets.only(left: 10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: TextField(
                        controller: _timeController,
                        enabled: false,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 22, color: Colors.black, fontFamily: 'Cabin'),
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 30),
                Container(
                  alignment: Alignment.center,
                  child: ElevatedButton(
                    onPressed: enviarDatosMQTT,
                    child: const Text('Finish'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
