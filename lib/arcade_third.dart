import 'package:flutter/material.dart';
import 'arcade_fourth.dart';

void main() {
  runApp(const Arcade3());
}

class Arcade3 extends StatelessWidget {
  const Arcade3({super.key});

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
    List<String> textos = [
      'CEDI',
      'Route',
      'General',
      'Super Market',
      'Location',
      'Address',
      'Week',
      'Date',
      'Hour',
      'Cash',
      'Prize'
    ];

    return SafeArea(
      child: Scaffold(
        backgroundColor: const Color.fromARGB(230, 255, 51, 57),
        body: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20), 
              Center(
                child: Text(
                  'BSC Discrepancy Weekly',
                  style: TextStyle(fontSize: 36, fontFamily: 'Cabin', color: Colors.white),
                ),
              ),
              const SizedBox(height: 30),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  scrollDirection: Axis.vertical,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          for (int i = 0; i < 11; i++)
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
                      for (int i = 0; i < 6; i++)
                        Row(
                          children: [
                            for (int j = 0; j < 9; j++)
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
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Center(
                child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => Arcade4()),
                          );                        
                        },
                  child: Text('Send'),
                ),
              ),
            ],
          ),
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
      case 4:
        return [
          'Option 5A',
          'Option 5B',
          'Option 5C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 5:
        return [
          'Option 6A',
          'Option 6B',
          'Option 6C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 6:
        return [
          'Option 7A',
          'Option 7B',
          'Option 7C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 7:
        return [
          'Option 8A',
          'Option 8B',
          'Option 8C',
        ].map((String value) {
          return DropdownMenuItem<String>(
            value: value,
            child: Text(value),
          );
        }).toList();
      case 8:
        return [
          'Option 9A',
          'Option 9B',
          'Option 9C',
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
