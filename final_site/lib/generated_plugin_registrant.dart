//
// Generated file. Do not edit.
//

// ignore_for_file: directives_ordering
// ignore_for_file: lines_longer_than_80_chars

import 'package:audio_session/audio_session_web.dart';
import 'package:device_info_plus_web/device_info_plus_web.dart';
import 'package:google_maps_flutter_web/google_maps_flutter_web.dart';
import 'package:just_audio_web/just_audio_web.dart';
import 'package:pdfx/src/renderer/web/pdfx_plugin.dart';
import 'package:syncfusion_pdfviewer_web/pdfviewer_web.dart';
import 'package:url_launcher_web/url_launcher_web.dart';
import 'package:video_player_web/video_player_web.dart';
import 'package:wakelock_web/wakelock_web.dart';

import 'package:flutter_web_plugins/flutter_web_plugins.dart';

// ignore: public_member_api_docs
void registerPlugins(Registrar registrar) {
  AudioSessionWeb.registerWith(registrar);
  DeviceInfoPlusPlugin.registerWith(registrar);
  GoogleMapsPlugin.registerWith(registrar);
  JustAudioPlugin.registerWith(registrar);
  PdfxPlugin.registerWith(registrar);
  SyncfusionFlutterPdfViewerPlugin.registerWith(registrar);
  UrlLauncherPlugin.registerWith(registrar);
  VideoPlayerPlugin.registerWith(registrar);
  WakelockWeb.registerWith(registrar);
  registrar.registerMessageHandler();
}
