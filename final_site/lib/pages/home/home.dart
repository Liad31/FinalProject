import 'dart:async';
import 'dart:convert';

import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/circles_overview.dart';
import 'package:final_site/pages/home/widgets/overview_cards_large.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:final_site/widgets/my_markdown.dart';
import 'package:final_site/widgets/tiktok_embedd.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:final_site/pages/home/widgets/Image_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatelessWidget {
  late OverviewCardsLargeScreen cards;
  var datas = [
    {'title': 'Tagged videos', 'value': '24,000'},
    {'title': 'AUC', 'value': '94'},
    {'title': 'Examined users', 'value': '4481'},
    {'title': 'Videos from last 24h', 'value': '0'}
  ].obs;

  HomePage({Key? key}) : super(key: key);

  int countOccurences(String mainString, String search) {
    int lInx = 0;
    int count = 0;
    while (lInx != -1) {
      lInx = mainString.indexOf(search, lInx);
      if (lInx != -1) {
        count++;
        lInx += search.length;
      }
    }
    return count;
  }

  Future<String> fetchUsersCount() async {
    final response = await http.get(Uri.parse(
        'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/usersCount'));
    if (response.statusCode == 200) {
      print(response.body.toString());
      datas[2]['value'] = response.body.toString();
      return response.body.toString();
    } else {
      throw Exception('Failed to load usersCount');
    }
  }

  Future<String> fetchVideosFromLast() async {
    final response = await http.get(Uri.parse(
        'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/videosFromLast?hours=24'));
    if (response.statusCode == 200) {
      print(response.body.toString());
      // datas[3]['value'] =
      //     countOccurences(response.body.toString(), "\"Vid\"").toString();
      datas[3]['value'] = response.body.toString();
      return response.body.toString();
    } else {
      throw Exception('Failed to load VideosFromLast24h');
    }
  }

  Future<String>? fetchData() async {
    await Future.wait([fetchUsersCount(), fetchVideosFromLast()]);
    print('done!');
    return 'done!';
  }

  @override
  Widget build(BuildContext context) {
    const List project_phases = [
      'Define nationalistic',
      'Collect data',
      'Build the tagging site',
      'Get labeled data',
      'Build and train the model'
    ];
    cards = OverviewCardsLargeScreen(datas);

    return Container(
      padding: const EdgeInsets.only(top: 20, left: 40, right: 80),
      child: ListView(
        children: [
          Container(
            margin: const EdgeInsets.only(bottom: 6),
            child: Row(
              children: [
                const CustomText(
                  text: 'TikTok classifier',
                  size: 34,
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
                    color: dark,
                  ),
                  width: double.infinity,
                  height: 3,
                ),
                flex: 10,
              ),
              Flexible(
                child: SizedBox(
                  child: Container(),
                  width: double.infinity,
                  height: 3,
                ),
                flex: 2,
              )
            ],
          ),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 10,
          ),
          const SizedBox(
            child: MyMarkdown(src: "markdown/text1.md"),
            height: 260,
          ),
          circlesOverview(texts: project_phases, color: torquise),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 13,
          ),
          FutureBuilder(
            future: fetchData(),
            builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                // OverviewCardsLargeScreen(datas).build(context)
                return cards.build(context);
              } else {
                return Container();
              }
            },
          ),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 15,
          ),
          Column(
            children: const [
              SizedBox(
                child: MyMarkdown(src: "markdown/text2.md"),
                height: 180,
              ),
              CustomText(
                text: 'Our TikTok classifier achieved an AUC of 94!',
                size: 18,
                weight: FontWeight.bold,
                color: Color.fromARGB(255, 11, 55, 131),
              ),
            ],
          ),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 25,
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            children: [
              Expanded(child: Container()),
              ImageCard(
                imagePath: 'photos/diagram.jpg',
                onTap: () {},
              ),
              Expanded(child: Container()),
            ],
          ),

          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 25,
          ),
          //
          //
          //
          //
          //
          //
          //
          //
          //
          //
          //
          FutureBuilder(
            future: rootBundle.loadString("home_vids/vids.json"),
            builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
              if (snapshot.hasData) {
                var data = snapshot.data;
                if (data != null) {
                  var list = json.decode(data);
                  List<dynamic> nat = list["national"];
                  List<dynamic> notNat = list["not_national"];
                  nat.shuffle();
                  notNat.shuffle();
                  return Row(
                    children: [
                      Expanded(child: Container()),
                      TiktokEmbedd(
                        src: nat[0]["vid"],
                        color: Colors.red,
                        text: 'score: ${nat[0]["score"].toStringAsFixed(3)}',
                        fontSize: 16,
                      ),
                      Expanded(child: Container()),
                      TiktokEmbedd(
                        src: notNat[0]["vid"],
                        color: Colors.green,
                        text: 'score: ${notNat[0]["score"].toStringAsFixed(3)}',
                        fontSize: 16,
                      ),
                      Expanded(child: Container()),
                      TiktokEmbedd(
                        src: nat[1]["vid"],
                        color: Colors.red,
                        text: 'score: ${nat[1]["score"].toStringAsFixed(3)}',
                        fontSize: 16,
                      ),
                      Expanded(child: Container()),
                    ],
                  );
                }
              }
              return const Center(
                child: CircularProgressIndicator(),
              );
            },
          ),
          Container(
            margin: const EdgeInsets.only(bottom: 6),
            child: Row(
              children: [
                const CustomText(
                  text: 'Our site',
                  size: 28,
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
                    color: dark,
                  ),
                  width: double.infinity,
                  height: 3,
                ),
                flex: 10,
              ),
              Flexible(
                child: SizedBox(
                  child: Container(),
                  width: double.infinity,
                  height: 3,
                ),
                flex: 2,
              )
            ],
          ),
          CustomText(
            text:
                '\nAll the data presented in the site is updated every 24h. Once a day, The algorithm downloads all the new videos it finds and updates all the data, with scores shown on the site.',
            size: 18,
            color: active,
            weight: FontWeight.bold,
          ),
          RichText(
            text: TextSpan(
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.normal,
              ),
              children: <TextSpan>[
                TextSpan(
                  text: '\nGet score page\n\n',
                  style: GoogleFonts.notoSans(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    decoration: TextDecoration.underline,
                  ),
                ),
                TextSpan(
                  text:
                      'On the get score page, you can test our machine learning model for either a nationalistic score for a given Tiktok post (by inserting its id) or a nationalistic score for a Tiktok user based on his videos (by inserting a username).',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
                TextSpan(
                    text: '\n\nUsers to follow\n\n',
                    style: GoogleFonts.notoSans(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    )),
                TextSpan(
                  text:
                      'Using our model, we managed to build a tool for following nationalistic users in the West Bank. We’ve accumulated ${datas[2]['value']} users in our database (and counting) and calculated a nationalistic score for each of them based on their latest nationalistic posts. In addition, we introduced a relevancy score for each user, which considers their nationalistic score and their influence on the Tiktok platform (followers, likes, etc.). If you’d like to watch the most relevant/nationalistic users, you\'re welcome to visit the "users to follow page," where all the relevant tables will be available.',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
                TextSpan(
                    text: '\n\nRecent\n\n',
                    style: GoogleFonts.notoSans(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    )),
                TextSpan(
                  text:
                      'The current page shows the most relevant nationalistic videos from the last 24h, which were found by our algorithm. their relevancy is based on their nationalistic score and exposure. This page is excellent for monitoring problematic videos from the West Bank, which may encourage violence or misuse of the platform.',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
                TextSpan(
                    text: '\n\nLocation\n\n',
                    style: GoogleFonts.notoSans(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    )),
                TextSpan(
                  text:
                      'On the location page, you’ll find a map showing the nationalistic level of each bloc in the West Bank. The nationalistic label of the bloc is determined by the average nationalistic level of the bloc’s overall users.',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
                TextSpan(
                    text: '\n\nTime\n\n',
                    style: GoogleFonts.notoSans(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    )),
                TextSpan(
                  text:
                      'The main goal of our tool is presented on the time page. Using our model, we try to predict nationalistic waves in the West Bank before they burst.\nThe chart graph featured on the time page shows the nationalistic score progress in time, based on the videos uploaded at each time period. Using the progression we present in the graph, intelligence and military bodies can monitor the temper in the Palestinian street, ultimately preventing future violence and terrorist attacks.',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20)
        ],
      ),
    );
  }
}
