import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const RedPage(),
    );
  }
}

class RedPage extends StatelessWidget {
  const RedPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: Column(
          //mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const SizedBox(height: 16.0), // Espacio añadido para separar del borde superior
            Container(
              alignment: Alignment.center,
              child: const Text(
                'Qr Scan',
                style: TextStyle(fontSize: 36, color: Colors.white, fontFamily: 'Cabin'),
              ),
            ),  
            const SizedBox(height: 30.0),
            Container(
              width: 100, // Tamaño de la imagen
              height: 100, // Tamaño de la imagen
              color: Colors.white, // Color de fondo del contenedor de la imagen
              child: Center(
                child: Image.asset(
                  'img/qrcode.png', // Reemplaza con la ruta de tu imagen
                  width: 150, // Tamaño de la imagen
                  height: 150, // Tamaño de la imagen
                ),
              ),
            ),
            const SizedBox(height: 20), // Espacio entre la imagen y el botón
            ElevatedButton(
              onPressed: () {
                // Acción cuando se presiona el botón
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue, // Color del botón
              ),
              child: const Text('Next', style: TextStyle(color: Colors.white)),
            ),
          ],
        ),
      ),
    );
  }
}
