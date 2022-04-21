import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/floating_circle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/pages/home/widgets/info_card.dart';

class OverviewCardsMediumScreen extends StatelessWidget {
  List datas;

  OverviewCardsMediumScreen({Key? key, required this.datas}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double _width = MediaQuery.of(context).size.width;

    return Row(children: [
      ...datas.map((data) {
        return Expanded(
          flex: 1,
          child: Row(
            children: [
              Flexible(
                flex: 8,
                child: InfoCard(
                  title: data['title'],
                  value: data['value'],
                  onTap: () {},
                  topColor: torquise,
                ),
              ),
              Flexible(
                flex: 1,
                child: Container(),
              ),
              //   SizedBox(
              //     width: _width / 64,
              //   ),
            ],
          ),
        );
      }).toList()
    ]);
  }
}
