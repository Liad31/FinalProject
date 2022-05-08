import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:get/get.dart';
import 'package:final_site/constatns/syle.dart';

class TiktokEmbedd extends StatelessWidget {
  final String src;
  final Color color;
  final String text;
  final double fontSize;
  const TiktokEmbedd(
      {Key? key,
      required this.src,
      required this.color,
      required this.text,
      this.fontSize = 20})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 540,
      width: 230,
      decoration: BoxDecoration(
        color: color,
        border: Border.all(color: dark.withOpacity(.3), width: .5),
        boxShadow: [
          BoxShadow(
              offset: const Offset(0, 6),
              color: lightGrey.withOpacity(.1),
              blurRadius: 12)
        ],
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const SizedBox(
            height: 10,
          ),
          Wrap(alignment: WrapAlignment.center, children: [
            Html(
              data: """
              <iframe height="450"
              src="https://www.tiktok.com/embed/$src">
              </iframe>
                """,
            ),
          ]),
          CustomText(
            text: text,
            align: TextAlign.center,
            size: fontSize,
          ),
          const SizedBox(
            height: 20,
          ),
        ],
      ),
    );
  }
}
