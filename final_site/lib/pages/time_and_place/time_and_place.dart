import 'package:final_site/widgets/custom_text.dart';
import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:syncfusion_flutter_charts/sparkcharts.dart';

import '../../widgets/tiktok_embedd.dart';

class TimeAndPlacePage extends StatelessWidget {
  TimeAndPlacePage({Key? key}) : super(key: key);
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

  final _selectionBehavior = SelectionBehavior(
    enable: true,
  );

  final List<DailyNatialisticData> _chartData = getChartData();
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
                primaryXAxis: DateTimeAxis(
                    intervalType: DateTimeIntervalType.days, interval: 2),
                primaryYAxis: NumericAxis(minimum: 0, maximum: 1),
                series: <ChartSeries>[
          LineSeries<DailyNatialisticData, DateTime>(
              selectionBehavior: _selectionBehavior,
              dataSource: _chartData,
              xValueMapper: (DailyNatialisticData data, _) => data.date,
              yValueMapper: (DailyNatialisticData data, _) => data.score,
              markerSettings: const MarkerSettings(
                  isVisible: true, shape: DataMarkerType.circle)),
        ])));
  }
}

class DailyNatialisticData {
  DailyNatialisticData(this.score, this.date, this.vid);

  final double score;
  final DateTime date;
  final String vid;
}

List<DailyNatialisticData> getChartData() {
  final List<DailyNatialisticData> chartData = [
    DailyNatialisticData(0.9, DateTime.utc(2022, 11, 9), "6718335390845095173"),
    DailyNatialisticData(
        0.8, DateTime.utc(2022, 11, 10), "6718335390845095173"),
    DailyNatialisticData(
        0.85, DateTime.utc(2022, 11, 11), "6718335390845095173"),
    DailyNatialisticData(
        0.7, DateTime.utc(2022, 11, 12), "6718335390845095173"),
    DailyNatialisticData(
        0.6, DateTime.utc(2022, 11, 13), "6718335390845095173"),
    DailyNatialisticData(
        0.5, DateTime.utc(2022, 11, 14), "6718335390845095173"),
    DailyNatialisticData(
        0.6, DateTime.utc(2022, 11, 15), "6718335390845095173"),
    DailyNatialisticData(
        0.7, DateTime.utc(2022, 11, 16), "6718335390845095173"),
    DailyNatialisticData(
        0.75, DateTime.utc(2022, 11, 17), "6718335390845095173"),
    DailyNatialisticData(
        0.9, DateTime.utc(2022, 11, 18), "6718335390845095173"),
    DailyNatialisticData(
        0.8, DateTime.utc(2022, 11, 19), "6718335390845095173"),
    DailyNatialisticData(
        0.85, DateTime.utc(2022, 11, 20), "6718335390845095173"),
  ];
  return chartData;
}
