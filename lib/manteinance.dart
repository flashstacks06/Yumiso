import 'package:flutter/material.dart';

class Maintenance1 extends StatefulWidget {
  @override
  _Maintenance1State createState() => _Maintenance1State();
}

class _Maintenance1State extends State<Maintenance1> {
  List<bool> repairChecked = List.generate(3, (index) => false);
  List<bool> partReplacementChecked = List.generate(3, (index) => false);
  List<int> selectionMatrix = List.generate(6, (index) => 0);

  Widget largeCheckbox(bool value, ValueChanged<bool?> onChanged, int index, String category) {
    return Transform.scale(
      scale: 2.0,
      child: Checkbox(
        value: value,
        onChanged: onChanged,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    List<String> titles = ['Coin Selector', 'Motherboard', 'Joystick'];

    List<Widget> repairWidgets = [];
    List<Widget> partReplacementWidgets = [];
    List<Widget> images = [];

    for (var i = 0; i < 3; i++) {
      images.add(
        Column(
          children: [
            Image.asset(
              'img/man${i + 1}.jpg',
              width: MediaQuery.of(context).size.width * 0.3,
              height: MediaQuery.of(context).size.width * 0.3,
            ),
            SizedBox(height: 8),
            Text(
              titles[i],
              style: TextStyle(fontSize: 18, fontFamily: 'Cabin', color: Colors.white),
            ),
          ],
        ),
      );

      repairWidgets.add(
        Column(
          children: [
            largeCheckbox(
              repairChecked[i],
              (value) {
                setState(() {
                  repairChecked[i] = value!;
                  int repairValue;
                  switch (i) {
                    case 0: repairValue = 9; break;
                    case 1: repairValue = 11; break;
                    case 2: repairValue = 10; break;
                    default: repairValue = 0; break;
                  }
                  selectionMatrix[i] = value ? repairValue : 0;
                });
              },
              i,
              'Repair',
            ),
          ],
        ),
      );

      partReplacementWidgets.add(
        Column(
          children: [
            largeCheckbox(
              partReplacementChecked[i],
              (value) {
                setState(() {
                  partReplacementChecked[i] = value!;
                  int replacementValue;
                  switch (i) {
                    case 0: replacementValue = 5; break;
                    case 1: replacementValue = 7; break;
                    case 2: replacementValue = 8; break;
                    default: replacementValue = 0; break;
                  }
                  selectionMatrix[i + 3] = value ? replacementValue : 0;
                });
              },
              i,
              'Part Replacement',
            ),
          ],
        ),
      );
    }

    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16.0),
          child: Column(
            children: [
              Text(
                'Maintenance',
                style: TextStyle(fontSize: 36, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 30),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: images,
              ),
              SizedBox(height: 20),
              Text(
                'Repair',
                style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: repairWidgets,
              ),
              Text(
                'Part Replacement',
                style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: partReplacementWidgets,
              ),
              ElevatedButton(
                onPressed: () {
                  // Acción a realizar cuando se presiona el botón "Finish"
                  print(selectionMatrix);
                },
                child: Text('Finish'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: Maintenance1(),
    debugShowCheckedModeBanner: false,
  ));
}
