import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/pages/home/widgets/floating_circle.dart';

class circlesOverview extends StatelessWidget {
  final List texts;
  final Color color;

  const circlesOverview({Key? key, required this.texts, required this.color})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
        mainAxisSize: MainAxisSize.max,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            child: Container(),
            width: 50,
          ),
          ...texts.map((phase) {
            return Expanded(
              flex: 1,
              child: Row(
                children: [
                  floatingCircle(
                    text: phase,
                    color: color,
                    size: 75,
                  ),
                  Flexible(
                    flex: 1,
                    child: Container(),
                  ),
                  if (texts.indexOf(phase) != texts.length - 1)
                    const Flexible(
                      flex: 4,
                      fit: FlexFit.tight,
                      child: SizedBox(
                        width: double.infinity,
                        child: FittedBox(
                          child: Icon(
                            Icons.double_arrow,
                          ),
                        ),
                      ),
                    ),
                  Flexible(
                    flex: 1,
                    child: Container(),
                  ),
                ],
              ),
            );
          }).toList()
        ]);
  }
}
