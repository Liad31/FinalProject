import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/pages/home/widgets/info_card_small.dart';

class OverviewCardsSmallScreen extends GetxController {
  var datas = [].obs;

  OverviewCardsSmallScreen(List datasSet) {
    datas.value = datasSet;
  }

  setList(List newdatas) {
    datas.value = newdatas;
  }

  @override
  Widget build(BuildContext context) {
    double _width = MediaQuery.of(context).size.width;
    if (datas.isNotEmpty) {
      return Obx(
        () => Container(
          height: 400,
          child: Column(
            children: [
              ...datas.map((data) {
                return Expanded(
                  flex: 1,
                  child: Column(
                    children: [
                      Flexible(
                        flex: 6,
                        child: InfoCardSmall(
                          title: data['title'],
                          value: data['value'],
                          onTap: () {},
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
            ],
          ),
        ),
      );
    } else {
      return Container();
    }
  }
}
