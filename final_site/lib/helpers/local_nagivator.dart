import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/routing/router.dart';
import 'package:final_site/routing/routs.dart';
import 'package:flutter/material.dart';

Navigator localNavgator() => Navigator(
      key: navigationController.navigationKey,
      initialRoute: homePageRoute,
      onGenerateRoute: genarateRoute,
    );
