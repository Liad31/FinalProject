import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';
import 'package:get/get.dart';
import 'package:final_site/constatns/syle.dart';

class TiktokEmbedd extends StatelessWidget {
  final String src;
  final Color color;
  final String text;
  TiktokEmbedd(
      {Key? key, required this.src, required this.color, required this.text})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 200,
      height: 575,
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
        children: [
          const SizedBox(
            height: 20,
          ),
          Row(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                child: Html(
                  data: """
                <iframe width="600" height="450"
                src="https://www.tiktok.com/embed/$src">
                </iframe>
                  """,
                ),
              ),
            ],
          ),
          Expanded(child: Container()),
          CustomText(
            text: text,
            align: TextAlign.center,
          ),
          Expanded(child: Container()),
        ],
      ),
    );
  }
}
