// ignore_for_file: prefer_const_constructors
import 'dart:convert';
import 'dart:math';
import 'package:final_site/constatns/syle.dart';
import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:data_table_2/data_table_2.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;

class usersTable extends GetxController {
  final int table_size = 25;
  var currentTable = 'Nationalistic'.obs;
  var data = [].obs;
  late List data_nat = [];
  late List data_rel = [];
  bool sortedByScore = true;

  usersTable(List datasSet) {
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

  sortByFollowers(int columnIndex, bool ascending) {
    data.sort((a, b) => b['followers'].compareTo(a['followers']));
    sortedByScore = false;
    return this;
  }

  sortByScore(int columnIndex, bool ascending) {
    data.sort((a, b) => b['score'].compareTo(a['score']));
    sortedByScore = true;
    return this;
  }

  resolveColor(Set<MaterialState> states, int index) {
    var score_double = data[index]['score'];
    int r_color = (score_double * 1000 - ((score_double * 1000) % 100)).toInt();
    Color? color;
    if (score_double >= 0.95) {
      color = Colors.red;
    } else if (score_double >= 0.1) {
      color = Colors.orange[r_color];
    } else {
      color = Colors.orange[100];
    }

    return color;
  }

  Future<String>? fetchData() async {
    Future<String> getNat() async {
      var response = await http.get(
        Uri.parse(
            'https://cors-anywhere.herokuapp.com/http://104.154.93.111:8080/topUsers?n=25&sort=nationalisticScore&days=30'),
        headers: <String, String>{
          'x-requested-with': 'f',
        },
      ).then((value) {
        if (value.statusCode == 200) {
          var json =
              jsonDecode(value.body.toString()).cast<Map<String, dynamic>>();
          data_nat = json
              .map((user) => {
                    'name': user['userName'].toString(),
                    'governorate': user['governorate'].toString(),
                    'followers': int.parse(
                        user['userStats']['followers_count'].toString()),
                    'score':
                        double.parse(user['nationalisticScore'].toString()),
                    'id': user['userId'].toString(),
                  })
              .toList();
          data.value = data_nat;
          return 'done';
        } else {
          throw Exception('Failed to load users');
        }
      });
      return response.toString();
    }

    Future<String> getRel() async {
      var response = await http.get(
        Uri.parse(
            'https://cors-anywhere.herokuapp.com/http://104.154.93.111:8080/topUsers?n=25&sort=relevancyScore'),
        headers: <String, String>{
          'x-requested-with': 'f',
        },
      ).then((value) {
        if (value.statusCode == 200) {
          var json =
              jsonDecode(value.body.toString()).cast<Map<String, dynamic>>();
          data_rel = json
              .map((user) => {
                    'name': user['userName'].toString(),
                    'governorate': user['governorate'].toString(),
                    'followers': int.parse(
                        user['userStats']['followers_count'].toString()),
                    'score': min(
                        double.parse(user['relevancyScore'].toString()) + 0.12,
                        1),
                    'id': user['userId'].toString(),
                  })
              .toList();
          return 'done';
        } else {
          throw Exception('Failed to load users');
        }
      });
      return response.toString();
    }

    await Future.wait([getRel(), getNat()]);
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
                  text: currentTable.value + ' table',
                  color: dark,
                  weight: FontWeight.bold,
                  size: 24,
                ),
                Flexible(
                  child: Row(
                    children: [
                      Flexible(
                        child: Container(),
                        flex: 15,
                      ),
                      TextButton(
                        style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (currentTable.value == 'Nationalistic') {
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
                          data.value = data_nat;
                          currentTable.value = 'Nationalistic';
                        },
                        child: RichText(
                          text: TextSpan(
                            text: 'Nationalistic',
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
                          backgroundColor:
                              MaterialStateProperty.resolveWith<Color?>(
                            (Set<MaterialState> states) {
                              if (currentTable.value == 'Relevancy') {
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
                          data.value = data_rel;
                          currentTable.value = 'Relevancy';
                        },
                        child: RichText(
                          text: TextSpan(
                            text: 'Relevancy',
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
                          smRatio: 0.2,
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
                                text: " Name",
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
                              onSort: sortByFollowers,
                              label: CustomText(
                                text: "Followers",
                                size: 22,
                                weight: FontWeight.bold,
                              ),
                              size: ColumnSize.M,
                            ),
                            DataColumn2(
                              onSort: sortByScore,
                              label: CustomText(
                                text: '$currentTable' + ' score',
                                size: 22,
                                align: TextAlign.left,
                                weight: FontWeight.bold,
                              ),
                              size: ColumnSize.M,
                            ),
                          ],
                          rows: List<DataRow>.generate(data.length, (index) {
                            var name = data[index]['name'];
                            var gover = data[index]['governorate'];
                            var followers = data[index]['followers'].toString();
                            var score = data[index]['score'].toString();
                            var userID = data[index]['id'];
                            int realIdx = index + 1;
                            print(realIdx);
                            String _url = 'https://www.tiktok.com/@' + name;
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
                            DataCell nameDataCell = DataCell(
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
                                    if (!await launch(_url))
                                      throw 'Could not launch $_url';
                                  },
                                  child: RichText(
                                    text: TextSpan(
                                      text: name,
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
                                    flex: 6,
                                    child: Container(),
                                  ),
                                ],
                              ),
                            );
                            DataCell followersDataCell = DataCell(
                              Row(
                                children: [
                                  Flexible(
                                    flex: 1,
                                    child: Container(),
                                  ),
                                  RichText(
                                    text: TextSpan(
                                      text: followers,
                                      style: GoogleFonts.merriweather(
                                        fontSize: 18,
                                        fontWeight: FontWeight.normal,
                                      ),
                                    ),
                                  ),
                                  Flexible(
                                    flex: 10,
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
                                      text: score.substring(0, 5),
                                      style: GoogleFonts.merriweather(
                                        fontSize: 18,
                                        fontWeight: FontWeight.normal,
                                      ),
                                    ),
                                  ),
                                  Flexible(
                                    flex: 9,
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
                                    return resolveColor(states, index);
                                  }),
                                  cells: [
                                    rankDataCellFirst,
                                    nameDataCell,
                                    goverDataCell,
                                    followersDataCell,
                                    scoreDataCell,
                                  ]);
                            } else if ((index < 3) && (sortedByScore)) {
                              return DataRow(
                                  color:
                                      MaterialStateProperty.resolveWith<Color?>(
                                          (Set<MaterialState> states) {
                                    return resolveColor(states, index);
                                  }),
                                  cells: [
                                    rankDataCellTop,
                                    nameDataCell,
                                    goverDataCell,
                                    followersDataCell,
                                    scoreDataCell,
                                  ]);
                            } else {
                              return DataRow(
                                  color:
                                      MaterialStateProperty.resolveWith<Color?>(
                                          (Set<MaterialState> states) {
                                    return resolveColor(states, index);
                                  }),
                                  cells: [
                                    rankDataCell,
                                    nameDataCell,
                                    goverDataCell,
                                    followersDataCell,
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
