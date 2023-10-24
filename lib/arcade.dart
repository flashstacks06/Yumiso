import 'package:flutter/material.dart';

class Arcade1 extends StatelessWidget {
  const Arcade1({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.red,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            const Text(
              'Texto a la izquierda',
              style: TextStyle(color: Colors.white),
            ),
            GestureDetector(
              onTap: () {
                // Acción al hacer clic en el botón de palomita
              },
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 10),
                width: 60,
                height: 60,
                decoration: const BoxDecoration(
                  color: Colors.green,
                  shape: BoxShape.circle,
                ),
                child: const Center(
                  child: Icon(
                    Icons.check,
                    color: Colors.white,
                    size: 30,
                  ),
                ),
              ),
            ),
            GestureDetector(
              onTap: () {
                // Acción al hacer clic en el botón de tachita
              },
              child: Container(
                width: 60,
                height: 60,
                decoration: const BoxDecoration(
                  color: Colors.red,
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Icon(
                    Icons.close,
                    color: Colors.white,
                    size: 30,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
