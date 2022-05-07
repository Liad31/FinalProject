import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:flutter/material.dart';
import 'dart:math';
import '../../../widgets/tiktok_embedd.dart';

class Graph extends StatelessWidget {
  Graph({Key? key}) : super(key: key);
  final _tooltipBehavior = TooltipBehavior(
      enable: true,
      duration: 5000,
      // Templating the tooltip
      builder: (dynamic data, dynamic point, dynamic series, int pointIndex,
          int seriesIndex) {
        return Container(
            child: TiktokEmbedd(
                src: data.vid,
                color: Colors.green,
                text: "score: ${data.score}"));
      });
  final _zoomPanBehavior = ZoomPanBehavior(
    enableMouseWheelZooming: true,
    zoomMode: ZoomMode.x,
    enablePanning: true,
  );

  final _selectionBehavior = SelectionBehavior(
    enable: true,
  );

  final List<DailyNationalisticData> _chartData = getChartData();
  @override
  Widget build(BuildContext context) {
    return Center(
        child: Container(
            child: SfCartesianChart(
                onSelectionChanged: (SelectionArgs args) {
                  args.selectedColor = Colors.red;
                  args.unselectedColor = Colors.lightGreen;
                },
                tooltipBehavior: _tooltipBehavior,
                zoomPanBehavior: _zoomPanBehavior,
                primaryXAxis: DateTimeAxis(
                    intervalType: DateTimeIntervalType.days, interval: 1),
                primaryYAxis: NumericAxis(minimum: 0, maximum: 1),
                series: <ChartSeries>[
          SplineSeries<DailyNationalisticData, DateTime>(
              selectionBehavior: _selectionBehavior,
              dataSource: _chartData,
              xValueMapper: (DailyNationalisticData data, _) => data.date,
              yValueMapper: (DailyNationalisticData data, _) => data.score,
              markerSettings: const MarkerSettings(
                  isVisible: true, shape: DataMarkerType.circle)),
        ])));
  }
}

class DailyNationalisticData {
  DailyNationalisticData(this.score, this.date, this.vid);

  final double score;
  final DateTime date;
  final String vid;
}

List<DailyNationalisticData> getChartData() {
  DateTime start = DateTime.utc(2022, 1, 1);
  Random random = Random();
  // final List<DailyNationalisticData> chartData = [
  //   DailyNationalisticData(
  //       0.9, DateTime.utc(2022, 11, 9), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.8, DateTime.utc(2022, 11, 10), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.85, DateTime.utc(2022, 11, 11), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.7, DateTime.utc(2022, 11, 12), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.6, DateTime.utc(2022, 11, 13), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.5, DateTime.utc(2022, 11, 14), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.6, DateTime.utc(2022, 11, 15), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.7, DateTime.utc(2022, 11, 16), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.75, DateTime.utc(2022, 11, 17), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.9, DateTime.utc(2022, 11, 18), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.8, DateTime.utc(2022, 11, 19), "6718335390845095173"),
  //   DailyNationalisticData(
  //       0.85, DateTime.utc(2022, 11, 20), "6718335390845095173"),
  // ];
  final List<DailyNationalisticData> chartData =
      List<DailyNationalisticData>.generate(
          360,
          (index) => DailyNationalisticData(sin(index / 10) / 3 + 0.5,
              start.add(Duration(days: index)), "6718335390845095173"));
  return chartData;
}
