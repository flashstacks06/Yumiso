import 'dart:async';
import 'package:flutter/material.dart';
import 'route_moneybag.dart'; // Asegúrate de tener esta ruta y página definidas en tu proyecto

class RouteStock extends StatefulWidget {
  final String userEmail;
  final String qrId;

  RouteStock({Key? key, required this.userEmail, required this.qrId}) : super(key: key);

  @override
  _RouteStockState createState() => _RouteStockState();
}

class _RouteStockState extends State<RouteStock> {
  final List<TextEditingController> stockTextControllers = List.generate(5, (_) => TextEditingController());
  final List<TextEditingController> refillTextControllers = List.generate(5, (_) => TextEditingController());
  final List<int> stockIndices = [14, 15, 16, 21, 22]; // Índices fijos para stock y refill

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              const SizedBox(height: 16.0),
              buildHeader('Stock And Refill'),
              buildSection('Stock', stockTextControllers, context, stockIndices),
              buildSection('Refill', refillTextControllers, context, stockIndices),
              buildSendButton(widget.userEmail, widget.qrId),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildHeader(String title) {
    return Container(
      alignment: Alignment.center,
      child: Text(
        title,
        style: const TextStyle(fontSize: 36, color: Colors.white, fontFamily: 'Cabin'),
      ),
    );
  }

  Widget buildSection(String title, List<TextEditingController> controllers, BuildContext context, List<int> indices) {
    return Column(
      children: <Widget>[
        Container(
          alignment: Alignment.center,
          child: Text(
            title,
            style: const TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
          ),
        ),
        const SizedBox(height: 20),
        StreamBuilder<List<Widget>>(
          stream: getImages(context, controllers, indices),
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
        const SizedBox(height: 30),
      ],
    );
  }

  Widget buildSendButton(String userEmail, String qrId) {
    return ElevatedButton(
      onPressed: () {
        final stockValues = getCombinedValues(stockTextControllers, stockIndices);
        final refillValues = getCombinedValues(refillTextControllers, stockIndices);
        final combinedValues = [...stockValues, ...refillValues];
        print('Valores combinados: $combinedValues');
        print('Correo: $userEmail'); // Imprimir correo
        print('ID: $qrId'); // Imprimir ID
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => MoneybagPage(userEmail: widget.userEmail,qrId: widget.qrId,combinedValues:combinedValues,),),
        );
      },
      child: const Text('Send'),
    );
  }

  Stream<List<Widget>> getImages(BuildContext context, List<TextEditingController> controllers, List<int> indices) async* {
    List<Widget> images = [];
    double imageSize = MediaQuery.of(context).size.width * 0.3;

    for (var i = 0; i < indices.length; i++) {
      String imagePath = 'img/mod${(i % 5) + 1}.jpg'; // Utiliza imágenes del mod1.jpg al mod5.jpg cíclicamente
      final image = Container(
        decoration: BoxDecoration(border: Border.all(color: Colors.black, width: 2)),
        child: Image.asset(
          imagePath,
          fit: BoxFit.cover,
          height: imageSize,
          width: imageSize,
        ),
      );

      final title = Text(
        'Mod ${indices[i]}',
        style: const TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'Cabin'),
        textAlign: TextAlign.center,
      );

      final numberEntry = Container(
        width: 65,
        height: 40,
        margin: const EdgeInsets.only(top: 10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
        ),
        child: TextField(
          controller: controllers[i],
          keyboardType: TextInputType.number,
          textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 16, color: Colors.black),
          decoration: const InputDecoration(border: InputBorder.none),
        ),
      );

      images.add(Column(
        children: [image, const SizedBox(height: 10), title, numberEntry, const SizedBox(height: 20)],
      ));
    }
    yield images;
  }

  List<String> getCombinedValues(List<TextEditingController> controllers, List<int> indices) {
    return indices.asMap().entries.map((entry) {
      final index = entry.key;
      final fixedIndex = entry.value;
      final text = controllers[index].text;
      return '$fixedIndex:${int.tryParse(text) ?? 0}';
    }).toList();
  }
}
