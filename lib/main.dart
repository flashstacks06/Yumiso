import 'package:flutter/material.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

// Importa tus otras pantallas aquí
import 'route_check.dart';
import 'arcade_first.dart';
import 'manteinance.dart';
import 'qr_check.dart'; // Asume que tu pantalla de escaneo de QR está en 'qr_check.dart'

void main() {
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
      debugShowCheckedModeBanner: false,
      routes: {
        '/route1': (context) => RouteCheck(),
        '/manteinance1': (context) => Manteinance1(),
        '/arcade1': (context) => const Arcade1(),
      },
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController usernameController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  bool _isLoading = false;
  String? errorMessage;

  void login() async {
    setState(() {
      _isLoading = true;
    });

    final username = usernameController.text;
    final password = passwordController.text;

    if (username.isEmpty || password.isEmpty) {
      setState(() {
        errorMessage = 'Por favor, completa todos los campos.';
        _isLoading = false;
      });
      return;
    }

    final encryptedUsername = encryptData(username);
    final encryptedPassword = encryptData(password);

    await enviarDatosMQTT(encryptedUsername, encryptedPassword);
  }

  String encryptData(String data) {
    final key = encrypt.Key.fromBase64('O1GqAK5igRS-BTYgSVLBvg==');
    final iv = encrypt.IV.fromBase64('v0kiTpvIvAN1IoFQNyB1IQ==');
    final encrypter =
        encrypt.Encrypter(encrypt.AES(key, mode: encrypt.AESMode.cbc));
    final encrypted = encrypter.encrypt(data, iv: iv);
    return encrypted.base64;
  }

  Future<void> enviarDatosMQTT(String username, String password) async {
    final client = MqttServerClient('137.184.86.135', '1883');

    try {
      await client.connect();
    } catch (e) {
      print('Error al conectar con el broker MQTT: $e');
      setState(() {
        _isLoading = false;
      });
      return;
    }

    if (client.connectionStatus!.state == MqttConnectionState.connected) {
      print('Cliente MQTT conectado');
      final builder = MqttClientPayloadBuilder();
      builder.addString('$username:$password');

      client.publishMessage(
        'users',
        MqttQos.atLeastOnce,
        builder.payload!,
      );

      // Suscribirse a un tópico para recibir la respuesta
      const respuestaTopico = 'respuesta';
      client.subscribe(respuestaTopico, MqttQos.atLeastOnce);

      client.updates!.listen((List<MqttReceivedMessage<MqttMessage>> c) {
        final MqttPublishMessage message = c[0].payload as MqttPublishMessage;
        final payload =
            MqttPublishPayload.bytesToStringAsString(message.payload.message);

        _navegarSegunRespuesta(payload);
      });
    } else {
      print('Error al conectarse al broker MQTT');
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _navegarSegunRespuesta(String respuesta) {
    setState(() {
      _isLoading = false;
    });

    switch (respuesta) {
      case 'Route':
      case 'Maintenance':
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => QRCodeScannerApp(mqttResponse: respuesta),
          ),
        );
        break;
      case 'Arcade':
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Arcade1()),
        );
        break;
      default:
        print('Respuesta MQTT no reconocida');
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: Center(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Image.asset(
                  'img/Logo.png',
                  height: 70,
                  width: 70,
                ),
                const SizedBox(height: 20),
                const Text(
                  'Login',
                  style: TextStyle(
                    fontSize: 28,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 40),
                TextField(
                  controller: usernameController,
                  decoration: InputDecoration(
                    labelText: 'Username',
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: passwordController,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Password',
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                if (_isLoading) CircularProgressIndicator(),
                if (!_isLoading)
                  ElevatedButton(
                    onPressed: login,
                    child: const Text(
                      'Login',
                      style: TextStyle(fontSize: 18),
                    ),
                    style: ElevatedButton.styleFrom(
                      primary: Colors.blue, // Button color
                      onPrimary: Colors.white, // Text color
                      minimumSize: const Size.fromHeight(50),
                    ),
                  ),
                if (errorMessage != null)
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      errorMessage!,
                      style: const TextStyle(
                        color: Colors.red,
                        fontSize: 16,
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
