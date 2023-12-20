import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';


class MoneybagPage extends StatefulWidget {
  final String userEmail;
  final String qrId;
  final List<String> combinedValues;

  MoneybagPage({
    Key? key,
    required this.userEmail,
    required this.qrId,
    required this.combinedValues,
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
    _moneybagController = TextEditingController(text: '\$1');       //Seteo el valor que irá en moneybag

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
      print('Error al conectarse a MQTT: $e');
    }
  }

void enviarDatosMQTT() {

  final message = [
    widget.userEmail,
    widget.qrId,
    widget.combinedValues.toString(),
  ];
  final formattedMessage = '{${message.join(', ')}}';
  final builder = MqttClientPayloadBuilder();
  builder.addString(formattedMessage);
  final payload = builder.payload;
  if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
    mqttClient.publishMessage('users/route/moneybag', MqttQos.atMostOnce, payload!);
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
                      primary: Colors.blue,
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
