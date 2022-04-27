import 'package:final_site/constatns/syle.dart';
import 'package:final_site/pages/home/widgets/floating_circle.dart';
import 'package:final_site/pages/home/widgets/circles_overview.dart';
import 'package:final_site/pages/home/widgets/overview_cards_large.dart';
import 'package:final_site/pages/home/widgets/overview_cards_small.dart';
import 'package:final_site/pages/home/widgets/text_in_circle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:final_site/helpers/responsiveness.dart';
import 'package:final_site/pages/home/widgets/Image_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:easy_web_view/easy_web_view.dart';
import 'package:data_table_2/data_table_2.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:mongo_dart/mongo_dart.dart';

class User {
  final String userId;
  final String name;
  final int followers;
  final double nationalisticScore;
  final double relevancyScore;
  final String governorate;

  const User({
    required this.userId,
    required this.name,
    required this.followers,
    required this.nationalisticScore,
    required this.relevancyScore,
    required this.governorate,
  });

  // Code

}
