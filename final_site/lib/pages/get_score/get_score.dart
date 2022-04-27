import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../constatns/syle.dart';
import 'package:final_site/pages/get_score/widgets/query_form.dart';

class getScorePage extends StatelessWidget {
  const getScorePage({Key? key}) : super(key: key);

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
                  text: 'Query our model',
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
                            'You are welcome to try and query our machine learning model for a Palestinian nationalistic score of a video(insert a URL to the right input box).\nIn addition, we provide a functionality of querying our model for a Palestinian user\'s nationalistic score produced by his latest posts based on a formula we introduce. Feel free to try!',
                        style: GoogleFonts.notoSans(fontSize: 16),
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
            height: 40,
            child: Container(),
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Flexible(
                child: Container(),
                flex: 1,
              ),
              Expanded(
                flex: 18,
                child: Container(
                  margin: EdgeInsets.only(top: 3),
                  decoration: BoxDecoration(
                    color: veryLightGrey.withOpacity(.4),
                    border: Border.all(color: dark.withOpacity(.3), width: .5),
                    boxShadow: [
                      BoxShadow(
                          offset: Offset(0, 6),
                          color: lightGrey.withOpacity(.1),
                          blurRadius: 12)
                    ],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    children: [
                      SizedBox(
                        height: 40,
                        child: Container(),
                      ),
                      queryForm('Video query', 'Enter the video\'s URL')
                          .build(context),
                      SizedBox(
                        height: 50,
                        child: Container(),
                      ),
                      Row(
                        children: [
                          Flexible(
                            child: Container(),
                            flex: 1,
                          ),
                          Flexible(
                            child: SizedBox(
                              child: Container(
                                decoration: BoxDecoration(
                                  color: dark,
                                  border: Border.all(
                                      color: active.withOpacity(.8), width: .5),
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
                              height: 4,
                            ),
                            flex: 6,
                          ),
                          Flexible(
                            child: Container(),
                            flex: 1,
                          ),
                        ],
                      ),
                      SizedBox(
                        height: 50,
                        child: Container(),
                      ),
                      queryForm('User query', 'Enter the username')
                          .build(context),
                      SizedBox(
                        height: 40,
                        child: Container(),
                      ),
                    ],
                  ),
                ),
              ),
              Flexible(
                child: Container(),
                flex: 1,
              ),
            ],
          ),
          SizedBox(
            height: 40,
            child: Container(),
          ),
        ],
      ),
    );
  }
}
