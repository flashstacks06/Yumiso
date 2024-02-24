import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart' as mqtt;
import 'package:mqtt_client/mqtt_server_client.dart';
import 'dart:convert';
import 'package:uuid/uuid.dart';


class Routestock2 extends StatefulWidget {

  final String userEmail;
  final String qrId;

  Routestock2({Key? key, required this.userEmail, required this.qrId}) : super(key: key);

  @override
  _MqttDataTablePageState createState() => _MqttDataTablePageState();
}

class _MqttDataTablePageState extends State<Routestock2> {
  List<Map<String, dynamic>> data = [];
  late MqttServerClient client;
  final String server = '137.184.86.135';
  late String clientIdentifier;

  @override
  void initState() {
    super.initState();
    _initializeMqttClient();
  }

  void _initializeMqttClient() async {
    var uuid = Uuid();
    clientIdentifier = uuid.v4();

    client = MqttServerClient.withPort(server, clientIdentifier, 1883);
    client.keepAlivePeriod = 60;
    client.onDisconnected = _onDisconnected;

    try {
      await client.connect();
      print('Cliente MQTT conectado con ID $clientIdentifier');
      _sendMessage();
      client.subscribe('productos_$clientIdentifier', mqtt.MqttQos.atLeastOnce);
      client.updates!.listen(_onMessage);
    } catch (e) {
      print('Error en la conexión MQTT: $e');
      client.disconnect();
    }
  }

  void _sendMessage() {
    final builder = mqtt.MqttClientPayloadBuilder();
    builder.addString('productos_$clientIdentifier');
    client.publishMessage('producto', mqtt.MqttQos.atLeastOnce, builder.payload!);
  }

  void _onDisconnected() {
    print('Cliente MQTT desconectado');
    client.disconnect();
  }

  void _onMessage(List<mqtt.MqttReceivedMessage<mqtt.MqttMessage>> event) {
    final mqtt.MqttPublishMessage recMess = event[0].payload as mqtt.MqttPublishMessage;
    final String message = mqtt.MqttPublishPayload.bytesToStringAsString(recMess.payload.message);

    List<dynamic> newEntries = json.decode(message);
    newEntries.sort((a, b) => (a['product_id'] ?? 0).compareTo(b['product_id'] ?? 0));

    setState(() {
      data = newEntries.cast<Map<String, dynamic>>();
    });
    }

  Future<void> _onRefresh() async {
    _sendMessage();
    await Future.delayed(const Duration(seconds: 2)); // Simula un retraso
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(230, 255, 51, 57),
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _onRefresh,
          child: SingleChildScrollView(
            child: Column(
              children: <Widget>[
                const SizedBox(height: 16.0),
                const Padding(
                  padding: EdgeInsets.all(16.0),
                  child: Text(
                    'Stock and Refill',
                    style: TextStyle(fontSize: 32, color: Colors.white, fontFamily: 'Cabin'),
                  ),
                ),
                buildSection('Stock', data),
                const SizedBox(height: 40),
                buildSection('Refill', data),
                const SizedBox(height: 20),
                const Padding(
                  padding: EdgeInsets.all(16.0),              
                ),
                const SizedBox(height: 30),
                ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: Colors.blue,
                  ),
                  child: const Text('Enviar')
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget buildSection(String title, List<Map<String, dynamic>> data) {
    return Column(
      children: <Widget>[
        Container(
          alignment: Alignment.center,
          padding: EdgeInsets.all(16.0),
          child: Text(
            title,
            style: const TextStyle(fontSize: 28, color: Colors.white, fontFamily: 'Cabin'),
          ),
        ),
        const SizedBox(height: 20),
        ListView.builder(
          shrinkWrap: true,
          physics: NeverScrollableScrollPhysics(),
          itemCount: (data.length / 2).ceil(), // Adjust the item count
          itemBuilder: (context, index) {
            // Calculate the actual index of the data list
            int dataIndex = index * 2; // Multiply index by 2
            final product1 = data[dataIndex];
            final product2 = dataIndex + 1 < data.length ? data[dataIndex + 1] : null;

            return Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                buildProduct(product1),
                product2 != null ? buildProduct(product2) : SizedBox(width: 130), // Keep space for symmetry
              ],
            );
          },
        ),
      ],
    );
  }


  Widget buildProduct(Map<String, dynamic> product) {
    final String productName = product['product_name'] ?? '';
    final String productType = product['product_type'] ?? '';
    final dynamic productImage = product['product_image'];
  
    String imageUrl;
    if (productImage is String && productImage.isNotEmpty) {
      imageUrl = 'http://137.184.86.135/${productName.replaceAll(' ', '_')}.png';
    } else {
      imageUrl = 'http://137.184.86.135/blanco.png';
    }
  
    final image = Container(
      decoration: BoxDecoration(border: Border.all(color: Colors.black, width: 2)),
      child: Image.network(
        imageUrl,
        fit: BoxFit.cover,
        width: 130,
        height: 130,
      ),
    );
  
    final title = Text(
      productName,
      style: const TextStyle(fontSize: 16, color: Colors.white, fontFamily: 'Cabin'),
      textAlign: TextAlign.center,
    );
  
    final inputKey = productType == 'Stock' ? 'stockInput' : 'refillInput';
    final currentValue = product[inputKey] ?? '0';
  
    final inputField = Container(
      width: 50,
      height: 30,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black, width: 1),
        borderRadius: BorderRadius.circular(5),
      ),
      child: TextFormField(
        initialValue: currentValue.toString(),
        keyboardType: TextInputType.number,
        textAlign: TextAlign.center,
        style: TextStyle(color: Colors.white),
        onChanged: (value) {
          setState(() {
            product[inputKey] = value;
          });
        },
      ),
    );
  
    return Column(
      children: [image, const SizedBox(height: 10), title, const SizedBox(height: 10), inputField, const SizedBox(height: 20)],
    );
  }


  @override
  void dispose() {
    client.disconnect();
    super.dispose();
  }
}
