import 'dart:async';
import 'package:flutter/material.dart';
import 'route_moneybag.dart';

class RouteStock extends StatelessWidget {
  const RouteStock({Key? key});

  Stream<List<Widget>> getImages(BuildContext context, String type) async* {
    List<Widget> images = [];
    double imageSize = MediaQuery.of(context).size.width * 0.3;

    for (var i = 1; i <= 5; i++) {
      final image = Container(
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black, width: 2), // Marco negro
        ),
        child: Image.asset(
          'img/mod$i.jpg',
          fit: BoxFit.cover,
          height: imageSize,
          width: imageSize,
        ),
      );

      final title = Text(
        'Mod $i',
        style: const TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'Cabin'),
        textAlign: TextAlign.center,
      );

      final numberEntry = Container(
        width: 65,
        height: 40,
        margin: const EdgeInsets.only(top: 10),
        decoration: BoxDecoration(
          color: Colors.white, // Color de fondo blanco
          borderRadius: BorderRadius.circular(8), // Bordes redondeados (ajusta según lo necesites)
        ),
        child: const TextField(
          keyboardType: TextInputType.number,
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 16, color: Colors.black),
          decoration: InputDecoration(
            border: InputBorder.none, // Elimina el borde predeterminado del TextField
          ),
        ),
      );

      images.add(Column(
        children: [
          image,
          const SizedBox(height: 10), //Cambia el espacio del texto de cada imagen
          title,
          numberEntry,
          const SizedBox(height: 20), //Cambia el espacio entre cada fila de imágenes
        ],
      ));

      if (i == 5) {
        yield images;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              const SizedBox(height: 16.0), // Espacio añadido para separar del borde superior
              Container(
                alignment: Alignment.center,
                child: const Text(
                  'Stock And Refill',
                  style: TextStyle(fontSize: 36, color: Colors.white, fontFamily: 'Cabin'),
                ),
              ),
              const SizedBox(height: 20),
              Container(
                alignment: Alignment.center,
                child: const Text(
                  'Stock',
                  style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                ),
              ),
              const SizedBox(height: 20),
              StreamBuilder<List<Widget>>(
                stream: getImages(context, 'Stock'),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return Wrap(
                      spacing: 10.0,
                      runSpacing: 10.0,
                      alignment: WrapAlignment.center,
                      children: snapshot.data!,
                    );
                  } else {
                    return const Center(child: CircularProgressIndicator());
                  }
                },
              ),
              //const SizedBox(height: 30), // Espacio añadido entre grupos de imágenes
              Container(
                alignment: Alignment.center,
                child: const Text(
                  'Refill',
                  style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                ),
              ),
              const SizedBox(height: 30), // Espacio añadido entre grupos de imágenes
              StreamBuilder<List<Widget>>(
                stream: getImages(context, 'Refill'),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return Wrap(
                      spacing: 10.0,
                      runSpacing: 10.0,
                      alignment: WrapAlignment.center,
                      children: snapshot.data!,
                    );
                  } else {
                    return const Center(child: CircularProgressIndicator());
                  }
                },
              ),
              const SizedBox(height: 20), // Espacio añadido después de las imágenes
              ElevatedButton(
                onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const MoneybagPage()),
                    );  
                },
                child: const Text('Send'),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: RouteStock(),
    debugShowCheckedModeBanner: false,
  ));
}
