import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:url_launcher/url_launcher.dart';

class MyMarkdown extends StatelessWidget {
  final String src;
  const MyMarkdown({Key? key, required this.src}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: rootBundle.loadString(src),
      builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
        if (snapshot.hasData) {
          final data = snapshot.data;
          if (data != null) {
            return Markdown(
                data: data,
                onTapLink: (text, url, title) {
                  launch(url!);
                },
                styleSheet: MarkdownStyleSheet.fromTheme(ThemeData(
                    textTheme: const TextTheme(
                        bodyText2: TextStyle(fontSize: 18.0)))));
          }
        }

        return const Center(
          child: CircularProgressIndicator(),
        );
      },
    );
  }
}
