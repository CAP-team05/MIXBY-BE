import 'package:geolocator/geolocator.dart';

class LocationToWeather {
  @override
  void init() {
    getPosition();
  }

  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permission are denied');
      }
    }

    if (permission == LocationPermission.deniedForever)
      return Future.error(
          'Location permissions are permanently denied, we cannot request permissions.');

    return await Geolocator.getCurrentPosition();
  }

  Future<Position> getPosition() async {
    var curPos = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.low);
    return curPos;
  }
}