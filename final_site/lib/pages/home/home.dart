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

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var c = 9;
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
          const CustomText(
            text:
                'The TikTok classifier is a tool for recognizing palestinian nationalism in TikTok.\nThe tool is based on a machine learning model which was trained for classifying TikTok videos as either palestinian nationalistic or not.\nThis tool was developed by R. Cirkin, G. Vitrak and L. Kehila as the final project for our computer science B.A in Bar-Ilan University. We collaborated with the Department of Middle Eastern Studiest of BIU, specifically with our mentors Y. mann and Eli (A.K.A hitpalgut normalit, Proxy medaleg, etc.) and students in their seminar.\nThanks to their guidance and the hard work of the seminar students who helped us a lot along the way, our model achived great performance.\nThe tool and its results are now avaible in this website. Now, using our tool we can follow palestinian nationalistic users, monitor their videos and predict nationalistic waves in the West bank before they burst.',
            size: 18,
            weight: FontWeight.normal,
          ),
          SizedBox(
            child: Container(),
            width: double.infinity,
            height: 8,
          ),
          const CustomText(
            text:
                'At first, we had to define palestinian nationalism and characterize the kinds of videos we should be looking out for. After discussing this with the seminar students and our mentors we got a green light to start collecting data(users, videos, etc...) from Tiktok, we created a location analyzer which tries to make sure that all our data comes from the West bank. Then, we built the tagging site for our taggers, the seminar students, where they could tag the videos we collected. this data was later used to train our model.\nAfter 3 intensive months of video tagging and model building, we finally were able to train & test our model on the labeled data.',
            size: 18,
            weight: FontWeight.normal,
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
                  children: [
                    RichText(
                      text: TextSpan(
                        text:
                            'Our model Relies on 4 different data types: text description, it\'s hashtags, The sound attached to the video and the video itself. For each data type we created a sub-model or introduced logic before combining all the outputs of the sub-models which were trained separately before into one vector and passed it through a final fully connected network. For the text description we built an attention based LSTM taking as input the words of the description represented as the vector given by ##AraVec 3.0 (word2vec)##. For the hashtags we developed a weighted-KNN model, Our logic was to look at the correlation between a given hashtag and the nationalism of the posts tagged by it. We then defined a score function combining the hashtags of each post(reminds of a weighted-KNN). Our video model is the Tannet model provided by ##MMaction 2.0##,  with it\'s final layer cut (to allow our final model to infer more about the video itself). Finally for the post sound we created a nationalistic sounds bucket based on the nationalistic sounds we accumulated in the tagging process and look for those sounds in future posts. Combining those four together, we created our final model which outputs a nationalistic score for a given TikTok post.',
                        style: GoogleFonts.notoSans(
                          fontSize: 18,
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                    ),
                    const CustomText(
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
                      'On the get score page you can ask our machine learning mode for either a nationalistic score for a given Tiktok post(just insert it\'s id) or a nationalistic score for a Tiktok user based on his videos(just insert his username). ',
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
        ],
      ),
    );
  }
}
