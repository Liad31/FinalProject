// ignore_for_file: prefer_const_constructors
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';

class queryForm extends GetxController {
  var title = '';
  RxString score = ''.obs;
  String defaultText = '';
  String value = '';
  bool isUser = false;
  bool ispending = false;
  queryForm(this.title, this.defaultText, this.isUser) {
    value = defaultText;
  }

  Future<http.Response> getPredictedScore() async {
    final http.Response response;
    String url = "";
    if (!isUser) {
      url =
          'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/getPredicted?urls=["$value"]';
    } else {
      //change to user prediction
      url =
          'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/getPredictedRelScore?username="$value"';
    }
    response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      return response;
    } else {
      throw Exception('Failed to load score');
    }
  }

  Future<http.Response> getPredictedScoreIter() async {
    while (true) {
      http.Response response = await getPredictedScore();
      if (response.statusCode != 200) {
        throw Exception('Failed to load score');
      }
      if (response.body.toString() != "too early") {
        return response;
      }
      await Future.delayed(Duration(seconds: 30));
    }
  }

  Future<int> getScore() async {
    final http.Response response;
    http.Response response1 = await getPredictedScore();
    String url = "";
    if (!isUser) {
      url =
          'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/predict?urls=["$value"]';
    } else {
      //change to user prediction
      url =
          'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/userRelScore?username="$value"';
    }
    if (response1.body.toString() != "too early") {
      response = response1;
    } else {
      response = await http
          .get(Uri.parse(url))
          .timeout(Duration(seconds: 30), onTimeout: getPredictedScoreIter);
    }
    if (response.statusCode == 200) {
      final parsed =
          jsonDecode(response.body.toString()).cast<Map<String, dynamic>>();
      ispending = false;
      // print(parsed.length);
      // print(parsed[0]['result'].toString().substring(0, 5));
      if (parsed.length == 0) {
        score.value = "Failed to load score";
      } else {
        score.value = parsed[0]['result'].toString().substring(0, 5);
      }
      return 1;
    } else {
      score.value = "Failed to load score";
      throw Exception('Failed to load score');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Obx(
      () => Column(
        children: [
          CustomText(
            text: title,
            size: 28,
            weight: FontWeight.bold,
            align: TextAlign.center,
          ),
          SizedBox(
            height: 30,
            child: Container(),
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Expanded(
                child: Container(),
                flex: 1,
              ),
              Expanded(
                flex: 4,
                child: TextField(
                  decoration: InputDecoration(
                    fillColor: light,
                    filled: true,
                    border: OutlineInputBorder(
                        borderSide:
                            BorderSide(color: dark.withOpacity(0.4), width: 5)),
                    labelText: '$value',
                  ),
                  onSubmitted: (String value) async {
                    this.value = value;
                    score.value = 'calculating...';
                    ispending = true;
                    getScore();
                  },
                  onChanged: (String value) async {
                    this.value = value;
                  },
                ),
              ),
              SizedBox(
                width: 20,
                child: Container(),
              ),
              Container(
                decoration: ShapeDecoration(
                  color: veryLightGrey.withOpacity(.8),
                  shape: RoundedRectangleBorder(
                    side: BorderSide(
                      color: dark,
                      width: 5,
                    ),
                  ),
                ),
                child: IconButton(
                  icon: const Icon(Icons.search),
                  tooltip: 'submit query',
                  onPressed: () async {
                    score.value = 'calculating...';
                    ispending = true;
                    getScore();
                  },
                ),
              ),
              Expanded(
                child: Container(),
                flex: 1,
              ),
            ],
          ),
          SizedBox(
            height: 30,
            child: Container(),
          ),
          !ispending
              ? RichText(
                  text: TextSpan(
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.normal,
                    ),
                    children: <TextSpan>[
                      TextSpan(
                        text: () {
                          if (score.isEmpty) {
                            return '';
                          } else if (score.value == "Failed to load score") {
                            return score.value;
                          } else {
                            return "The post\'s score is ${score.value}";
                          }
                        }(),
                        style: GoogleFonts.notoSans(
                          fontSize: 25,
                          fontWeight: FontWeight.bold,
                          color: () {
                            if (!score.isEmpty &&
                                score.value != "Failed to load score") {
                              var score_double = double.parse(score.value);
                              int r_color = (score_double * 1000 -
                                      ((score_double * 1000) % 100))
                                  .toInt();
                              if (score_double >= 0.95) {
                                return Colors.red;
                              }
                              if (score_double >= 0.1) {
                                return Colors.orange[r_color];
                              } else {
                                return Colors.orange[200];
                              }
                            } else {
                              return Colors.black;
                            }
                          }(),
                        ),
                      ),
                    ],
                  ),
                )
              : Column(
                  children: [
                    RichText(
                      text: TextSpan(
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.normal,
                        ),
                        children: <TextSpan>[
                          TextSpan(
                            text: 'It may take a few seconds...',
                            style: GoogleFonts.notoSans(),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(
                      height: 4,
                    ),
                    Icon(Icons.pending),
                  ],
                ),
        ],
      ),
    );
  }
}
