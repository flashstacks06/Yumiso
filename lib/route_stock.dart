import 'package:flutter/material.dart';

class RouteStock extends StatelessWidget {
  const RouteStock({Key? key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 20),
                child: Text(
                  'Stock And',
                  style: TextStyle(fontSize: 24, color: Colors.white),
                ),
              ),
              const Text(
                'Stock',
                style: TextStyle(fontSize: 16, color: Colors.white),
              ), 
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  for (var i = 1; i <= 5; i += 1)
                    Column(
                      children: [
                        Image.asset(
                          'img/mod$i.jpg',
                          height: 100,
                          width: 100,
                        ),
                        const SizedBox(height: 10),
                        Text(
                          'Mod $i',
                          style: TextStyle(fontSize: 16, color: Colors.white),
                        ),
                      ],
                    ),
                ],
              ),
              SizedBox(height: 20), // Espacio entre las filas de imágenes
              const Text(
                'Refill',
                style: TextStyle(fontSize: 16, color: Colors.white),
              ),              
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  for (var i = 1; i <= 5; i += 1)
                    Column(
                      children: [
                        Image.asset(
                          'img/mod$i.jpg',
                          height: 100,
                          width: 100,
                        ),
                        const SizedBox(height: 10),
                        Text(
                          'Mod $i',
                          style: TextStyle(fontSize: 16, color: Colors.white),
                        ),
                      ],
                    ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
