import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class floatingCircle extends StatelessWidget {
  final String text;
  final Color color;
  final int size;
  final Color textColor;
  const floatingCircle({
    Key? key,
    required this.text,
    required this.color,
    this.size = 20,
    this.textColor = const Color.fromARGB(255, 34, 30, 30),
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // return Container(
    //   decoration: BoxDecoration(
    //       border: Border.all(
    //         color: color,
    //       ),
    //       color: color,
    //       borderRadius: BorderRadius.all(Radius.circular(size.toDouble()))),
    //   child: CustomText(
    //     text: text,
    //   ),
    // );
    return CircleAvatar(
      backgroundColor: color, //back ground colors
      radius: size.toDouble(),
      child: ClipRRect(
        child: CustomText(
          text: text,
          size: (size / 3) - 1,
          align: TextAlign.center,
          weight: FontWeight.bold,
        ),
      ),
    );
  }
}
