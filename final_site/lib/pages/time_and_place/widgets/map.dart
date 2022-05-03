import 'dart:collection';

import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_maps_flutter_web/google_maps_flutter_web.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart' as maps;

class GMap extends GetxController {
  final List<List<maps.LatLng>> polygonLatLongs;
  var polygons = LinkedHashSet<maps.Polygon>().obs;
  final List names;
  List scores = [];
  late maps.GoogleMapController mapController;

  GMap(
      {required this.polygonLatLongs,
      required this.names,
      required this.scores});

  void setScores(List scores) {
    this.scores = scores;
    _setPolygons();
  }

  void onCreated(maps.GoogleMapController controller) {
    mapController = controller;
  }

  void _setPolygons() {
    if (names.length != polygonLatLongs.length) {
      print('wrong length for the names array');
      throw -1;
    }
    for (var i = 0; i < polygonLatLongs.length; ++i) {
      Color color = Colors.black;
      var score_double = double.parse(scores[i]);
      int r_color =
          (score_double * 1000 - ((score_double * 1000) % 100)).toInt();
      if (score_double >= 0.95) {
        color = Colors.red.withOpacity(0.7);
      }
      if (score_double >= 0.1) {
        color = Colors.orange[r_color]!.withOpacity(0.7) as Color;
      } else {
        color = Colors.orange[100]!.withOpacity(0.7) as Color;
      }
      polygons.value.add(
        maps.Polygon(
          polygonId: maps.PolygonId(names[i]),
          points: polygonLatLongs[i],
          fillColor: color,
          geodesic: false,
          strokeWidth: 1,
          consumeTapEvents: true,
          visible: true,
          // onTap:             infoWindow: InfoWindow(
          //     title: "San Francsico",
          //     snippet: "An Interesting city",[
          //   ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    _setPolygons();
    return Obx(
      () => maps.GoogleMap(
        initialCameraPosition: const maps.CameraPosition(
          target: maps.LatLng(31.898043, 35.204269),
          zoom: 10,
        ),
        polygons: polygons.value,
        onMapCreated: onCreated as void Function(maps.GoogleMapController)?,
      ),
    );
  }
}
