import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:final_site/constatns/syle.dart';

AppBar topNavigationBar(BuildContext context, GlobalKey<ScaffoldState> key) =>
    AppBar(
      leading: !ResponsiveWidget.isSmallScreen(context)
          ? Row(
              children: [
                Container(
                  padding: const EdgeInsets.only(left: 14),
                  child: Image.asset(
                    "icons/logo.jpeg",
                    width: 28,
                  ),
                )
              ],
            )
          : IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {
                key.currentState?.openDrawer();
              },
            ),
      elevation: 0,
      title: Row(children: [
        Visibility(
          child: CustomText(
            text: "Dash",
            size: 20,
            color: lightGrey,
            weight: FontWeight.bold,
          ),
        ),
        Expanded(
          child: Container(),
        ),
        IconButton(
          icon: const Icon(Icons.settings),
          color: dark.withOpacity(.7),
          onPressed: () {},
        ),
        Stack(
          children: [
            IconButton(
              icon: Icon(Icons.notifications, color: dark.withOpacity(.7)),
              onPressed: () {},
            ),
            Positioned(
              top: 7,
              right: 7,
              child: Container(
                width: 12,
                height: 12,
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                    color: active,
                    borderRadius: BorderRadius.circular(30),
                    border: Border.all(
                      color: light,
                      width: 2,
                    )),
              ),
            )
          ],
        ),
        Container(
          width: 1,
          height: 22,
          color: lightGrey,
        ),
        CustomText(
          text: "hello",
          color: lightGrey,
        ),
        const SizedBox(
          width: 16,
        ),
        Container(
          decoration: BoxDecoration(
              color: Colors.white, borderRadius: BorderRadius.circular(30)),
          child: Container(
            padding: const EdgeInsets.all(12),
            margin: const EdgeInsets.all(2),
            child: CircleAvatar(
              backgroundColor: light,
              child: Icon(
                Icons.person,
                color: dark,
              ),
            ),
          ),
        ),
      ]),
      iconTheme: IconThemeData(color: dark),
      backgroundColor: Colors.transparent,
    );
