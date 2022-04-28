import 'package:final_site/pages/home/home.dart';
import 'package:final_site/pages/recent/rencet.dart';
import 'package:final_site/pages/time_and_place/time_and_place.dart';
import 'package:final_site/pages/users_to_follow/users_to_follow.dart';
import 'package:final_site/routing/routs.dart';
import 'package:flutter/material.dart';

import '../pages/get_score/get_score.dart';

Route<dynamic> genarateRoute(RouteSettings settings) {
  switch (settings.name) {
    case homePageRoute:
      return _getPageRoute(const HomePage());
    case getScorePageRoute:
      return _getPageRoute(const getScorePage());
    case usersToFollowPageRoute:
      return _getPageRoute(UsersToFollowPage());
    case recentPageRoute:
      return _getPageRoute(RecentPage());
    case timeAndPlacePageRoute:
      return _getPageRoute(const TimeAndPlacePage());
    default:
      return _getPageRoute(const HomePage());
  }
}

PageRoute _getPageRoute(Widget child) {
  return MaterialPageRoute(builder: (context) => child);
}
