// ignore_for_file: prefer_const_constructors
import 'package:final_site/constatns/syle.dart';

import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:google_fonts/google_fonts.dart';

import 'package:data_table_2/data_table_2.dart';
import 'package:url_launcher/url_launcher.dart';

class videoTable extends GetxController {
  int table_size = 10;
  var currentTable = '24'.obs;
  var data = [].obs;
  bool sortedByScore = true;

  videoTable(List datasSet) {
    data.value = datasSet;
  }

  setList(List newdatas) {
    data.value = newdatas;
  }

  sortByGover(int columnIndex, bool ascending) {
    data.sort((a, b) => a['governorate'].compareTo(b['governorate']));
    sortedByScore = false;
    return this;
  }

  sortByViews(int columnIndex, bool ascending) {
    data.sort((a, b) => b['views'].compareTo(a['views']));
    sortedByScore = false;
    return this;
  }

  sortByLikes(int columnIndex, bool ascending) {
    data.sort((a, b) => b['likes'].compareTo(a['likes']));
    sortedByScore = false;
    return this;
  }

  sortByScore(int columnIndex, bool ascending) {
    data.sort((a, b) => b['score'].compareTo(a['score']));
    sortedByScore = true;
    return this;
  }

  @override
  Widget build(BuildContext context) {
    Widget _verticalDivider = const VerticalDivider(
      color: Colors.black,
      thickness: 1,
    );
    return Obx(
      () => Container(
        decoration: BoxDecoration(
          color: Colors.white,
          border: Border.all(color: active.withOpacity(.4), width: .5),
          boxShadow: [
            BoxShadow(
                offset: Offset(0, 6),
                color: lightGrey.withOpacity(.1),
                blurRadius: 12)
          ],
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.all(16),
        margin: EdgeInsets.only(bottom: 30),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                Flexible(
                  child: Container(),
                  flex: 1,
                ),
                CustomText(
                  text: 'Videos from last ' + currentTable.value + ' hours',
                  color: dark,
                  weight: FontWeight.bold,
                  size: 24,
                ),
                Flexible(
                  child: Row(
                    children: [
                      Icon(Icons.watch_later_outlined),
                      Flexible(
                        child: Container(),
                        flex: 15,
                      ),
                      TextButton(
                        style: ButtonStyle(
                          fixedSize: MaterialStateProperty.resolveWith<Size?>(
                              (Set<MaterialState> states) {
                            return Size.fromWidth(100);
                          }),
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (currentTable.value == '24') {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              if (states.contains(MaterialState.focused) ||
                                  states.contains(MaterialState.pressed) ||
                                  states.contains(MaterialState.hovered)) {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              return torquise; // Defer to the widget's default.
                            },
                          ),
                        ),
                        onPressed: () {
                          //setList(getNAtionalistic());
                          setList([
                            {
                              // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
                              'user': 'user2',
                              'governorate': 'Juruz',
                              'views': 1200,
                              'likes': 900,
                              'score': 0.91,
                              'id': '7073810575611956481'
                            }
                          ]);
                          currentTable.value = '24';
                          table_size = 10;
                        },
                        child: RichText(
                          text: TextSpan(
                            text: '24h',
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                              color: blue,
                            ),
                          ),
                        ),
                      ),
                      Flexible(
                        child: Container(),
                        flex: 1,
                      ),
                      TextButton(
                        style: ButtonStyle(
                          fixedSize: MaterialStateProperty.resolveWith<Size?>(
                              (Set<MaterialState> states) {
                            return Size.fromWidth(100);
                          }),
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (currentTable.value == '72') {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              if (states.contains(MaterialState.focused) ||
                                  states.contains(MaterialState.pressed) ||
                                  states.contains(MaterialState.hovered)) {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              return torquise; // Defer to the widget's default.
                            },
                          ),
                        ),
                        onPressed: () {
                          //setList(getNAtionalistic());
                          setList([
                            {
                              // 'video': 'https://tiktok.com/@username/video/70880m12__b432452777757953?is_copy_url=1&is_from_webapp=v1',
                              'user': 'user1',
                              'governorate': 'Jenin',
                              'views': 12,
                              'likes': 6,
                              'score': 0.73,
                              'id': '7082076746517990662'
                            }
                          ]);
                          currentTable.value = '72';
                          table_size = 25;
                        },
                        child: RichText(
                          text: TextSpan(
                            text: '72h',
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                              color: blue,
                            ),
                          ),
                        ),
                      ),
                      Flexible(
                        child: Container(),
                        flex: 15,
                      ),
                    ],
                  ),
                  flex: 1,
                ),
              ],
            ),
            Container(
              margin: EdgeInsets.only(top: 3),
              decoration: BoxDecoration(
                color: light,
                border: Border.all(color: dark.withOpacity(.4), width: .5),
                boxShadow: [
                  BoxShadow(
                      offset: Offset(0, 6),
                      color: lightGrey.withOpacity(.1),
                      blurRadius: 12)
                ],
                borderRadius: BorderRadius.circular(8),
              ),
              child: DataTable2(
                columnSpacing: 10,
                horizontalMargin: 12,
                smRatio: 0.3,
                lmRatio: 0.5,
                dividerThickness: 5,
                minWidth: 600,
                columns: [
                  const DataColumn2(
                    label: CustomText(
                      text: "Rank",
                      size: 22,
                      align: TextAlign.left,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.S,
                  ),
                  const DataColumn2(
                    label: CustomText(
                      text: " Post",
                      size: 22,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                  DataColumn2(
                    label: CustomText(
                      text: " User",
                      size: 22,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                  DataColumn2(
                    onSort: sortByViews,
                    label: CustomText(
                      text: "Views",
                      size: 22,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                  DataColumn2(
                    onSort: sortByLikes,
                    label: CustomText(
                      text: "Likes",
                      size: 22,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                  DataColumn2(
                    onSort: sortByGover,
                    label: CustomText(
                      text: "Governorate",
                      size: 22,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                  DataColumn2(
                    onSort: sortByScore,
                    label: CustomText(
                      text: 'Nationalistic score',
                      size: 22,
                      align: TextAlign.left,
                      weight: FontWeight.bold,
                    ),
                    size: ColumnSize.M,
                  ),
                ],
                rows: List<DataRow>.generate(data.length, (index) {
                  var link = 'https://www.tiktok.com/@username/video/' +
                      data[index]['id'] +
                      '?is_copy_url=1&is_from_webapp=v1';
                  var gover = data[index]['governorate'];
                  var views = data[index]['views'].toString();
                  var likes = data[index]['likes'].toString();
                  var score = data[index]['score'].toString();
                  var user = data[index]['user'];
                  String _url_post = link;
                  String _url_user = 'https://www.tiktok.com/@' + user;
                  DataCell rankDataCell = DataCell(
                    RichText(
                      text: TextSpan(
                        text: "$index",
                        style: GoogleFonts.merriweather(
                          fontSize: 18,
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                    ),
                  );
                  DataCell rankDataCellTop = DataCell(
                    Row(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        RichText(
                          text: TextSpan(
                            text: "$index",
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        const Expanded(
                          child: Icon(Icons.outlined_flag_rounded),
                        )
                      ],
                    ),
                  );
                  DataCell rankDataCellFirst = DataCell(
                    Row(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        RichText(
                          text: TextSpan(
                            text: "$index",
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        const Expanded(
                          child: Icon(Icons.flag_sharp),
                        )
                      ],
                    ),
                  );
                  DataCell linkDataCell = DataCell(
                      TextButton(
                        style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (states.contains(MaterialState.focused) ||
                                  states.contains(MaterialState.pressed) ||
                                  states.contains(MaterialState.hovered)) {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              return null; // Defer to the widget's default.
                            },
                          ),
                        ),
                        onPressed: () async {
                          if (!await launch(_url_post))
                            throw 'Could not launch $_url_post';
                        },
                        child: RichText(
                          text: TextSpan(
                            text: 'Link to the post',
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                              color: blue,
                            ),
                          ),
                        ),
                      ),
                      onTap: () {});
                  DataCell userDataCell = DataCell(
                      TextButton(
                        style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (states.contains(MaterialState.focused) ||
                                  states.contains(MaterialState.pressed) ||
                                  states.contains(MaterialState.hovered)) {
                                return Theme.of(context)
                                    .colorScheme
                                    .primary
                                    .withOpacity(0.5);
                              }
                              return null; // Defer to the widget's default.
                            },
                          ),
                        ),
                        onPressed: () async {
                          if (!await launch(_url_user))
                            throw 'Could not launch $_url_user';
                        },
                        child: RichText(
                          text: TextSpan(
                            text: '$user',
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                              color: blue,
                            ),
                          ),
                        ),
                      ),
                      onTap: () {});
                  DataCell goverDataCell = DataCell(
                    Row(
                      children: [
                        Flexible(
                          flex: 1,
                          child: Container(),
                        ),
                        RichText(
                          text: TextSpan(
                            text: gover,
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        Flexible(
                          flex: 4,
                          child: Container(),
                        ),
                      ],
                    ),
                  );
                  DataCell viewsDataCell = DataCell(
                    Row(
                      children: [
                        // Flexible(
                        //   flex: 1,
                        //   child: Container(),
                        // ),
                        RichText(
                          text: TextSpan(
                            text: views,
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        Flexible(
                          flex: 20,
                          child: Container(),
                        ),
                      ],
                    ),
                  );
                  DataCell likesDataCell = DataCell(
                    Row(
                      children: [
                        // Flexible(
                        //   flex: 1,
                        //   child: Container(),
                        // ),
                        RichText(
                          text: TextSpan(
                            text: likes,
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        Flexible(
                          flex: 20,
                          child: Container(),
                        ),
                      ],
                    ),
                  );
                  DataCell scoreDataCell = DataCell(
                    Row(
                      children: [
                        Flexible(
                          flex: 4,
                          child: Container(),
                        ),
                        RichText(
                          text: TextSpan(
                            text: score,
                            style: GoogleFonts.merriweather(
                              fontSize: 18,
                              fontWeight: FontWeight.normal,
                            ),
                          ),
                        ),
                        Flexible(
                          flex: 7,
                          child: Container(),
                        ),
                      ],
                    ),
                  );
                  if ((index == 0) && (sortedByScore)) {
                    return DataRow(
                        color: MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                          var score_double = double.parse(score);
                          int r_color = (score_double * 1000 -
                                  ((score_double * 1000) % 100))
                              .toInt();
                          if (states.contains(MaterialState.hovered)) {
                            //INMPLEMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            // return Theme.of(context)
                            //     .colorScheme
                            //     .primary
                            //     .withOpacity(0.08);
                            // return Colors.red;
                          }
                          if (score_double >= 0.95) {
                            return Colors.red;
                          }
                          if (score_double >= 0.1) {
                            return Colors.orange[r_color];
                          } else {
                            return Colors.orange[100];
                          }
                        }),
                        cells: [
                          rankDataCellFirst,
                          linkDataCell,
                          userDataCell,
                          viewsDataCell,
                          likesDataCell,
                          goverDataCell,
                          scoreDataCell,
                        ]);
                  } else if ((index < 3) && (sortedByScore)) {
                    return DataRow(
                        color: MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                          var score_double = double.parse(score);
                          int r_color = (score_double * 1000 -
                                  ((score_double * 1000) % 100))
                              .toInt();
                          if (states.contains(MaterialState.hovered)) {
                            //INMPLEMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            // return Theme.of(context)
                            //     .colorScheme
                            //     .primary
                            //     .withOpacity(0.08);
                            // return Colors.red;
                          }
                          if (score_double >= 0.95) {
                            return Colors.red;
                          }
                          if (score_double >= 0.1) {
                            return Colors.orange[r_color];
                          } else {
                            return Colors.orange[100];
                          }
                        }),
                        cells: [
                          rankDataCellTop,
                          linkDataCell,
                          userDataCell,
                          viewsDataCell,
                          likesDataCell,
                          goverDataCell,
                          scoreDataCell,
                        ]);
                  } else {
                    return DataRow(
                        color: MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                          var score_double = double.parse(score);
                          int r_color = (score_double * 1000 -
                                  ((score_double * 1000) % 100))
                              .toInt();
                          if (states.contains(MaterialState.hovered)) {
                            //INMPLEMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            // return Theme.of(context)
                            //     .colorScheme
                            //     .primary
                            //     .withOpacity(0.08);
                            // return Colors.red;
                          }
                          if (score_double >= 0.95) {
                            return Colors.red;
                          }
                          if (score_double >= 0.1) {
                            return Colors.orange[r_color];
                          } else {
                            return Colors.orange[100];
                          }
                        }),
                        cells: [
                          rankDataCell,
                          linkDataCell,
                          userDataCell,
                          viewsDataCell,
                          likesDataCell,
                          goverDataCell,
                          scoreDataCell,
                        ]);
                  }
                }),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
