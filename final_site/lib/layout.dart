import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/widgets/large_screen.dart';
import 'package:final_site/widgets/side_menu.dart';

import 'package:final_site/widgets/top_vav.dart';
import 'package:flutter/material.dart';

class SiteLayout extends StatelessWidget {
  SiteLayout({Key? key}) : super(key: key);
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: scaffoldKey,
      appBar: topNavigationBar(context, scaffoldKey),
      body: ResponsiveWidget(
        largeScreen: const LargeScreen(),
        smallScreen: const LargeScreen(),
        scaffoldKey: scaffoldKey,
      ),
      drawer: const Drawer(
        child: SideMenu(),
      ),
    );
  }
}
