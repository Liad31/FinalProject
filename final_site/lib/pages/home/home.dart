import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/circles_overview.dart';
import 'package:final_site/pages/home/widgets/overview_cards_large.dart';
import 'package:final_site/pages/home/widgets/overview_cards_small.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:final_site/widgets/my_markdown.dart';
import 'package:final_site/widgets/tiktok_embedd.dart';
import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:get/get.dart';
import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/pages/home/widgets/Image_card.dart';
import 'package:google_fonts/google_fonts.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    const List project_phases = [
      'Define nationalistic',
      'Collect data',
      'Build the tagging site',
      'Get labeled data',
      'Build and train the model'
    ];
    var datas = [
      {'title': 'Tagged videos', 'value': '30,000'},
      {'title': 'AUC', 'value': '94'},
      {'title': 'Examined users', 'value': '3,824'},
      {'title': 'New videos from last 24h', 'value': '121'},
    ].obs;
    return Container(
      padding: EdgeInsets.only(top: 20, left: 40, right: 80),
      child: ListView(
        children: [
          Container(
            margin: EdgeInsets.only(bottom: 6),
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
            height: 300,
          ),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 10,
          ),
          circlesOverview(texts: project_phases, color: torquise),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 13,
          ),
          if (ResponsiveWidget.isLargeScreen(context) ||
              ResponsiveWidget.isMediumScreen(context))
            OverviewCardsLargeScreen(datas).build(context)
          else
            OverviewCardsSmallScreen(datas).build(context),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 15,
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            children: [
              Expanded(
                child: Column(
                  children: const [
                    SizedBox(
                      child: MyMarkdown(src: "markdown/text2.md"),
                      height: 300,
                    ),
                    CustomText(
                      text:
                          'With all of that, our TikTok classifier achived an AUC of 94!',
                      size: 18,
                      weight: FontWeight.bold,
                    ),
                  ],
                ),
                flex: 3,
              ),
              Expanded(
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  children: [
                    Flexible(
                      child: Container(),
                      flex: 1,
                    ),
                    Flexible(
                      flex: 25,
                      child: ImageCard(
                        imagePath: 'assets/photos/diagram.png',
                        onTap: () {},
                      ),
                    ),
                    Flexible(
                      child: Container(),
                      flex: 1,
                    ),
                  ],
                ),
                flex: 4,
              ),
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
                '\nAll the data presented in the site is rendered every 24h. Once a day, The Algorithm downloads all the new videos it founds and updating all the data and scores shown in the site.',
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
                      'On the get score page you can query our machine learning mode for either a nationalistic score for a given Tiktok post(just insert it\'s id) or a nationalistic score for a Tiktok user based on his videos(just insert his username). ',
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
                      'Using our model, we managed to build a tool for following nationalistic users in the west bank area. we have accumaleted ${datas[2]['value']} users in our database(and still counting) and calculated a nationalistic score for each of them, based on their latest nationalistic posts. Adding on that, we introduce a relevancy score given for each user which takes into consideration his nationalistic score, and his influence in the Tiktok platform(followers, likes, etc.). If you would like to watch the most relevant/nationalistic users, you\'re welcome to visit the users to follow page where you will find all the relevant tables.',
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
                      'The recent page shows the most relevant nationalistic videos from the last 24h which were found by our algorithm. their relevancy is based on their nationalistic score and their exposure. This page is great for monitoring problematic videos from the west bank which may encourage violence or Cause fermentation.',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
                TextSpan(
                    text: '\n\nTime and place\n\n',
                    style: GoogleFonts.notoSans(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    )),
                TextSpan(
                  text: '...',
                  style: GoogleFonts.notoSans(
                      fontSize: 18, fontWeight: FontWeight.normal),
                ),
              ],
            ),
          ),
          TiktokEmbedd(
              src: "6718335390845095173", color: Colors.green, text: 'nice'),
        ],
      ),
    );
  }
}
