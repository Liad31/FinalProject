// ignore_for_file: prefer_const_constructors
import 'package:final_site/constatns/syle.dart';

import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:google_fonts/google_fonts.dart';

class queryForm extends GetxController {
  var title = '';
  var score = '0.5'.obs;
  var defaultText = '';
  queryForm(@required String this.title, @required String this.defaultText) {}

  @override
  Widget build(BuildContext context) {
    return Obx(
      () => Column(
        children: [
          CustomText(
            text: '$title',
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
                    obscureText: true,
                    decoration: InputDecoration(
                      fillColor: light,
                      filled: true,
                      border: OutlineInputBorder(
                          borderSide: BorderSide(
                              color: dark.withOpacity(0.4), width: 5)),
                      labelText: '$defaultText',
                    ),
                    onSubmitted: (String value) async {
                      await showDialog<void>(
                        context: context,
                        builder: (BuildContext context) {
                          return AlertDialog(
                            title: const Text('Thanks!'),
                            content: Text(
                                'You typed "$value", which has length ${value.characters.length}.'),
                            actions: <Widget>[
                              TextButton(
                                onPressed: () {
                                  Navigator.pop(context);
                                },
                                child: const Text('OK'),
                              ),
                            ],
                          );
                        },
                      );
                    }),
              ),
              SizedBox(
                width: 20,
                child: Container(),
              ),
              Ink(
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
                  onPressed: () {},
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
          RichText(
            text: TextSpan(
              style: const TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.normal,
              ),
              children: <TextSpan>[
                TextSpan(
                  text: 'The post\'s score is $score',
                  style: GoogleFonts.notoSans(
                    fontSize: 25,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
