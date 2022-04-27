import 'dart:html';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/floating_circle.dart';
import 'package:final_site/pages/home/widgets/circles_overview.dart';
import 'package:final_site/pages/home/widgets/overview_cards_large.dart';
import 'package:final_site/pages/home/widgets/overview_cards_small.dart';
import 'package:final_site/pages/home/widgets/text_in_circle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/pages/home/widgets/Image_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:easy_web_view/easy_web_view.dart';
import 'package:final_site/pages/users_to_follow/widgets/users_table.dart';
import 'user.dart';
import 'package:final_site/helpers/database.dart';

class UsersToFollowPage extends StatelessWidget {
  static MongoDatabase database = Get.find();
  List<Map<String, dynamic>> data = [
    {
      'name': 'user1',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.95,
      'id': '123456789'
    },
    {
      'name': 'user2',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.9,
      'id': '123456789'
    },
    {
      'name': 'user3',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.85,
      'id': '123456789'
    },
    {
      'name': 'user4',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.8,
      'id': '123456789'
    },
    {
      'name': 'user5',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.75,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 900,
      'score': 0.7,
    },
    {
      'name': 'user6',
      'governorate': 'Jerusalem',
      'followers': 900,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Yericho',
      'followers': 900,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 1200,
      'score': 0.7,
      'id': '123456789'
    },
    {
      'name': 'user6',
      'governorate': 'Jenin',
      'followers': 1000,
      'score': 0.65,
      'id': '123456789'
    },
  ];

  UsersToFollowPage({Key? key}) : super(key: key);

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
                  text: 'Users to follow tables',
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
                            'On this page we offer two kinds of scores to sort the table by. ',
                        style: GoogleFonts.notoSans(
                          fontSize: 15,
                        ),
                      ),
                      TextSpan(
                        text: 'nationalistic ',
                        style: GoogleFonts.notoSans(
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextSpan(
                        text:
                            'sorts the table by the most nationalistic users found based on their latest uploads.\nThe ',
                        style: GoogleFonts.notoSans(
                          fontSize: 15,
                        ),
                      ),
                      TextSpan(
                        text: 'relevancy ',
                        style: GoogleFonts.notoSans(
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      TextSpan(
                        text:
                            'score, sorts the table by the most relevant users to follow, based on a formula we present, which takes into account both the nationalistic score of the user and his influence power in the area.\nFor sorting the table by one of the columns, click on the wanted column name.',
                        style: GoogleFonts.notoSans(fontSize: 15),
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
          usersTable(data).sortByScore(0, true).build(context),
        ],
      ),
    );
  }
}
