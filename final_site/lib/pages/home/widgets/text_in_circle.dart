import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class textCircle extends StatelessWidget {
  final String text;
  final Color color1;
  final Color color2;
  final int size1;
  final int size2;
  final Color textColor;
  const textCircle({
    Key? key,
    required this.text,
    required this.color1,
    required this.color2,
    required this.size1,
    required this.size2,
    this.textColor = const Color.fromARGB(255, 34, 30, 30),
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      backgroundColor: color1, //back ground colors
      radius: size1.toDouble(),
      child: CircleAvatar(
        backgroundColor: color2, //back ground colors
        radius: size2.toDouble(),
        child: ClipRRect(
          child: Column(children: [
            Expanded(
              child: Container(),
              flex: 1,
            ),
            CustomText(
              text: text,
              size: (size2 * (8 - text.length + 2.5) / 8),
              align: TextAlign.center,
              weight: FontWeight.bold,
            ),
            Expanded(child: Container()),
          ]),
        ),
      ),
    );
  }
}
