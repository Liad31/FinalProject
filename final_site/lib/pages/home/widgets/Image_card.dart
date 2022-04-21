import 'package:final_site/constatns/controllers.dart';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ImageCard extends StatelessWidget {
  final String imagePath;
  final VoidCallback onTap;

  const ImageCard({
    Key? key,
    required this.imagePath,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      height: 400,
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
              offset: const Offset(0, 6),
              color: lightGrey.withOpacity(.1),
              blurRadius: 8)
        ],
        border: Border.all(color: lightGrey, width: 3.5),
        borderRadius: BorderRadius.circular(8),
      ),
      child: FittedBox(
        fit: BoxFit.fill,
        child: Image.asset(imagePath),
      ),
    );
    // return FittedBox(
    //   child: Image.asset(imagePath),
    // );
  }
}
