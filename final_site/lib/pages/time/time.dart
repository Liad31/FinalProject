import 'package:final_site/pages/time/widgets/graph.dart';
import 'package:flutter/material.dart';
import '../../constatns/syle.dart';
import 'package:final_site/pages/time_and_place/widgets/score_show.dart';

class TimePage extends StatelessWidget {
  const TimePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Flexible(
          child: Container(),
          flex: 1,
        ),
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            border: Border.all(color: dark.withOpacity(.7), width: .5),
            boxShadow: [
              BoxShadow(
                  offset: const Offset(0, 6),
                  color: lightGrey.withOpacity(.1),
                  blurRadius: 12)
            ],
            borderRadius: BorderRadius.circular(8),
          ),
          width: 1000,
          height: double.infinity,
          child: Column(
            children: [
              Flexible(
                child: Container(),
                flex: 1,
              ),
              SizedBox(
                child: Graph(),
                height: 800,
              ),
              Flexible(
                child: Container(),
                flex: 2,
              ),
              scoreShow().build(context),
              Flexible(
                child: Container(),
                flex: 2,
              ),
            ],
          ),
        ),
        Flexible(
          child: Container(),
          flex: 9,
        ),
      ],
    );
  }
}
