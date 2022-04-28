import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:final_site/constatns/syle.dart';

AppBar topNavigationBar(BuildContext context, GlobalKey<ScaffoldState> key) =>
    AppBar(
      leadingWidth: 100,
      leading: !ResponsiveWidget.isSmallScreen(context)
          ? Row(
              children: [
                Container(
                  color: torquise,
                  padding: const EdgeInsets.only(bottom: 100, left: 35),
                  margin: const EdgeInsets.only(bottom: 100),
                  child: IconButton(
                    icon: const Icon(Icons.tiktok_outlined),
                    color: dark.withOpacity(.9),
                    onPressed: () {},
                    iconSize: 50,
                  ),
                  width: 75,
                ),
              ],
            )
          : IconButton(
              icon: const Icon(Icons.menu),
              onPressed: () {
                key.currentState?.openDrawer();
              },
            ),
      elevation: 200,
      title: Row(children: [
        Visibility(
          child: CustomText(
            text: "TikTok nationalistic classifier",
            size: 18,
            color: darkgrey,
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
        const SizedBox(
          width: 16,
        ),
        Container(
          child: Container(
            padding: const EdgeInsets.all(12),
            margin: const EdgeInsets.all(2),
            child: CircleAvatar(
              backgroundColor: torquise,
              child: Icon(
                Icons.person,
                color: dark,
              ),
            ),
          ),
        ),
      ]),
      iconTheme: IconThemeData(color: dark),
      backgroundColor: torquise,
    );
