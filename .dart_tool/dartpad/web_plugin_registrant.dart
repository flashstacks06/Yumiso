// Flutter web plugin registrant file.
//
// Generated file. Do not edit.
//

// @dart = 2.13
// ignore_for_file: type=lint

import 'package:camera_web/camera_web.dart';
import 'package:fluttertoast/fluttertoast_web.dart';
import 'package:mobile_scanner/mobile_scanner_web_plugin.dart';
import 'package:flutter_web_plugins/flutter_web_plugins.dart';

void registerPlugins([final Registrar? pluginRegistrar]) {
  final Registrar registrar = pluginRegistrar ?? webPluginRegistrar;
  CameraPlugin.registerWith(registrar);
  FluttertoastWebPlugin.registerWith(registrar);
  MobileScannerWebPlugin.registerWith(registrar);
  registrar.registerMessageHandler();
}
