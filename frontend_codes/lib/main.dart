import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';

void main() async{
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: ".env");
  
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Weather Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: WeatherScreen(),
    );
  }
}

class WeatherScreen extends StatefulWidget {
  @override
  _WeatherScreenState createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  String weatherMessage = "현재 위치의 날씨를 가져오는 중...";
  final String apiKey = dotenv.env['OPEN_WEATHER_MAP_API_KEY'] ?? ''; // 여기에 OpenWeatherMap API 키를 넣으세요.

  @override
  void initState() {
    super.initState();
    _getCurrentLocationAndWeather();
  }

  Future<void> _getCurrentLocationAndWeather() async {
    bool serviceEnabled;
    LocationPermission permission;

    // 위치 서비스 활성화 여부 확인
    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      setState(() {
        weatherMessage = "위치 서비스가 비활성화되어 있습니다.";
      });
      return;
    }

    // 위치 권한 확인 및 요청
    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        setState(() {
          weatherMessage = "위치 권한이 거부되었습니다.";
        });
        return;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      setState(() {
        weatherMessage = "위치 권한이 영구적으로 거부되었습니다.";
      });
      return;
    }

    // 현재 위치 가져오기
    Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high);

    // 날씨 정보 가져오기
    await _fetchWeather(position.latitude, position.longitude);
  }

  Future<void> _fetchWeather(double latitude, double longitude) async {
    final url =
        'https://api.openweathermap.org/data/2.5/weather?lat=$latitude&lon=$longitude&units=metric&appid=$apiKey&lang=kr';

    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final description = data['weather'][0]['description'];
        final temperature = data['main']['temp'];

        setState(() {
          weatherMessage =
          "현재 온도: $temperature°C\n날씨: $description";
        });
      } else {
        setState(() {
          weatherMessage = "날씨 정보를 가져오지 못했습니다. (${response.statusCode})";
        });
      }
    } catch (e) {
      setState(() {
        weatherMessage = "날씨 정보를 가져오는 중 오류가 발생했습니다: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('현재 위치 날씨'),
      ),
      body: Center(
        child: Text(
          weatherMessage,
          style: TextStyle(fontSize: 20),
          textAlign: TextAlign.center,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _getCurrentLocationAndWeather,
        child: Icon(Icons.refresh),
      ),
    );
  }
}