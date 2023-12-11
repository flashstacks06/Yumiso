import 'package:flutter/material.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

// Importa tus otras pantallas aquí
import 'segunda.dart';
import 'intro_screen.dart'; 
import 'route_check.dart';
import 'arcade_first.dart';
import 'manteinance.dart';

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
        '/pagina2': (context) => const PaginaDos(),
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
  String? management;
  String? errorMessage;

  void login() async {
    final username = usernameController.text;
    final password = passwordController.text;

    if (username.isEmpty || password.isEmpty || management == null) {
      setState(() {
        errorMessage =
            'Por favor, completa todos los campos y selecciona una opción de gestión.';
      });
      return;
    }

    final encryptedUsername = encryptData(username);
    final encryptedPassword = encryptData(password);

    await enviarDatosMQTT(encryptedUsername, encryptedPassword);

    // Navegar a la página correspondiente
    Widget pageToNavigate;
    switch (management) {
      case 'Route':
        pageToNavigate = RouteCheck();
        break;
      case 'Maintenance':
        pageToNavigate = Manteinance1();
        break;
      case 'Arcade':
        pageToNavigate = Arcade1();
        break;
      default:
        pageToNavigate = Container();
    }
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => pageToNavigate),
    );
  }

String encryptData(String data) {
  final key = encrypt.Key.fromBase64('O1GqAK5igRS-BTYgSVLBvg=='); // Usa la clave generada aquí
  final iv = encrypt.IV.fromBase64('v0kiTpvIvAN1IoFQNyB1IQ=='); // Usa el IV generado aquí
  final encrypter = encrypt.Encrypter(encrypt.AES(key, mode: encrypt.AESMode.cbc));
  final encrypted = encrypter.encrypt(data, iv: iv);
  return encrypted.base64;
}


  Future<void> enviarDatosMQTT(String username, String password) async {
    final client = MqttServerClient('137.184.86.135', '1883'); // Reemplaza con tu broker

    try {
      await client.connect();
    } catch (e) {
      print('Error al conectar con el broker MQTT: $e');
      return;
    }

    if (client.connectionStatus!.state == MqttConnectionState.connected) {
      print('Cliente MQTT conectado');
      final builder = MqttClientPayloadBuilder();
      builder.addString('$username:$password');

      client.publishMessage(
        'users', // Reemplaza con tu tópico
        MqttQos.atLeastOnce,
        builder.payload!,
      );
    } else {
      print('Error al conectarse al broker MQTT');
    }

    client.disconnect();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                Center(
                  child: Image.asset(
                    'img/Logo.png',
                    height: 70,
                    width: 70,
                  ),
                ),
                const SizedBox(height: 80),
                const Text(
                  'Management',
                  style: TextStyle(
                    fontSize: 20,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 10),
                ConstrainedBox(
                  constraints: const BoxConstraints.tightFor(width: 200,),
                  child: DropdownButtonFormField<String>(
                    isExpanded: true,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Color.fromARGB(255, 0, 0, 0)),
                      ),
                      fillColor: Colors.white,
                      filled: true,
                    ),
                    items: <String>['Route', 'Maintenance', 'Arcade']
                        .map<DropdownMenuItem<String>>((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(
                          value,
                          style: const TextStyle(color: Color.fromARGB(255, 0, 0, 0)),
                        ),
                      );
                    }).toList(),
                    onChanged: (String? newValue) {
                      setState(() {
                        management = newValue;
                      });
                    },
                    hint: const Text(
                      'Select a Management',
                      style: TextStyle(color: Color.fromARGB(255, 0, 0, 0), fontSize: 13),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Username',
                  style: TextStyle(
                    fontSize: 20,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 10),
                ConstrainedBox(
                  constraints: const BoxConstraints.tightFor(width: 200),
                  child: TextField(
                    controller: usernameController,
                    style: const TextStyle(color: Color.fromARGB(255, 0, 0, 0)),
                    decoration: const InputDecoration(
                      hintText: 'Username',
                      hintStyle: TextStyle(color: Color.fromARGB(255, 0, 0, 0)),
                      border: OutlineInputBorder(),
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Color.fromARGB(255, 0, 0, 0)),
                      ),
                      fillColor: Colors.white,
                      filled: true,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Password',
                  style: TextStyle(
                    fontSize: 20,
                    color: Colors.white,
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 10),
                ConstrainedBox(
                  constraints: const BoxConstraints.tightFor(width: 200),
                  child: TextField(
                    controller: passwordController,
                    obscureText: true,
                    style: const TextStyle(color: Color.fromARGB(255, 0, 0, 0)),
                    decoration: const InputDecoration(
                      hintText: 'Password',
                      hintStyle: TextStyle(color: Color.fromARGB(255, 0, 0, 0)),
                      border: OutlineInputBorder(),
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Color.fromARGB(255, 0, 0, 0)),
                      ),
                      fillColor: Colors.white,
                      filled: true,
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                SizedBox(
                  height: 50,
                  width: 200,
                  child: ElevatedButton(
                    onPressed: login,
                    child: const Text('Login'),
                  ),
                ),
                const SizedBox(height: 20),
                if (errorMessage != null)
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(
                      errorMessage!,
                      style: const TextStyle(
                        color: Color.fromARGB(255, 0, 0, 0),
                        fontSize: 20,
                        fontFamily: 'Cabin',
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
