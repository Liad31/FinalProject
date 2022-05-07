import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';

import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/text_in_circle.dart';

class InfoCard extends StatelessWidget {
  final String title;
  final String value;
  final Color topColor;
  final bool isActive;
  final VoidCallback onTap;

  const InfoCard(
      {Key? key,
      required this.title,
      required this.value,
      this.isActive = false,
      required this.onTap,
      required this.topColor})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      customBorder: const RoundedRectangleBorder(),
      borderRadius: BorderRadius.circular(12),
      hoverColor: Colors.black,
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.all(4.0),
        height: 135,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
                offset: const Offset(0, 6),
                color: lightGrey.withOpacity(.1),
                blurRadius: 8)
          ],
          border: Border.all(color: lightGrey, width: 3.5),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                    child: Container(
                  decoration: BoxDecoration(
                    color: topColor,
                    border: Border.all(color: lightGrey, width: 0.3),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  height: 6,
                ))
              ],
            ),
            Expanded(
              child: Container(),
            ),
            CustomText(
              text: "$title",
              color: dark,
              size: 24,
              align: TextAlign.center,
              weight: FontWeight.bold,
            ),
            Expanded(
              child: Container(),
            ),
            textCircle(
                text: "$value",
                color1: lightBlue,
                color2: light,
                size1: 42,
                size2: 35),
            Expanded(
              child: Container(),
            ),
          ],
        ),
      ),
    );
  }
}
