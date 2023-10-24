import 'package:flutter/material.dart';

class Imagenes extends StatelessWidget {
  const Imagenes({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Pantalla con Imagen'),
        ),
        body: Image.asset('img/IMG_2276.HEIC'),
      ),
    );
  }
}