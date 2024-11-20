import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: MyCustomLayout(),
      ),
    );
  }
}

class MyCustomLayout extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 화면 크기 정보 가져오기
    final screenSize = MediaQuery.of(context).size;

    return SingleChildScrollView(  // 스크롤을 가능하게 하기 위해 추가
      child: Column(
        children: [
          // 첫 번째 Stack - 그라디언트 배경과 이미지
          Stack(
            children: [
              // 두 번째 Container (Gradient 배경)
              Positioned.fill( // Stack 내에서 채워지도록 설정
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(40),
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Color(0xff595981),
                        Color(0xff32325d),
                        Color(0xff060926),
                      ],
                    ),
                  ),
                ),
              ),
              // 배경 색상
              Container(
                width: screenSize.width,  // 전체 화면 너비
                height: screenSize.height, // 전체 화면 높이
                decoration: BoxDecoration(
                  color: Color(0xff32325d),
                ),
              ),
              // 투명 배경색
              Container(
                width: screenSize.width,  // 전체 화면 너비
                height: screenSize.height, // 전체 화면 높이
                decoration: BoxDecoration(
                  color: Color(0x991d1c38),
                ),
              ),
              // main_img.png 이미지를 Stack 안에서 가장 앞에 배치
              Positioned(
                left: 0,
                top: 0,
                child: Image.asset(
                  "assets/main_img.png",
                  width: screenSize.width, // 전체 화면 너비로 확장
                  height: screenSize.height * 0.5, // 높이를 50%로 설정
                  fit: BoxFit.cover, // 이미지 크기 비율에 맞춰 보정
                ),
              ),
              // 새로운 Container 추가
              Positioned(
                left: 10,
                top: screenSize.height * 0.5,  // main_img 아래에 배치
                child: Container(
                  width: 390,
                  height: 85,
                  child: Stack(
                    children: [
                      Positioned(
                        left: 10,
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
                              )
                            ],
                          ),
                        ),
                      ),
                      Positioned(
                        left: 112,
                        top: 15,
                        child: SizedBox(
                          width: 250,
                          height: 40,
                          child: Text(
                            '한적한 금요일 저녁,\n취기를 원하신다면..',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                              fontFamily: 'GyeonggiBatangOTF',
                              fontWeight: FontWeight.w400,
                              height: 0.08,
                            ),
                          ),
                        ),
                      ),
                      Positioned(
                        left: 17,
                        top: 5,
                        child: Container(
                          width: 75,
                          height: 75,
                          decoration: ShapeDecoration(
                            color: Color(0xFF545A7C),
                            shape: OvalBorder(),
                            shadows: [
                              BoxShadow(
                                color: Color(0x3F000000),
                                blurRadius: 4,
                                offset: Offset(0, 4),
                                spreadRadius: 0,
                              )
                            ],
                          ),
                        ),
                      ),
                      Positioned(
                        left: 33,
                        top: 15,
                        child: Container(
                          width: 43,
                          height: 53.96,
                          decoration: BoxDecoration(
                            image: DecorationImage(
                              image: AssetImage("bartender_point.png"),
                              fit: BoxFit.fill,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
