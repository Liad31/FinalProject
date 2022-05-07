import 'package:final_site/constatns/syle.dart';
import 'package:final_site/routing/routs.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class MenuController extends GetxController {
  static MenuController isntance = Get.find();
  var activeItem = homePageRoute.obs;
  var hoverItem = "".obs;

  changeActiveItemTo(String itemName) {
    activeItem.value = itemName;
  }

  onHover(String itemName) {
    if (!isActive(itemName)) hoverItem.value = itemName;
  }

  isActive(String itemName) => activeItem.value == itemName;

  isHoveing(String itemName) => hoverItem.value == itemName;

  Widget returnIconFor(String itemName) {
    switch (itemName) {
      case homePageRoute:
        return _customIcon(Icons.home_rounded, itemName);
      case getScorePageRoute:
        return _customIcon(Icons.grade_rounded, itemName);
      case usersToFollowPageRoute:
        return _customIcon(Icons.people, itemName);
      case recentPageRoute:
        return _customIcon(Icons.video_collection_rounded, itemName);
      case locationPageRoute:
        return _customIcon(Icons.map, itemName);
      case timePageRoute:
        return _customIcon(Icons.access_time_filled_sharp, itemName);
      default:
        return _customIcon(Icons.home_rounded, itemName);
    }
  }

  Widget _customIcon(IconData icon, String itemName) {
    if (isActive(itemName)) {
      return Icon(
        icon,
        size: 22,
        color: dark,
      );
    }
    return Icon(
      icon,
      color: isHoveing(itemName) ? dark : lightGrey,
    );
  }
}
