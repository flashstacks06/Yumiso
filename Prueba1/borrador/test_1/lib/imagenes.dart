import 'package:flutter/material.dart';

class Imagenes extends StatelessWidget {
  const Imagenes({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Imagenes'),
      ),
      body: Center(
        child: Container(
          color: Colors.blue, // Cambiar el color de fondo
          child: Transform.translate(
            offset: const Offset(50, 50), // Cambiar la posición en x y y
            child: Image.asset(
              'images/IMG_2276.png', // Ruta de la imagen
              height: 200, // Cambiar el tamaño de la imagen
              width: 200,
            ),
          ),
        ),
      ),
    );
  }
}