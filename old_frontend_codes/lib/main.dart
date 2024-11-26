import 'package:flutter/material.dart';
import 'content.dart'; // content.dart에서 Content 클래스를 가져옵니다.
import 'content2.dart';

class FullWidthBackgroundScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 전체 화면 너비와 높이를 가져옴
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Stack(
        children: [
          // 그라디언트 배경
          Positioned(
            left: 0,
            top: 0,
            child: Container(
              width: screenWidth, // 화면의 전체 너비로 설정
              height: screenHeight, // 화면의 전체 높이로 설정
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment(0.00, -1.00),
                  end: Alignment(0, 1),
                  colors: [Color(0xFF32325D), Color(0xFFC4C4C4)],
                ),
              ),
            ),
          ),
          // 단색 배경
          Positioned(
            left: 0,
            top: 0,
            child: Container(
              width: screenWidth, // 화면의 전체 너비로 설정
              height: screenHeight, // 화면의 전체 높이로 설정
              decoration: BoxDecoration(
                color: Color(0xB232325D),
              ),
            ),
          ),
          // 이미지 추가
          Positioned(
            left: 10,
            top: 0, // 상단에 고정
            child: Container(
              width: 409,
              height: 409,
              decoration: BoxDecoration(
                image: DecorationImage(
                  image: AssetImage("assets/image/main_img.png"), // 로컬 이미지 경로
                  fit: BoxFit.fill,
                ),
              ),
            ),
          ),
          // 추가된 Container
          Positioned(
            left: 16, // 원하는 위치 조정
            top: 330, // 원하는 위치 조정
            child: Container(
              width: 368,
              height: 85,
              child: Stack(
                children: [
                  // 배경 모양
                  Positioned(
                    left: 0,
                    top: 0,
                    child: Container(
                      width: 368,
                      height: 85,
                      decoration: ShapeDecoration(
                        color: Color(0xE532325D),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(180),
                        ),
                        shadows: [
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
                  // 텍스트 추가
                  Positioned(
                    left: 102,
                    top: 15,
                    child: SizedBox(
                      width: 250,
                      height: 60, // 높이를 늘려서 줄바꿈이 가능하도록 설정
                      child: Text(
                        '무더운 날씨, \n이런 칵테일은 어떠세요?',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontFamily: 'GyeonggiBatangOTF',
                          fontWeight: FontWeight.w400,
                          height: 1.2, // 줄 간격 조정
                        ),
                        textAlign: TextAlign.center, // 텍스트 중앙 정렬
                      ),
                    ),
                  ),
                  // 원형 배경 추가
                  Positioned(
                    left: 7,
                    top: 5,
                    child: ClipOval(
                      child: Container(
                        width: 75,
                        height: 75,
                        decoration: BoxDecoration(
                          color: Color(0xFF545A7C), // 배경색 설정
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: Color(0x3F000000),
                              blurRadius: 4,
                              offset: Offset(0, 4),
                              spreadRadius: 0,
                            ),
                          ],
                        ),
                        child: ClipOval(
                          child: Container(
                            decoration: BoxDecoration(
                              image: DecorationImage(
                                image: AssetImage("assets/image/bartender.png"), // 로컬 이미지 경로
                                fit: BoxFit.cover, // 이미지를 잘라서 Container에 맞추기
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          // Content 위젯 추가
          Positioned(
            left: 16, // 위치 조정
            top: 440, // bartender.png 아래로 위치 조정 (원하는 위치에 맞게 조정)
            child: Content(), // content.dart에서 가져온 Content 위젯
          ),
          // Content2 위젯 추가
          Positioned(
            left: 16,
            top: 650, // Content의 아래로 위치 조정 (Content의 높이에 따라 조정)
            child: Content2(), // content2.dart에서 가져온 Content2 위젯
          ),
        ],
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: FullWidthBackgroundScreen(),
  ));
}