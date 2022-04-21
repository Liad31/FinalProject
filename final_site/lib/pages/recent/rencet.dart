import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';

class RecentPage extends StatelessWidget {
  const RecentPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: CustomText(text: "Recent"),
    );
  }
}
