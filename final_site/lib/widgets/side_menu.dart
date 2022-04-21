import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/routing/routs.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:final_site/widgets/side_menu_item.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import '../constatns/syle.dart';

class SideMenu extends StatelessWidget {
  const SideMenu({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    double _width = MediaQuery.of(context).size.width;
    return Container(
      color: light,
      child: ListView(children: [
        if (ResponsiveWidget.isSmallScreen(context))
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SizedBox(
                height: 20,
              ),
              Row(
                children: [
                  SizedBox(
                    width: _width / 48,
                  ),
                  const Padding(
                    padding: EdgeInsets.only(right: 12),
                    child: Icon(Icons.abc_outlined),
                  ),
                  Flexible(
                    child: CustomText(
                      text: "Dash",
                      size: 20,
                      weight: FontWeight.bold,
                      color: active,
                    ),
                  )
                ],
              ),
            ],
          ),
        const SizedBox(
          height: 20,
        ),
        Divider(
          color: lightGrey.withOpacity(.1),
        ),
        Column(
          mainAxisSize: MainAxisSize.min,
          children: sideMenuItems
              .map((itemName) => SideMenuItem(
                  itemName: itemName == authenticationPageRoute
                      ? "Log out"
                      : itemName,
                  onTap: () {
                    if (itemName == authenticationPageRoute) {
                      // TODO: go to auth page
                    }
                    if (!menuController.isActive(itemName)) {
                      menuController.changeActiveItemTo(itemName);
                      if (ResponsiveWidget.isSmallScreen(context)) {
                        Get.back();
                      }
                      navigationController.navigateTo(itemName);
                    }
                  }))
              .toList(),
        )
      ]),
    );
  }
}
