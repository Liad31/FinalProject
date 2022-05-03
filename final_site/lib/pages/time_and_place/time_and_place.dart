import 'dart:convert';
import "dart:io";
import 'package:final_site/pages/time_and_place/widgets/graph.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:syncfusion_flutter_charts/sparkcharts.dart';

import '../../widgets/tiktok_embedd.dart';
import 'package:final_site/pages/time_and_place/widgets/map.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:get/get.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:final_site/constatns/goversJson.dart' as gJson;
import 'dart:convert';
import 'package:final_site/pages/time_and_place/governrate.dart';
import '../../constatns/syle.dart';

class TimeAndPlacePage extends StatelessWidget {
  TimeAndPlacePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String goversString = gJson.goversJson;
    // String goversString = '"govers": [{"name": "bezkoder", "age": 30}]';
    var goversJson = jsonDecode(goversString)['govers'] as List;
    List<Governrate> govers =
        goversJson.map((goverJson) => Governrate.fromJson(goverJson)).toList();
    List<List<LatLng>> cordinates_list = [];
    var govers_names = [];
    var scores = [];
    for (var i = 0; i < govers.length; ++i) {
      cordinates_list.add(govers[i].cordinates);
      govers_names.add(govers[i].name);
      scores.add((0.99 - 0.05 * i).toString());
    }
    print(cordinates_list);
    return Container(
        child: ListView(
      children: [
        Graph(),
        Flexible(
          child: Container(),
          flex: 1,
        ),
        Container(
          decoration: BoxDecoration(
            color: mapBAckground.withOpacity(.7),
            border: Border.all(color: dark.withOpacity(.7), width: .5),
            boxShadow: [
              BoxShadow(
                  offset: const Offset(0, 6),
                  color: lightGrey.withOpacity(.1),
                  blurRadius: 12)
            ],
            borderRadius: BorderRadius.circular(8),
          ),
          width: 630,
          height: 850,
          child: Center(
            child: Container(
              child: GMap(
                polygonLatLongs: cordinates_list as List<List<LatLng>>,
                names: govers_names,
                scores: scores,
              ).build(context),
              width: 600,
              height: 800,
            ),
          ),
        ),
        Flexible(
          child: Container(),
          flex: 9,
        ),
      ],
    ));
  }
}
