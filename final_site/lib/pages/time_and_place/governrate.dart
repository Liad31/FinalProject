import 'package:google_maps_flutter/google_maps_flutter.dart';

class Governrate {
  late String name;
  List<LatLng> cordinates = [];

  Governrate(String name, List cordinates) {
    this.name = name;
    for (var i = 0; i < cordinates.length; ++i) {
      this.cordinates = cordinates
          .map((cordinate) => LatLng(cordinate[1], cordinate[0]))
          .toList();
    }
  }
  factory Governrate.fromJson(dynamic json) {
    return Governrate(json['name'], json['cordinates']);
  }
}
