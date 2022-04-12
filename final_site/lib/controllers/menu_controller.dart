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
        return _customIcon(Icons.abc, itemName);
      case expertsPageRoute:
        return _customIcon(Icons.access_alarm, itemName);
      case usersToFollowPageRoute:
        return _customIcon(Icons.catching_pokemon, itemName);
      case recentPageRoute:
        return _customIcon(Icons.local_laundry_service, itemName);
      case timeAndSpacePageRoute:
        return _customIcon(Icons.exit_to_app, itemName);
      case authenticationPageRoute:
        return _customIcon(Icons.exit_to_app, itemName);
      default:
        return _customIcon(Icons.exit_to_app, itemName);
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
