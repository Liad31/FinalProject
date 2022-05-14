import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class scoreShow extends GetxController {
  static var currentGover = ''.obs;
  static var currentScore = ''.obs;

  scoreShow();

  void set(String gover, String score) {
    currentGover.value = gover;
    currentScore.value = score;
  }

  @override
  Widget build(BuildContext context) {
    return Obx(
      () => CustomText(
        text: () {
          if (currentGover.value.length > 0) {
            return '$currentGover - $currentScore';
          }
          return '';
        }(),
        weight: FontWeight.bold,
        size: 22,
        align: TextAlign.center,
      ),
    );
  }
}
