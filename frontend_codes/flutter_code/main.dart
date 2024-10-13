import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isVisible = true;

  @override
  void initState() {
    super.initState();
    // 깜빡임 애니메이션
    _startBlinkAnimation();
  }

  void _startBlinkAnimation() {
    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        _isVisible = !_isVisible;
      });
      _startBlinkAnimation(); // 재귀적으로 호출
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          width: 390,
          height: 844,
          clipBehavior: Clip.antiAlias,
          decoration: ShapeDecoration(
            color: Colors.white,
            shape: RoundedRectangleBorder(
              side: const BorderSide(width: 1, color: Color(0xFF9D9D9D)),
              borderRadius: BorderRadius.circular(40),
            ),
          ),
          child: Stack(
            children: [
              // 이미지3 (배경 이미지, 스택의 가장 아래에 위치해야 함)
              Positioned(
                left: 0,
                top: 50,
                child: Container(
                  width: 350,
                  height: 200,
                  decoration: BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/image/image3.png'),
                      fit: BoxFit.fill,
                    ),
                  ),
                ),
              ),
              // 이미지1 (전경 이미지)
              Positioned(
                left: 0,
                top: 50,
                child: Container(
                  width: 400,
                  height: 255,
                  decoration: BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/image/image1.png'),
                      fit: BoxFit.fill,
                    ),
                  ),
                ),
              ),
              // 이미지2 (전경 이미지)
              Positioned(
                left: 0,
                top: 200,
                child: Container(
                  width: 390,
                  height: 100,
                  decoration: BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/image/image2.png'),
                      fit: BoxFit.fill,
                    ),
                  ),
                ),
              ),
              // 삼각형 버튼 (애니메이션 효과)
              Positioned(
                right: 30, // 버튼을 오른쪽으로 위치
                bottom: 560, // 버튼을 아래쪽으로 위치
                child: AnimatedOpacity(
                  opacity: _isVisible ? 1.0 : 0.0, // 깜빡임 효과
                  duration: const Duration(milliseconds: 500),
                  child: GestureDetector(
                    onTap: () {
                      // 버튼 클릭 시 추가할 기능
                    },
                    child: CustomPaint(
                      size: Size(15, 15), // 버튼 크기를 더욱 작게 설정
                      painter: TriangleButtonPainter(),
                    ),
                  ),
                ),
              ),



              //화면 밑에 음료 선호도//

              SingleChildScrollView(
                scrollDirection: Axis.horizontal, // 수평 스크롤
                child: Row(
                  children: [

                    // 데낄라 선라이즈 카드
                    // 데킬라 선라이즈 카드
                    Container(
                      margin: EdgeInsets.only(right: 10, top: 310, left: 5), // 카드 간 간격 및 위치 조정
                      width: 236,
                      height: 266,
                      decoration: BoxDecoration(
                        boxShadow: [
                          BoxShadow(
                            color: Color(0x3F000000),
                            blurRadius: 4,
                            offset: Offset(0, 4),
                            spreadRadius: 0,
                          ),
                        ],
                      ),
                      child: Stack(
                        children: [
                          // 이미지 부분
                          Container(
                            width: 236,
                            height: 266,
                            decoration: ShapeDecoration(
                              image: DecorationImage(
                                image: AssetImage("assets/image/tequila_sunrise.png"), // Tequila Sunrise 이미지
                                fit: BoxFit.fill,
                              ),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                          ),
                          // 상단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            top: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    topLeft: Radius.circular(20),
                                    topRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          // 칵테일 이름
                          Positioned(
                            left: 65,
                            bottom: 5,
                            child: Text(
                              '데킬라 선라이즈',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 매칭 퍼센트
                          Positioned(
                            left: 87,
                            top: 5,
                            child: Text(
                              '89% 일치',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 하단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            left: 0,
                            bottom: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    bottomLeft: Radius.circular(20),
                                    bottomRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),

                    // 김렛 카드
                    Container(
                      margin: EdgeInsets.only(right: 10, top: 310, left: 5), // 카드 간 간격 및 위치 조정
                      width: 236,
                      height: 266,
                      decoration: BoxDecoration(
                        boxShadow: [
                          BoxShadow(
                            color: Color(0x3F000000),
                            blurRadius: 4,
                            offset: Offset(0, 4),
                            spreadRadius: 0,
                          ),
                        ],
                      ),
                      child: Stack(
                        children: [
                          // 이미지 부분
                          Container(
                            width: 236,
                            height: 266,
                            decoration: ShapeDecoration(
                              image: DecorationImage(
                                image: AssetImage("assets/image/gimlet.png"), // Gimlet 이미지
                                fit: BoxFit.fill,
                              ),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                          ),
                          // 상단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            top: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    topLeft: Radius.circular(20),
                                    topRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          // 칵테일 이름
                          Positioned(
                            left: 100,
                            bottom: 5,
                            child: Text(
                              '김렛',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 매칭 퍼센트
                          Positioned(
                            left: 87,
                            top: 5,
                            child: Text(
                              '95% 일치',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 하단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            left: 0,
                            bottom: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    bottomLeft: Radius.circular(20),
                                    bottomRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),

                    // 골드러쉬 카드
                    Container(
                      margin: EdgeInsets.only(right: 10, top: 310, left: 5), // 카드 간 간격 및 위치 조정
                      width: 236,
                      height: 266,
                      decoration: BoxDecoration(
                        boxShadow: [
                          BoxShadow(
                            color: Color(0x3F000000),
                            blurRadius: 4,
                            offset: Offset(0, 4),
                            spreadRadius: 0,
                          ),
                        ],
                      ),
                      child: Stack(
                        children: [
                          // 이미지 부분
                          Container(
                            width: 236,
                            height: 266,
                            decoration: ShapeDecoration(
                              image: DecorationImage(
                                image: AssetImage("assets/image/gold_rush.png"), // Gold Rush 이미지
                                fit: BoxFit.fill,
                              ),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(20),
                              ),
                            ),
                          ),
                          // 상단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            top: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    topLeft: Radius.circular(20),
                                    topRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                          // 칵테일 이름
                          Positioned(
                            left: 90,
                            bottom: 5,
                            child: Text(
                              '골드러쉬',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 매칭 퍼센트
                          Positioned(
                            left: 87,
                            top: 5,
                            child: Text(
                              '92% 일치',
                              style: TextStyle(
                                color: Colors.black,
                                fontSize: 16,
                                fontFamily: 'Gmarket Sans TTF',
                                fontWeight: FontWeight.w500,
                                height: 0,
                              ),
                            ),
                          ),
                          // 하단 배너 (회색 박스) - 이미지 위에 위치하도록 순서 수정
                          Positioned(
                            left: 0,
                            bottom: 0,
                            child: Container(
                              width: 236,
                              height: 30,
                              decoration: ShapeDecoration(
                                color: Color(0x7FB5B5B5),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.only(
                                    bottomLeft: Radius.circular(20),
                                    bottomRight: Radius.circular(20),
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

            ],
          ),
        ),
      ),
    );
  }
}

class TriangleButtonPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.black; // 삼각형 버튼 색상

    final path = Path()
      ..moveTo(size.width / 2, size.height) // 꼭짓점 (아래쪽)
      ..lineTo(size.width, 0) // 오른쪽 꼭짓점
      ..lineTo(0, 0) // 왼쪽 꼭짓점
      ..close(); // 삼각형을 완성

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}
