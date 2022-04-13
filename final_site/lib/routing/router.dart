import 'package:final_site/pages/home/home.dart';
import 'package:final_site/pages/recent/rencet.dart';
import 'package:final_site/pages/time_and_space/time_and_space.dart';
import 'package:final_site/pages/users_to_follow/users_to_follow.dart';
import 'package:final_site/routing/routs.dart';
import 'package:flutter/material.dart';

import '../pages/experts/experts.dart';

Route<dynamic> genarateRoute(RouteSettings settings) {
  switch (settings.name) {
    case homePageRoute:
      return _getPageRoute(const HomePage());
    case expertsPageRoute:
      return _getPageRoute(const ExpertsPage());
    case usersToFollowPageRoute:
      return _getPageRoute(const UsersToFollowPage());
    case recentPageRoute:
      return _getPageRoute(const RecentPage());
    case timeAndSpacePageRoute:
      return _getPageRoute(const TimeAndSpacePage());
    default:
      return _getPageRoute(const HomePage());
  }
}

PageRoute _getPageRoute(Widget child) {
  return MaterialPageRoute(builder: (context) => child);
}
