import 'package:flutter/material.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:convert';

// Importa las páginas a las que necesitas navegar
import 'route_moneybag.dart';

class QRCodeScannerApp_m extends StatefulWidget {
  final String userEmail;
  final String qrId;
  final String combinedValues;

  QRCodeScannerApp_m({
    Key? key, 
    required this.userEmail, 
    required this.qrId,
    required this.combinedValues,
  }) : super(key: key);
  

  @override
  _QRCodeScannerAppState createState() => _QRCodeScannerAppState();
}

class _QRCodeScannerAppState extends State<QRCodeScannerApp_m> {
  late QRViewController _controller;
  final GlobalKey _qrKey = GlobalKey(debugLabel: 'QR');
  String? qrId_m = '0'; 
  TextEditingController _manualIdController = TextEditingController(); // Controlador para el campo de texto manual

  @override
  void dispose() {
    _controller.dispose();
    _manualIdController.dispose(); // Dispose del controlador de texto manual
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Column(
          children: [
            Expanded(
              flex: 5,
              child: Column(
                children: [
                  Expanded(
                    child: QRView(
                      key: _qrKey,
                      onQRViewCreated: _onQRViewCreated,
                      overlay: QrScannerOverlayShape(
                        borderColor: Colors.red,
                        borderRadius: 10,
                        borderLength: 30,
                        borderWidth: 10,
                        cutOutSize: 300,
                      ),
                      onPermissionSet: (ctrl, p) => _onPermissionSet(context, ctrl, p),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: TextField(
                      controller: _manualIdController,
                      decoration: InputDecoration(
                        hintText: 'Ingresa el ID manualmente',
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: _enviarIdBolsa, // Acción del botón para enviar el ID
                    child: Text('Enviar ID de Bolsa'),
                  ),
                ],
              ),
            ),
            Align(
              alignment: Alignment.bottomCenter,
              child: Container(
                margin: EdgeInsets.all(16.0),
                padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16.0),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.5),
                      spreadRadius: 1,
                      blurRadius: 2,
                      offset: Offset(0, 1),
                    ),
                  ],
                ),
                child: Text(
                  'Número de Bolsa: $qrId_m',
                  style: TextStyle(fontSize: 18.0),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    setState(() {
      _controller = controller;
      _controller.scannedDataStream.listen((scanData) {
        final code = scanData.code;
        try {
          final decodedData = json.decode(code!);
          if (decodedData is Map<String, dynamic> &&
              decodedData.containsKey('bag') &&
              decodedData['bag'] is String) {
            qrId_m = decodedData['bag'];
            setState(() {});
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => MoneybagPage(userEmail: widget.userEmail,qrId: widget.qrId, combinedValues: widget.combinedValues,bagid: qrId_m!)),
            );            
          } else {
            print('QR code does not have the expected format.');
          }
        } catch (e) {
          print('Error decoding QR code: $e');
        }
      });
    });
  }

  void _onPermissionSet(BuildContext context, QRViewController ctrl, bool p) {
    if (!p) {
      // Handle permission denied
    }
  }

  void _enviarIdBolsa() {
    // Obtener el ID manualmente ingresado desde el controlador
    final manualId = _manualIdController.text;
    if (manualId.isNotEmpty) {
      setState(() {
        qrId_m = manualId;
      });
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => MoneybagPage(userEmail: widget.userEmail,qrId: widget.qrId, combinedValues: widget.combinedValues,bagid: qrId_m!)),
      );
    }
  }
}
