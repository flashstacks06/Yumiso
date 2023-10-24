import 'package:flutter/material.dart';

class RouteStock extends StatelessWidget {
  const RouteStock({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      appBar: AppBar(
        title: const Text('Stock Route'),
      ),
      body: const Center(
        child: Text('Esta es la página de Stock'),
      ),
    );
  }
}
