import 'dart:html';

import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/recent/widgets/vidoes_table.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:final_site/widgets/tiktok_embedd.dart';
import 'package:flutter/material.dart';
import 'package:flutter_widget_from_html/flutter_widget_from_html.dart';
import 'package:get/state_manager.dart';
import 'package:http/http.dart' as http;
import 'package:google_fonts/google_fonts.dart';
import 'dart:js' as js;

class RecentPage extends StatelessWidget {
  List<Map<String, dynamic>> data = [];
  late String minimumValue = "-1";
  late String maximunValue = "-1";
  late String minimumDateValue = "";
  late String maximunDateValue = "";
  late var error = ''.obs;
  // Initial Selected Value
  late var goverdropdownvalue = 'All'.obs;

  // List of items in our dropdown menu
  var items = [
    'All',
    'Hebron',
    'Bethlehem',
    'Jerusalem',
    'Ramallah and Al-Bireh',
    'Jericho',
    'Tubas',
    'Jenin',
    'Nablus',
    'Tulkarm',
    'Qalqilya',
    'Salfit',
  ];

  RecentPage({Key? key}) : super(key: key);

  Future<void> getFile(minimum, maximum, minDate, maxDate, gover) async {
    var response;
    double minimumDouble;
    double maximumDouble;
    print(maxDate);
    final regex = RegExp(r'(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}');
    try {
      minimumDouble = double.parse(minimum);
      maximumDouble = double.parse(maximum);
    } catch (e) {
      error.value =
          'minimum and maximum values has to be in the range of 0 to 1';
      return;
    }
    if (!(minimumDouble >= 0 &&
        minimumDouble <= 1 &&
        minimumDouble <= maximumDouble &&
        maximumDouble >= 0 &&
        maximumDouble <= 1)) {
      error.value =
          'minimum and maximum values has to be in the range of 0 to 1';
    } else if ((minDate.length != 0 &&
            (minDate.length != 10 || !regex.hasMatch(minDate))) ||
        (maxDate).length != 0 &&
            (maxDate.length != 10 || !regex.hasMatch(maxDate))) {
      error.value = 'date is not in dd-mm-yyyy format';
    } else {
      error.value = '';
      js.context.callMethod('open', [
        'http://104.154.93.111:8080/getVideosByScore?lowerBound=' +
            minimum +
            '&upperBound=' +
            maximum +
            '&minDate=' +
            minDate +
            '&maxDate=' +
            maxDate +
            '&gover=' +
            gover
      ]);
      // await http.get(Uri.parse(
      //     'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/getVideosByScore?lowerBound=' +
      //         minimum +
      //         '&upperBound=' +
      //         maximum));
      // response = await http.get(Uri.parse(
      //     'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/getVideosByScore?lowerBound=0.3&upperBound=0.9'));
    }
  }

  @override
  Widget build(BuildContext context) {
    // MongoDatabase.connect();
    // data = MongoDatabase.getDocuments();
    return Container(
      padding: const EdgeInsets.only(top: 20, left: 40, right: 80),
      child: ListView(
        children: [
          Container(
            margin: const EdgeInsets.only(bottom: 6),
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
                            offset: const Offset(0, 6),
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
            margin: const EdgeInsets.only(bottom: 6),
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
                            'This page features the most recent nationalistic videos uploaded by Palestinians to TikTok.\nYou’re welcome to choose how far back you want to look, and our site will show you the most relevant videos we found in our database from that period.\nEach post contains it\'s link, the bloc it’s uploaded from, the user who posted it, and its nationalistic score given by our model. For your convenience, the first video in the table is presented below.',
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
          Center(
            child: Container(
              height: 370,
              width: 700,
              color: grey.withOpacity(0.2),
              alignment: Alignment.center,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Row(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Flexible(
                        child: Container(),
                        flex: 2,
                      ),
                      Expanded(
                        child: TextField(
                          decoration: InputDecoration(
                            fillColor: light,
                            filled: true,
                            border: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: dark.withOpacity(0.4), width: 5)),
                            labelText: 'Minimum score value',
                          ),
                          onSubmitted: (String value) async {
                            this.minimumValue = value;
                          },
                          onChanged: (String value) async {
                            this.minimumValue = value;
                          },
                        ),
                        flex: 2,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                      Expanded(
                        child: TextField(
                          decoration: InputDecoration(
                            fillColor: light,
                            filled: true,
                            border: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: dark.withOpacity(0.4), width: 5)),
                            labelText: 'Maximum score value',
                          ),
                          onSubmitted: (String value) async {
                            this.maximunValue = value;
                          },
                          onChanged: (String value) async {
                            this.maximunValue = value;
                          },
                        ),
                        flex: 2,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 2,
                      )
                    ],
                  ),
                  SizedBox(
                    height: 30,
                    child: Container(),
                  ),
                  Row(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Flexible(
                        child: Container(),
                        flex: 2,
                      ),
                      Expanded(
                        child: TextField(
                          decoration: InputDecoration(
                            fillColor: light,
                            filled: true,
                            border: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: dark.withOpacity(0.4), width: 5)),
                            labelText: 'min date dd-mm-yyyy',
                          ),
                          onSubmitted: (String value) async {
                            this.minimumDateValue = value;
                          },
                          onChanged: (String value) async {
                            this.minimumDateValue = value;
                          },
                        ),
                        flex: 2,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                      Expanded(
                        child: TextField(
                          decoration: InputDecoration(
                            fillColor: light,
                            filled: true,
                            border: OutlineInputBorder(
                                borderSide: BorderSide(
                                    color: dark.withOpacity(0.4), width: 5)),
                            labelText: 'max dd-mm-yyyy',
                          ),
                          onSubmitted: (String value) async {
                            this.maximunDateValue = value;
                          },
                          onChanged: (String value) async {
                            this.maximunDateValue = value;
                          },
                        ),
                        flex: 2,
                      ),
                      Flexible(
                        child: Container(),
                        flex: 2,
                      )
                    ],
                  ),
                  SizedBox(
                    height: 30,
                    child: Container(),
                  ),
                  Obx(
                    () => DropdownButton<String>(
                      // Initial Value
                      value: goverdropdownvalue.value,
                      // Down Arrow Icon
                      icon: const Icon(Icons.keyboard_arrow_down),

                      // Array list of items
                      items: items.map((String items) {
                        return DropdownMenuItem(
                          value: items,
                          child: Text(items),
                        );
                      }).toList(),
                      // After selecting the desired option,it will
                      // change button value to selected value
                      onChanged: (String? newValue) {
                        goverdropdownvalue.value = newValue!;
                      },
                    ),
                  ),
                  SizedBox(
                    height: 30,
                    child: Container(),
                  ),
                  Center(
                    child: Container(
                      decoration: ShapeDecoration(
                        color: torquise.withOpacity(.8),
                        shape: RoundedRectangleBorder(
                          side: BorderSide(
                            color: dark,
                            width: 3,
                          ),
                        ),
                      ),
                      height: 60,
                      width: 150,
                      child: TextButton(
                        onPressed: () {
                          getFile(
                              this.minimumValue,
                              this.maximunValue,
                              this.minimumDateValue,
                              this.maximunDateValue,
                              this.goverdropdownvalue.value);
                        },
                        child: CustomText(text: 'Get CSV file'),
                      ),
                    ),
                  ),
                  SizedBox(
                    height: 22,
                    child: Container(),
                  ),
                  Obx(() => CustomText(
                        text: error.value,
                        size: 18,
                        color: Colors.red.withOpacity(0.8),
                      ))
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
