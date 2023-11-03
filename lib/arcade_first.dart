import 'package:flutter/material.dart';

void main() {
  runApp(const Arcade1());
}

class Arcade1 extends StatelessWidget {
  const Arcade1({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const ScrollableGrid(),
    );
  }
}

class ScrollableGrid extends StatelessWidget {
  const ScrollableGrid({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    List<String> textos = ['CEDI', 'Route', 'Week', 'Moneybag', 'Money-count'];

    return SafeArea(  
      child: Scaffold(
        backgroundColor: const Color.fromARGB(230, 255, 51, 57),
        body: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 20), // Espacio entre el título y los elementos
            Center(
              child: Text(
                'Arcade',
                style: TextStyle(fontSize: 36, fontFamily: 'Cabin', color: Colors.white),
              ),
            ),
            const SizedBox(height: 30), // Espacio entre el título y los elementos
            Center(
              child: Container(
                width: 150, // Ajusta el ancho del contenedor
                height: 50, // Ajusta el alto del contenedor
                child: TextField(
                  readOnly: true,
                  controller: TextEditingController(text: 'CEDI PUE'),
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    prefixStyle: TextStyle(fontWeight: FontWeight.bold),
                    contentPadding: EdgeInsets.symmetric(horizontal: 10),
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            const SizedBox(height: 30),
            SingleChildScrollView(
              scrollDirection: Axis.vertical,
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center, 
                      children: [
                        for (int i = 0; i < 5; i++)
                          SizedBox(
                            width: 200,
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center, 
                              children: [
                                Text(
                                  textos[i],
                                  style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 10),
                              ],
                            ),
                          ),
                      ],
                    ),
                    for (int i = 0; i < 3; i++)
                      Row(
                        children: [
                          for (int j = 0; j < 4; j++)
                            Column(
                              children: [
                                SizedBox(
                                  height: 100, 
                                  width: 200,
                                  child: DropdownButtonFormField<String>(
                                    items: getDropdownOptions(j),
                                    onChanged: (String? newValue) {
                                      // Handle value change
                                    },
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      contentPadding: EdgeInsets.symmetric(horizontal: 10),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 20),
                          SizedBox(
                            height: 100,
                            width: 200,
                            child: TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Enter text',
                                contentPadding: const EdgeInsets.symmetric(horizontal: 10),
                              ),
                            ),
                          ),
                        
                        ],
                        
                      ),
                      const SizedBox(height: 20),
                  ],
                ),
              ),
            ),
            Center(
                      child: ElevatedButton(
                        onPressed: () {
                          // Lógica cuando se presiona el botón "Send"
                        },
                        child: Text('Send'),
                      ),
                    ),
                  ],
                ),
              ),
            );
          }

  List<DropdownMenuItem<String>> getDropdownOptions(int columnIndex) {
    switch (columnIndex) {
      case 0:
        return [
          'Option 1A',
          'Option 1B',
          'Option 1C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 1:
        return [
          'Option 2A',
          'Option 2B',
          'Option 2C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 2:
        return [
          'Option 3A',
          'Option 3B',
          'Option 3C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 3:
        return [
          'Option 4A',
          'Option 4B',
          'Option 4C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      default:
        return [];
    }
  }
}
