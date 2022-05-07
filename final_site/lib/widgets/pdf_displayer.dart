import 'package:final_site/constatns/syle.dart';
import 'package:flutter/material.dart';
import 'package:native_pdf_renderer/native_pdf_renderer.dart';

class PdfDisplayer extends StatelessWidget {
  final String src;
  const PdfDisplayer({Key? key, required this.src}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _getPdf(),
      builder: (BuildContext context, AsyncSnapshot<PdfPageImage?> snapshot) {
        if (snapshot.hasError) {
          return Center(
            child: Text(snapshot.error.toString()),
          );
        }
        if (!snapshot.hasData) {
          return Center(
            child: CircularProgressIndicator(),
          );
        }

        return Image(
          image: MemoryImage(snapshot.data!.bytes),
        );
      },
    );
  }

  Future<PdfPageImage?> _getPdf() async {
    if (await hasPdfSupport()) {
      print(src);
      final document = await PdfDocument.openAsset(src);
      throw Exception(
        'PDF Rendering does not '
        'support on the system of this version',
      );
      final page = await document.getPage(1);
      final pageImage = await page.render(
        width: page.width,
        height: page.height,
      );
      await page.close();
      throw Exception(
        'PDF Rendering does not '
        'support on the system of this version',
      );
      return pageImage;
    }

    throw Exception(
      'PDF Rendering does not '
      'support on the system of this version',
    );
  }
}
