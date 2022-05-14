import 'package:final_site/constatns/syle.dart';

import 'package:final_site/pages/recent/widgets/vidoes_table.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:final_site/widgets/tiktok_embedd.dart';
import 'package:flutter/material.dart';

import 'package:google_fonts/google_fonts.dart';

class RecentPage extends StatelessWidget {
  List<Map<String, dynamic>> data = [];
  //   {
  //     // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
  //     'user': 'user1',
  //     'governorate': 'Jenin',
  //     'views': 20000,
  //     'likes': 1000,
  //     'score': 0.95,
  //     'id': '7073810575611956481'
  //   },
  //   {
  //     // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
  //     'user': 'user2',
  //     'governorate': 'Jerusalem',
  //     'views': 50000,
  //     'likes': 40000,
  //     'score': 0.9,
  //     'id': '7073810575611956481'
  //   },
  //   {
  //     // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
  //     'user': 'user1',
  //     'governorate': 'Jenin',
  //     'views': 20000,
  //     'likes': 1000,
  //     'score': 0.83,
  //     'id': '7082076746517990662'
  //   },
  //   {
  //     // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
  //     'user': 'user3',
  //     'governorate': 'Jenin',
  //     'views': 2000,
  //     'likes': 1200,
  //     'score': 0.77,
  //     'id': '7082076746517990662'
  //   },
  //   {
  //     // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
  //     'user': 'user1',
  //     'governorate': 'Jenin',
  //     'views': 12,
  //     'likes': 6,
  //     'score': 0.65,
  //     'id': '7082076746517990662'
  //   },
  // ];

  RecentPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // MongoDatabase.connect();
    // data = MongoDatabase.getDocuments();
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
                            'On this page we present you the most Palestinian nationalistic videos lately uploaded to the TikTok platform.\nYou are welcome to choose how far back you want to look, And our site will show you the most relevant videos we found in our DB from that timme period.\nEach post contains it\'s linke, the governrate it was uploaded from, the user who published it and it\'s nationalistic score given by our model. For your convenience, The first video in the table is presented below.',
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
          videoTable(data).sortByScore(0, true).build(context),
          // Row(
          //   children: [
          //     Expanded(child: Container()),
          //     TiktokEmbedd(
          //       src: data[0]["id"],
          //       color: Colors.red,
          //       text: '',
          //     ),
          //     Expanded(child: Container()),
          //   ],
          // )
        ],
      ),
    );
  }
}
