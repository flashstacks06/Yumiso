import 'package:flutter/material.dart';

class Manteinance1 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    List<String> titles = ['Coin Selector', 'Motherboard', 'Joystick'];

    List<Widget> widgets = [];

    for (var i = 1; i <= 3; i++) {
      widgets.addAll([
        Column(
          children: [
            Container(
              decoration: BoxDecoration(
                border: Border.all(color: Colors.black, width: 2), // Borde negro
              ),
              child: Image.asset(
                'img/man$i.jpg',
                width: MediaQuery.of(context).size.width * 0.29,
                height: MediaQuery.of(context).size.width * 0.29,
              ),
            ),
            SizedBox(height: 15),
            Text(
              titles[i - 1],
              style: TextStyle(fontSize: 20, fontFamily: 'Cabin', color: Colors.white),
            ),
            SizedBox(height: 10),
          ],
        ),
      ]);
    }

    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Maintenance',
                style: TextStyle(fontSize: 36, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 30),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: widgets.sublist(0, 3),
              ),
              SizedBox(height: 20),
              Text(
                'Repair',
                style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20),
              Text(
                'Part replacement',
                style: TextStyle(fontSize: 28, fontFamily: 'Cabin', color: Colors.white),
              ),
              SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                  Container(
                    width: MediaQuery.of(context).size.width * 0.2,
                    child: TextField(
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                        fillColor: Colors.white,
                        filled: true,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  // Acción a realizar cuando se presiona el botón "Finish"
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
    home: Manteinance1(),
    debugShowCheckedModeBanner: false,
  ));
}
