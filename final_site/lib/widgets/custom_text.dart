import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomText extends StatelessWidget {
  final String text;
  final double size;
  final Color color;
  final FontWeight weight;
  final TextAlign align;

  const CustomText({
    Key? key,
    this.text = "",
    this.size = 16,
    this.color = Colors.black,
    this.align = TextAlign.left,
    this.weight = FontWeight.normal,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: GoogleFonts.lora(
        fontSize: size,
        color: color,
        fontWeight: weight,
      ),
      textAlign: align,
    );
  }
}
