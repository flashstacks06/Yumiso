import 'dart:math';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'route_stock.dart'; // Importa RouteStock

class RouteCheck extends StatefulWidget {
  final String userEmail;
  final String qrId;
  RouteCheck({Key? key, required this.userEmail, required this.qrId}) : super(key: key);

  @override
  _RouteCheckState createState() => _RouteCheckState();
}

MqttServerClient createRandomMqttClient(String broker, int port) {
  final Random random = Random();
  final int randomNumber = random.nextInt(10000);
  final String clientId = 'mqtt_client_$randomNumber';

  final MqttServerClient mqttClient = MqttServerClient.withPort(broker, clientId, port);

  return mqttClient;
}

class _RouteCheckState extends State<RouteCheck> {
  final TextEditingController textController = TextEditingController();
  Map<String, bool> buttonStates = {};
  final MqttServerClient mqttClient = createRandomMqttClient('137.184.86.135', 1883);

  @override
  void initState() {
    super.initState();
    initializeButtonStates();
    _connectToMQTT();
  }

  void initializeButtonStates() {
    buttonStates = {
      'Coin Selector': false,
      'Motherboard': false,
      'Joystick': false,
      'Claw': false,
      'Lights': false,
      'Other': false,
      'Showcase': false,
      'Crystals': false,
      'Cabinet': false,
      'Acrylics/Stickers': false,
      'Other Cleaning': false,
    };
  }

  void _connectToMQTT() async {
    try {
      await mqttClient.connect();
    } catch (e) {
      print('Error al conectarse a MQTT: $e');
    }
  }

  List<int> generateSelectionMatrix(Map<String, bool> buttonStates) {
    final optionValues = {
      'Coin Selector': [5, 9],
      'Motherboard': [7, 11],
      'Joystick': [8, 10],
      'Claw': [18, 17],
      'Lights': [20, 19],
      'Other': [1],  // 'Other' solo toma un valor
      // Agrega aquí las demás opciones si las hay
    };

    List<int> selectionMatrix = [];

    for (var entry in optionValues.entries) {
      final isSelected = buttonStates[entry.key] ?? false;
      if (isSelected) {
        selectionMatrix.addAll(List.filled(entry.value.length, 0));
      } else {
        selectionMatrix.addAll(entry.value);
      }
    }

    return selectionMatrix;
  }

  void enviarDatosMQTT() {
    final selectionMatrix = generateSelectionMatrix(buttonStates);

    final message = [
      widget.userEmail,
      widget.qrId,
      selectionMatrix.toString(),
    ];

    final formattedMessage = '{${message.join(', ')}}';

    final builder = MqttClientPayloadBuilder();
    builder.addString(formattedMessage);
    final payload = builder.payload;

    if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
      mqttClient.publishMessage('users/route', MqttQos.atMostOnce, payload!);
      Fluttertoast.showToast(
        msg: 'Datos enviados a MQTT',
        toastLength: Toast.LENGTH_SHORT,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: Colors.green,
        textColor: Colors.white,
        fontSize: 16.0,
      );
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => RouteStock(userEmail: widget.userEmail,qrId: widget.qrId,),),); 
      
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
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 20),
                const Text(
                  'Code Checklist',
                  style: TextStyle(
                    fontSize: 40,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Functional',
                  style: TextStyle(
                    fontSize: 30,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 20),
                // Button pairs for 'Functional' options
                ...buttonStates.keys.take(6).map((String key) => ButtonPair(
                  text: key,
                  buttonStates: buttonStates,
                  updateButtonState: _updateButtonState,
                )).toList(),
                const Text(
                  'Cleaning',
                  style: TextStyle(
                    fontSize: 30,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                // Button pairs for 'Cleaning' options
                ...buttonStates.keys.skip(6).map((String key) => ButtonPair(
                  text: key,
                  buttonStates: buttonStates,
                  updateButtonState: _updateButtonState,
                )).toList(),
                const SizedBox(height: 20),
                TextField(
                  controller: textController,
                  decoration: const InputDecoration(
                    labelText: 'Observations',
                    labelStyle: TextStyle(color: Colors.white),
                    enabledBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                  style: const TextStyle(color: Colors.white),
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: enviarDatosMQTT,
                  child: const Text('Send'),
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: Colors.blue,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _updateButtonState(String text, bool value) {
    setState(() {
      buttonStates[text] = value;
    });
  }
}

class ButtonPair extends StatefulWidget {
  final String text;
  final Map<String, bool> buttonStates;
  final Function(String, bool) updateButtonState;

  ButtonPair({required this.text, required this.buttonStates, required this.updateButtonState});

  @override
  _ButtonPairState createState() => _ButtonPairState();
}

class _ButtonPairState extends State<ButtonPair> {
  bool isCheckButtonPressed = false;
  bool isCloseButtonPressed = false;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      child: Row(
        children: [
          Expanded(
            child: Text(
              widget.text,
              style: const TextStyle(color: Colors.white, fontSize: 20),
            ),
          ),
          GestureDetector(
            onTap: () {
              setState(() {
                isCheckButtonPressed = !isCheckButtonPressed;
                isCloseButtonPressed = false;
                widget.updateButtonState(widget.text, isCheckButtonPressed);
              });
            },
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 10),
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: isCheckButtonPressed ? Colors.white : Colors.grey,
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Icon(
                  Icons.check,
                  color: isCheckButtonPressed ? Colors.red : Colors.white,
                  size: 30,
                ),
              ),
            ),
          ),
          GestureDetector(
            onTap: () {
              setState(() {
                isCloseButtonPressed = !isCloseButtonPressed;
                isCheckButtonPressed = false;
                widget.updateButtonState(widget.text, !isCloseButtonPressed);
              });
            },
            child: Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: isCloseButtonPressed ? Colors.white : Colors.grey,
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Icon(
                  Icons.close,
                  color: isCloseButtonPressed ? Colors.red : Colors.white,
                  size: 30,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
