import 'dart:math';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

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
    // Inicializa las opciones con valores predeterminados (falsos)
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

  void enviarDatosMQTT() {
    final List<int> selectionMatrix = buttonStates.values.map((value) => value ? 1 : 0).toList();

    final message = {
      widget.userEmail,
      widget.qrId,
      selectionMatrix.toString(),
    };

    final builder = MqttClientPayloadBuilder();
    builder.addString(message.toString());

    final payload = builder.payload;

    if (mqttClient.connectionStatus!.state == MqttConnectionState.connected) {
      mqttClient.publishMessage('users/route', MqttQos.atMostOnce, payload!);
      print('Datos enviados a MQTT');
    } else {
      print('Error: No se pudo enviar datos a MQTT porque la conexión no está activa.');
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
                ButtonPair(text: 'Coin Selector', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Motherboard', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Joystick', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Claw', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Lights', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Other', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                const Text(
                  'Cleaning',
                  style: TextStyle(
                    fontSize: 30,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 20),
                ButtonPair(text: 'Showcase', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Crystals', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Cabinet', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Acrylics/Stickers', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                ButtonPair(text: 'Other Cleaning', buttonStates: buttonStates, updateButtonState: _updateButtonState),
                const SizedBox(height: 20),
                const Text(
                  'Observations',
                  style: TextStyle(
                    fontSize: 30,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
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
                  onPressed: () {
                    bool allButtonsSelected = buttonStates.values.any((value) => value);

                    if (allButtonsSelected) {
                      enviarDatosMQTT();
                      mostrarAlerta('Datos enviados', 'Los datos se han enviado correctamente.');
                    } else {
                      mostrarAlerta('Error', 'Por favor, selecciona al menos una opción.');
                    }
                  },
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

  // Función para actualizar el estado del botón
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

