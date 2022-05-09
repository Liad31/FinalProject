import 'package:final_site/pages/time/widgets/graph.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../constatns/syle.dart';
import 'package:final_site/pages/time_and_place/widgets/score_show.dart';
import 'package:final_site/widgets/custom_text.dart';

class TimePage extends StatelessWidget {
  const TimePage({Key? key}) : super(key: key);

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
                  text: 'Nationalistic progression in time',
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
                            'The following graph shows the nationalistic level in the west bank by day.\nThe score of each day is calculated by the average nationalistic score of the videos we examined, which were uploaded in the three days prior each date.\nWhen hovering on each time point in the graph you can watch the most nationalistic video from that day.\n We also allow you to choose how far back do you want the graph to present, one year back or a full lifetime.\nNow, using our model and the fact that we update our databse with new users and videos every day,\nThe relevant bodies can use this graph in order to predict and prevent violent nationalistic waves and watch the progression of the nationslistic level on Tiktok in the west bank.\n hopefully our tool can help the security forces and maybe even save lifes.',
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
                  child: Container(),
                  flex: 1,
                ),
                Container(
                  decoration: BoxDecoration(
                    color: Colors.white,
                    border: Border.all(color: dark.withOpacity(.7), width: .5),
                    boxShadow: [
                      BoxShadow(
                          offset: const Offset(0, 6),
                          color: lightGrey.withOpacity(.1),
                          blurRadius: 12)
                    ],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  width: 1000,
                  height: double.infinity,
                  child: Column(
                    children: [
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                      SizedBox(
                        child: Graph(),
                        height: 800,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                    ],
                  ),
                ),
                Flexible(
                  child: Container(),
                  flex: 9,
                ),
              ],
            ),
            height: 1000,
          ),
        ],
      ),
    );
  }
}
