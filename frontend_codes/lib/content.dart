import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Mixby'),
        ),
        body: Center(
          child: Container(
            margin: EdgeInsets.only(top: 20), // 전체 프레임 위로 올리기 위한 여백
            height: 300, // 전체 프레임의 높이 조정
            child: Content(), // Content 위젯 사용
          ),
        ),
      ),
    );
  }
}

class Content extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Container(
        width: MediaQuery.of(context).size.width * 2,
        height: 237,
        child: Row(
          children: [
            _buildCocktailCard("assets/image/moscow_mule.png", "모스크 뮬", "#묵직 #스모키"),
            _buildCocktailCard("assets/image/screw_driver.png", "스크류 드라이버", "#상큼 #오렌지"),
            _buildCocktailCard("assets/image/margarita.png", "마르가리따", "#상큼 #레몬"),
          ],
        ),
      ),
    );
  }

  Widget _buildCocktailCard(String imagePath, String cocktailName, String hashtags) {
    return Container(
      width: 160,
      height: 230,
      margin: EdgeInsets.only(right: 10),
      child: Stack(
        children: [
          Positioned(
            left: 0,
            top: 70,
            child: Container(
              width: 152,
              height: 160,
              decoration: BoxDecoration(
                color: Color(0xE51D1C38),
                borderRadius: BorderRadius.circular(19),
              ),
            ),
          ),
          Positioned(
            left: 0,
            top: 160,
            child: Container(
              width: 160,
              height: 70,
              child: Stack(
                children: [
                  Positioned(
                    left: 0,
                    top: 40,
                    child: SizedBox(
                      width: 160,
                      height: 30,
                      child: Text(
                        hashtags,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Color(0xFFD0D0EE),
                          fontSize: 16,
                          fontFamily: 'GyeonggiBatangOTF',
                          fontWeight: FontWeight.w400,
                          height: 0.08,
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    left: 0,
                    top: 10,
                    child: SizedBox(
                      width: 163,
                      height: 40,
                      child: Text(
                        cocktailName,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Color(0xFFFFDD45),
                          fontSize: 20,
                          fontFamily: 'GyeonggiBatangOTF',
                          fontWeight: FontWeight.w700,
                          height: 0.07,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            left: 0,
            top: 0,
            child: Container(
              width: 152,
              height: 152,
              decoration: BoxDecoration(
                image: DecorationImage(
                  image: AssetImage(imagePath),
                  fit: BoxFit.fill,
                ),
                borderRadius: BorderRadius.circular(30),
                boxShadow: [
                  BoxShadow(
                    color: Color(0x3F000000),
                    blurRadius: 4,
                    offset: Offset(0, 4),
                    spreadRadius: 0,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
