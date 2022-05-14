import 'package:final_site/constatns/syle.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/pages/home/widgets/info_card.dart';

class OverviewCardsLargeScreen extends GetxController {
  var datas = [].obs;

  OverviewCardsLargeScreen(List datasSet) {
    datas.value = datasSet;
  }

  setList(List newdatas) {
    datas.value = newdatas;
  }

  Widget build(BuildContext context) {
    double _width = MediaQuery.of(context).size.width;
    if (datas.isNotEmpty) {
      return Obx(
        () => Row(
          mainAxisSize: MainAxisSize.max,
          children: [
            Flexible(
              child: Container(),
            ),
            ...datas.map((data) {
              return Flexible(
                flex: 6,
                child: Row(
                  children: [
                    Expanded(
                      flex: 5,
                      child: InfoCard(
                        title: data['title'],
                        value: data['value'],
                        onTap: () {},
                        topColor: torquise,
                      ).build(context),
                    ),
                    Expanded(
                      flex: 1,
                      child: Container(),
                    ),
                  ],
                ),
              );
            }).toList()
          ],
        ),
      );
    } else {
      return Container();
    }
  }
}
