import 'package:final_site/helpers/local_nagivator.dart';
import 'package:final_site/widgets/side_menu.dart';
import 'package:flutter/material.dart';

class LargeScreen extends StatelessWidget {
  const LargeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(children: [
      const Expanded(
        child: SideMenu(),
      ),
      Expanded(
        flex: 5,
        child: localNavgator(),
      ),
    ]);
  }
}
