import 'package:flutter/material.dart';

void main() {
  runApp(MiPrimeraApp());
}

class MiPrimeraApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Mi Primera App'),
        ),
        body: const Center(
          child: Text(
            'Hola, Mundo!',
            style: TextStyle(fontSize: 24),
          ),
        ),
      ),
    );
  }
}
