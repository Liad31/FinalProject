import 'package:final_site/widgets/large_screen.dart';
import 'package:flutter/material.dart';

const int largeScreenSize = 1366;
const int meduimScreenSize = 768;
const int smallScreenSize = 360;
const int customScreenSize = 1100;

class ResponsiveWidget extends StatelessWidget {
  final Widget largeScreen;
  final Widget meduimScreen;
  final Widget smallScreen;
  final GlobalKey<ScaffoldState> scaffoldKey;

  const ResponsiveWidget(
      {Key? key,
      this.largeScreen = const LargeScreen(),
      this.meduimScreen = const LargeScreen(),
      this.smallScreen = const LargeScreen(),
      required this.scaffoldKey})
      : super(key: key);

  static bool isSmallScreen(BuildContext context) =>
      MediaQuery.of(context).size.width < meduimScreenSize;

  static bool isMediumScreen(BuildContext context) =>
      MediaQuery.of(context).size.width >= meduimScreenSize &&
      MediaQuery.of(context).size.width < largeScreenSize;

  static bool isLargeScreen(BuildContext context) =>
      MediaQuery.of(context).size.width >= largeScreenSize;

  @override
  Widget build(BuildContext context) {
    WidgetsBinding.instance!.addPostFrameCallback((_) => afterBuild(context));
    return LayoutBuilder(builder: (context, constraints) {
      double _width = constraints.maxWidth;
      if (_width >= largeScreenSize) {
        return largeScreen;
      } else if (_width < largeScreenSize && _width >= meduimScreenSize) {
        return meduimScreen;
      } else {
        return smallScreen;
      }
    });
  }

  void afterBuild(BuildContext context) {
    if (!isSmallScreen(context)) {
      scaffoldKey.currentState?.openEndDrawer();
    }
  }
}
