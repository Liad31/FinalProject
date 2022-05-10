import 'package:final_site/constatns/syle.dart';
import 'package:flutter/material.dart';
import 'package:pdfx/pdfx.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';

class PdfDisplayer extends StatelessWidget {
  final String src;
  const PdfDisplayer({Key? key, required this.src}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _getPdf(),
      builder: (BuildContext context, AsyncSnapshot<SfPdfViewer?> snapshot) {
        if (snapshot.hasError) {
          return Center(
            child: Text(snapshot.error.toString()),
          );
        }
        if (snapshot.hasData) {
          final data = snapshot.data;

          if (data != null) {
            return Container(
              child: data,
            );
          }
        }
        return const Center(
          child: CircularProgressIndicator(),
        );
      },
    );
  }

  Future<SfPdfViewer?> _getPdf() async {
    return SfPdfViewer.asset(src);
  }
}
