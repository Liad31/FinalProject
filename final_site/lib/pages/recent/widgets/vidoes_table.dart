// ignore_for_file: prefer_const_constructors
import 'dart:convert';

import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:google_fonts/google_fonts.dart';
import 'package:data_table_2/data_table_2.dart';
import 'package:url_launcher/url_launcher.dart';

class videoTable extends GetxController {
  int table_size = 10;
  var currentTable = '24'.obs;
  var data = [].obs;
  late List data_24 = [];
  late List data_72 = [];
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

  Future<String>? fetchData() async {
    Future<String> getvids(hours) async {
      var response = await http
          .get(Uri.parse(
              'https://floating-harbor-96334.herokuapp.com/http://104.154.93.111:8080/topVideos?n=25&sort=score&hours=' +
                  hours))
          .then((value) {
        if (value.statusCode == 200) {
          var json =
              jsonDecode(value.body.toString()).cast<Map<String, dynamic>>();
          if (hours == '24') {
            data_24 = json
                .map((video) => {
                      'video': 'https://tiktok.com/@username/video/70880m12__' +
                          video['Vid'].toString() +
                          'is_copy_url=1&is_from_webapp=v1',
                      'user': video['userName'].toString(),
                      'governorate': video['governorate'].toString(),
                      'score': double.parse(
                          video['score'].toString().substring(0, 5)),
                      'views':
                          int.parse(video['stats']['plays_count'].toString()),
                      'likes':
                          int.parse(video['stats']['diggs_count'].toString()),
                      'id': video['Vid'].toString()
                    })
                .toList();
            data.value = data_24;
          } else {
            data_72 = json
                .map((video) => {
                      'video': 'https://tiktok.com/@username/video/70880m12__' +
                          video['Vid'].toString() +
                          'is_copy_url=1&is_from_webapp=v1',
                      'user': video['userName'].toString(),
                      'governorate': video['governorate'].toString(),
                      'score': double.parse(
                          video['score'].toString().substring(0, 5)),
                      'views':
                          int.parse(video['stats']['plays_count'].toString()),
                      'likes':
                          int.parse(video['stats']['diggs_count'].toString()),
                      'id': video['Vid'].toString()
                    })
                .toList();
          }
          return 'done';
        } else {
          throw Exception('Failed to load users');
        }
      });
      return response.toString();
    }

    await Future.wait([getvids('24'), getvids('72')]);
    return 'done';
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
                          data.value = data_24;
                          currentTable.value = '24';
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
                              if (currentTable.value == '96') {
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
                          data.value = data_72;
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
              child: FutureBuilder(
                  future: fetchData(),
                  builder:
                      (BuildContext context, AsyncSnapshot<String> snapshot) {
                    if (snapshot.connectionState == ConnectionState.done ||
                        snapshot.connectionState == ConnectionState.waiting) {
                      return Obx(
                        () => DataTable2(
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
                            var link =
                                'https://www.tiktok.com/@username/video/' +
                                    data[index]['id'] +
                                    '?is_copy_url=1&is_from_webapp=v1';
                            var gover = data[index]['governorate'];
                            var views = data[index]['views'].toString();
                            var likes = data[index]['likes'].toString();
                            var score = data[index]['score'].toString();
                            var user = data[index]['user'];
                            var realIdx = index + 1;
                            String _url_post = link;
                            String _url_user =
                                'https://www.tiktok.com/@' + user;
                            DataCell rankDataCell = DataCell(
                              RichText(
                                text: TextSpan(
                                  text: "$realIdx",
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
                                      text: "$realIdx",
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
                                      text: "$realIdx",
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
                                    backgroundColor: MaterialStateProperty
                                        .resolveWith<Color?>(
                                      (Set<MaterialState> states) {
                                        if (states.contains(
                                                MaterialState.focused) ||
                                            states.contains(
                                                MaterialState.pressed) ||
                                            states.contains(
                                                MaterialState.hovered)) {
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
                                    if (!await launch(_url_post)) {
                                      throw 'Could not launch $_url_post';
                                    }
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
                                    backgroundColor: MaterialStateProperty
                                        .resolveWith<Color?>(
                                      (Set<MaterialState> states) {
                                        if (states.contains(
                                                MaterialState.focused) ||
                                            states.contains(
                                                MaterialState.pressed) ||
                                            states.contains(
                                                MaterialState.hovered)) {
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
                                    if (!await launch(_url_user)) {
                                      throw 'Could not launch $_url_user';
                                    }
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
                                  color:
                                      MaterialStateProperty.resolveWith<Color?>(
                                          (Set<MaterialState> states) {
                                    var score_double = double.parse(score);
                                    int r_color = (score_double * 1000 -
                                            ((score_double * 1000) % 100))
                                        .toInt();
                                    if (states
                                        .contains(MaterialState.hovered)) {
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
                                  color:
                                      MaterialStateProperty.resolveWith<Color?>(
                                          (Set<MaterialState> states) {
                                    var score_double = double.parse(score);
                                    int r_color = (score_double * 1000 -
                                            ((score_double * 1000) % 100))
                                        .toInt();
                                    if (states
                                        .contains(MaterialState.hovered)) {
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
                                  color:
                                      MaterialStateProperty.resolveWith<Color?>(
                                          (Set<MaterialState> states) {
                                    var score_double = double.parse(score);
                                    int r_color = (score_double * 1000 -
                                            ((score_double * 1000) % 100))
                                        .toInt();
                                    if (states
                                        .contains(MaterialState.hovered)) {
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
                      );
                    } else {
                      return Container();
                    }
                  }),
            ),
          ],
        ),
      ),
    );
  }
}
