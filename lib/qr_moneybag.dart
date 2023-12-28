import 'package:flutter/material.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:convert';

// Importa las páginas a las que necesitas navegar
import 'route_moneybag.dart';

// Asegúrate de que estas importaciones coincidan con los nombres de archivo y clase en tu proyecto

class QRCodeScannerApp_m extends StatefulWidget {
  final String userEmail;    // Correo electrónico del usuario
  final String qrId;
  final String combinedValues;

  QRCodeScannerApp_m({Key? key, 
  required this.userEmail, 
  required this.qrId,
  required this.combinedValues}) : super(key: key);
  

  @override
  _QRCodeScannerAppState createState() => _QRCodeScannerAppState();
}

class _QRCodeScannerAppState extends State<QRCodeScannerApp_m> {
  late QRViewController _controller;
  final GlobalKey _qrKey = GlobalKey(debugLabel: 'QR');
  String? qrId_m = '0'; // Variable para almacenar el número de ID del código QR
  //late String bagid;

  @override
  void dispose() {
    _controller.dispose();
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
            print('ID Moneybag: $qrId_m');
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
}
