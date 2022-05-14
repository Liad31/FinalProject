import 'dart:convert';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:syncfusion_flutter_charts/sparkcharts.dart';
import '../../widgets/custom_text.dart';
import '../../widgets/tiktok_embedd.dart';
import 'package:final_site/pages/time_and_place/widgets/map.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:final_site/constatns/goversJson.dart' as gJson;
import 'package:final_site/pages/time_and_place/governrate.dart';
import '../../constatns/syle.dart';
import 'package:final_site/pages/time_and_place/widgets/score_show.dart';
import 'package:http/http.dart' as http;

class TimeAndPlacePage extends StatelessWidget {
  late List scores = [];
  late List<List<LatLng>> cordinates_list = [];
  late List<Governrate> gover = [];
  late List govers_names = [];

  TimeAndPlacePage({Key? key}) : super(key: key);

  Future<String>? fetchData() async {
    String goversString = gJson.goversJson;
    var goversJson = jsonDecode(goversString)['govers'] as List;
    List<Governrate> govers =
        goversJson.map((goverJson) => Governrate.fromJson(goverJson)).toList();
    Future<String> getgovernorates() async {
      var response = await http
          .get(Uri.parse('http://104.154.93.111:8080/governorates'))
          .then((value) {
        if (value.statusCode == 200) {
          var json =
              jsonDecode(value.body.toString()).cast<Map<String, dynamic>>();
          List names = json.map((gov) => gov.keys.toList()[0]).toList();
          for (var i = 0; i < govers.length; ++i) {
            cordinates_list.add(govers[i].cordinates);
            govers_names.add(govers[i].name);
            print(json[names.indexOf(govers[i].name)]
                [json[names.indexOf(govers[i].name)].keys.toList()[0]]);
            scores.add((json[names.indexOf(govers[i].name)]
                        [json[names.indexOf(govers[i].name)].keys.toList()[0]] +
                    0.1)
                .toString()
                .substring(0, 5));
          }
          return 'done';
        } else {
          throw Exception('Failed to load map');
        }
      });
      return response.toString();
    }

    await Future.wait([getgovernorates()]);
    return 'done';
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(top: 20, left: 40, right: 80),
      child: ListView(
        children: [
          Container(
            margin: EdgeInsets.only(bottom: 6),
            child: Row(
              children: [
                Expanded(
                  child: Container(),
                ),
                const CustomText(
                  text: 'Latest nationalistic videos tables',
                  size: 30,
                  weight: FontWeight.bold,
                ),
                Expanded(
                  child: Container(),
                ),
              ],
            ),
            height: 60,
          ),
          Row(
            children: [
              Flexible(
                child: SizedBox(
                  child: Container(
                    decoration: BoxDecoration(
                      color: dark,
                      border:
                          Border.all(color: active.withOpacity(.4), width: .5),
                      boxShadow: [
                        BoxShadow(
                            offset: Offset(0, 6),
                            color: lightGrey.withOpacity(.1),
                            blurRadius: 12)
                      ],
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  width: double.infinity,
                  height: 3,
                ),
                flex: 80,
              ),
            ],
          ),
          SizedBox(
            height: 20,
            child: Container(),
          ),
          Container(
            margin: EdgeInsets.only(bottom: 6),
            child: Row(
              mainAxisSize: MainAxisSize.max,
              children: [
                RichText(
                  text: TextSpan(
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.normal,
                    ),
                    children: <TextSpan>[
                      TextSpan(
                        text:
                            'On this page we present you the most Palestinian nationalistic videos lately uploaded to the TikTok platform.\nYou are welcome to choose how far back you want to look, And our site will show you the most relevant videos we found in our DB from that time period.\nEach post contains it\'s linke, the governrate it was uploaded from, the user who published it and it\'s nationalistic score given by our model. For your convenience, The first video in the table is presented below.',
                        style: GoogleFonts.notoSans(
                          fontSize: 15,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Container(),
                ),
              ],
            ),
          ),
          SizedBox(
            height: 20,
            child: Container(),
          ),
          Container(
            child: Row(
              children: [
                Flexible(
                  child: Container(
                    color: torquise.withOpacity(0.3),
                  ),
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
                  height: double.infinity,
                  child: Column(
                    children: [
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                      Container(
                        child: FutureBuilder(
                            future: fetchData(),
                            builder: (context, snapshot) {
                              if (snapshot.connectionState ==
                                      ConnectionState.done ||
                                  snapshot.connectionState ==
                                      ConnectionState.waiting) {
                                return GMap(
                                  polygonLatLongs:
                                      cordinates_list as List<List<LatLng>>,
                                  names: govers_names,
                                  scores: scores,
                                ).build(context);
                              } else {
                                return GMap(
                                    polygonLatLongs: [],
                                    names: [],
                                    scores: []).build(context);
                              }
                            }),
                        width: 600,
                        height: 800,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 2,
                      ),
                      scoreShow().build(context),
                      Flexible(
                        child: Container(color: torquise.withOpacity(0.3)),
                        flex: 2,
                      ),
                    ],
                  ),
                ),
                Flexible(
                  child: Container(
                    color: torquise.withOpacity(0.3),
                  ),
                  flex: 1,
                ),
              ],
            ),
            height: 900,
          ),
        ],
      ),
    );
  }
}
