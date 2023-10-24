import 'package:flutter/material.dart';
import 'route_stock.dart';

class ButtonPair extends StatefulWidget {
  final String text;

  ButtonPair({required this.text});

  @override
  _ButtonPairState createState() => _ButtonPairState();
}

class _ButtonPairState extends State<ButtonPair> {
  bool isCheckButtonPressed = false;
  bool isCloseButtonPressed = false;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            widget.text,
            style: const TextStyle(color: Colors.white, fontSize: 20),
          ),
          Row(
            children: [
              GestureDetector(
                onTap: () {
                  setState(() {
                    isCheckButtonPressed = !isCheckButtonPressed;
                    isCloseButtonPressed = false;
                    buttonStates[widget.text] = isCheckButtonPressed;
                  });
                },
                child: Container(
                  margin: const EdgeInsets.symmetric(horizontal: 10),
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: isCheckButtonPressed ? Colors.white : Colors.grey,
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Icon(
                      Icons.check,
                      color: isCheckButtonPressed ? Colors.red : Colors.white,
                      size: 30,
                    ),
                  ),
                ),
              ),
              GestureDetector(
                onTap: () {
                  setState(() {
                    isCloseButtonPressed = !isCloseButtonPressed;
                    isCheckButtonPressed = false;
                    buttonStates[widget.text] = !isCloseButtonPressed;
                  });
                },
                child: Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: isCloseButtonPressed ? Colors.white : Colors.grey,
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Icon(
                      Icons.close,
                      color: isCloseButtonPressed ? Colors.red : Colors.white,
                      size: 30,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

Map<String, bool> buttonStates = {};

class RouteCheck extends StatelessWidget {
  final TextEditingController textController = TextEditingController();

  RouteCheck({super.key});

  void _navigateToRouteStock(BuildContext context) {
    bool allButtonsSelected = buttonStates.values.every((value) => value == true);

    if (!allButtonsSelected) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Error'),
            content: const Text('Por favor, asegúrate de que todos los checks estén seleccionados.'),
            actions: [
              ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text('OK'),
              ),
            ],
          );
        },
      );
    } else {
      buttonStates.forEach((key, value) {
        print('Option: $key, Checked: $value');
      });

      print('Textfield Content: ${textController.text}');

      // Navegar a la página RouteStock
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => RouteStock()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(60),
          child: Column(
            children: [
              const Text(
                'Code Checklist',
                style: TextStyle(
                  fontSize: 40,
                  color: Color.fromARGB(255, 0, 0, 0),
                  fontFamily: 'Cabin',
                ),
              ),
              const SizedBox(height: 20),
              const Text(
                'Functional',
                style: TextStyle(
                  fontSize: 30,
                  color: Color.fromARGB(255, 0, 0, 0),
                  fontFamily: 'Cabin',
                ),
              ),
              const SizedBox(height: 20),
              ButtonPair(text: 'Coin Selector'),
              ButtonPair(text: 'Claw'),
              ButtonPair(text: 'Joystick'),
              ButtonPair(text: 'Lights'),
              ButtonPair(text: 'Other'),
              const Text(
                'Cleaning',
                style: TextStyle(
                  fontSize: 30,
                  color: Color.fromARGB(255, 0, 0, 0),
                  fontFamily: 'Cabin',
                ),
              ),
              const SizedBox(height: 20),
              ButtonPair(text: 'Cleaning'),
              ButtonPair(text: 'Showcase'),
              ButtonPair(text: 'Crystals'),
              ButtonPair(text: 'Cabinet'),
              ButtonPair(text: 'Acrylics/Stickers'),
              ButtonPair(text: 'Other'),
              const SizedBox(height: 20),
              const Text(
                'Observations',
                style: TextStyle(
                  fontSize: 30,
                  color: Color.fromARGB(255, 0, 0, 0),
                  fontFamily: 'Cabin',
                ),
              ),
              const SizedBox(height: 20),
              TextField(
                controller: textController,
                decoration: const InputDecoration(
                  labelText: 'Observations',
                  labelStyle: TextStyle(color: Colors.white),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                ),
                style: const TextStyle(color: Colors.white),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  bool allButtonsSelected = buttonStates.values.every((value) => value == true);

                  if (allButtonsSelected) {
                    _navigateToRouteStock(context);
                  } else {
                    showDialog(
                      context: context,
                      builder: (BuildContext context) {
                        return AlertDialog(
                          title: const Text('Error'),
                          content: const Text('Por favor, asegúrate de que todos los checks estén seleccionados.'),
                          actions: [
                            ElevatedButton(
                              onPressed: () {
                                Navigator.of(context).pop();
                              },
                              child: const Text('OK'),
                            ),
                          ],
                        );
                      },
                    );
                  }
                },
                child: const Text('Send'),
                style: ElevatedButton.styleFrom(
                  foregroundColor: Colors.white,
                  backgroundColor: Colors.blue,
                ),
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
    home: RouteCheck(),
    debugShowCheckedModeBanner: false,
  ));
}
