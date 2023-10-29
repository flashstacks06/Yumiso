import 'package:flutter/material.dart';
//import 'Imagenes.dart';
import 'segunda.dart';
import 'intro_screen.dart'; 
import 'route_check.dart';
import 'arcade.dart';
import 'manteinance.dart';

void main() {
  runApp(const MainApp());
}

/// The MainApp class is a StatelessWidget that defines the routes for navigating between different
/// pages in a Flutter application.
class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const SplashScreen(),
      debugShowCheckedModeBanner: false,
      routes: {
        '/pagina2': (context) => const PaginaDos(),
        '/route1': (context) => RouteCheck(),
        '/manteinance1': (context) => Manteinance1(),
        '/arcade1': (context) => const Arcade1(),
        //'/pagina3': (context) => const Imagenes(),
      },
    );
  }
}

/// The `MyHomePage` class is a stateless widget that represents the home page of an app, with an app
/// bar and three buttons to navigate to different pages.

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

  void login() {
    final username = usernameController.text;
    final password = passwordController.text;

    if (username.isEmpty || password.isEmpty || management == null) {
      setState(() {
        errorMessage =
            'Por favor, completa todos los campos y selecciona una opción de gestión.';
      });
    } else {
      print(
          'Management: $management, Username: $username, Password: $password');
      setState(() {
        errorMessage = null;
      });

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
                    color: Color.fromARGB(255, 0, 0, 0),
                    fontFamily: 'Cabin',
                  ),
                ),
                const SizedBox(height: 10),
                ConstrainedBox(
                  constraints: const BoxConstraints.tightFor(width: 200,),
                  child: DropdownButtonFormField<String>(
                    isExpanded: true, // Para ocupar todo el ancho disponible
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Color.fromARGB(255, 0, 0, 0)),
                      ),
                    ),
                    items: <String>['Admin', 'Partner', 'Route', 'Maintenance', 'Arcade']
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
                    color: Color.fromARGB(255, 0, 0, 0),
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
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Password',
                  style: TextStyle(
                    fontSize: 20,
                    color: Color.fromARGB(255, 0, 0, 0),
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

