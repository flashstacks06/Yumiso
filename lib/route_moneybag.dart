import 'dart:async';
import 'package:flutter/material.dart';

void main() {
  runApp(MaterialApp(
    home: MoneybagPage(),
    debugShowCheckedModeBanner: false,
  ));
}

class MoneybagPage extends StatefulWidget {
  const MoneybagPage({Key? key}) : super(key: key);

  @override
  State<MoneybagPage> createState() => _MoneybagPageState();
}

class _MoneybagPageState extends State<MoneybagPage> {
  late TextEditingController _timeController;
  late TextEditingController _moneybagController;
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _timeController = TextEditingController(text: _getCurrentTime());   //Actualizo en tiempo real el tiempo
    _moneybagController = TextEditingController(text: '\$1,989');       //Seteo el valor que irá en moneybag

    _timer = Timer.periodic(const Duration(seconds: 1), _updateTime);
  }

  String _getCurrentTime() {
    final now = DateTime.now();
    return '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}';
  }

  void _updateTime(Timer timer) {
    setState(() {
      _timeController.text = _getCurrentTime();
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    _timeController.dispose();
    _moneybagController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  alignment: Alignment.center,
                  child: const Text(
                    'Moneybag',
                    style: TextStyle(fontSize: 36, color: Colors.white, fontFamily: 'Cabin'),
                  ),
                ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    const Text(
                      'MoneyBag',
                      style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                    ),
                    Container(
                      width: 120,
                      height: 40,
                      margin: const EdgeInsets.only(left: 10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: TextField(
                        controller: _moneybagController,
                        enabled: false,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 22, color: Colors.black, fontFamily: 'Cabin'),
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: <Widget>[
                    const Text(
                      'Cut-off-time',
                      style: TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
                    ),
                    Container(
                      width: 120,
                      height: 40,
                      margin: const EdgeInsets.only(left: 10),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: TextField(
                        controller: _timeController,
                        enabled: false,
                        textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 22, color: Colors.black, fontFamily: 'Cabin'),
                        decoration: const InputDecoration(
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 30),
                Container(
                  alignment: Alignment.center,
                  child: ElevatedButton(
                    onPressed: () {
                      // Acción a realizar cuando se presiona el botón "Finish"
                    },
                    child: const Text('Finish'),
                    style: ElevatedButton.styleFrom(
                      primary: Colors.blue,
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
