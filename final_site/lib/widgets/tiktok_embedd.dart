import 'package:flutter/material.dart';
import 'package:flutter_html/flutter_html.dart';

class TiktokEmbedd extends StatelessWidget {
  final String src;

  const TiktokEmbedd({
    Key? key,
    this.src = "6718335390845095173",
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
        child: Html(
      data: """
<iframe width="420" height="315"
src="https://www.tiktok.com/embed/$src">
</iframe>
  """,
    ));
  }
}
