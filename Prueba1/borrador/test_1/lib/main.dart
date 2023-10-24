import 'package:flutter/material.dart';
import 'Imagenes.dart';
import 'segunda.dart';
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
      home: const MyHomePage(),
      routes: {
        '/pagina2': (context) => const PaginaDos(),
        '/pagina3': (context) => const Imagenes(),
      },
    );
  }
}


/// The `MyHomePage` class is a stateless widget that represents the home page of an app, with an app
/// bar and two buttons to navigate to different pages.
class MyHomePage extends StatelessWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inicio'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/pagina2');
              },
              child: const Text('Ir a la pagina 2'),
            ),ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/pagina3');
              },
              child: const Text('Ir a la pagina 3'),
            ),
          ],
        ),
      ),
    );
  }
}



