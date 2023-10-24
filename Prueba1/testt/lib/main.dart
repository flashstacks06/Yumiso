import 'package:flutter/material.dart';
//import 'Imagenes.dart';
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
      debugShowCheckedModeBanner: false,
      routes: {
        '/pagina2': (context) => const PaginaDos(),
        //'/pagina3': (context) => const Imagenes(),
      },
    );
  }
}

/// The `MyHomePage` class is a stateless widget that represents the home page of an app, with an app
/// bar and three buttons to navigate to different pages.
class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: ListView( // Usamos un ListView para permitir desplazamiento si el contenido es demasiado grande
          children: [
            SizedBox(
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height - MediaQuery.of(context).padding.top,
              child: Align(
                alignment: Alignment.topCenter,
                child: Padding(
                  padding: const EdgeInsets.only(top: 10.0), // Ajusta el espaciado desde SafeArea
                  child: Image.asset(
                    'img/Logo.png',
                    height: 70,
                    width: 70,
                  ),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: TextField(
                decoration: InputDecoration(
                  labelText: 'Nombre',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: TextField(
                decoration: InputDecoration(
                  labelText: 'Correo electrónico',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(
              height: 50,
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  // Procesar los datos ingresados
                },
                child: Text('Enviar'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
