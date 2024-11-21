import 'package:flutter/material.dart';

class RoundedScreenWithBackground extends StatelessWidget {
  final double containerHeight;

  const RoundedScreenWithBackground({
    Key? key,
    this.containerHeight = 400,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Stack(
        children: [
          // 배경 색상
          Container(
            width: double.infinity,
            height: double.infinity,
            color: const Color(0xFF32325D),
          ),
          // 둥근 화면
          Positioned(
            top: 0,
            left: 0,
            child: Container(
              width: screenWidth,
              height: containerHeight,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment(0.00, -1.00),
                  end: Alignment(0, 1),
                  colors: [
                    const Color(0xFF595981),
                    const Color(0xFF32325D),
                    const Color(0xFF060926),
                  ],
                ),
                borderRadius: const BorderRadius.vertical(
                  bottom: Radius.circular(40),
                ),
                image: const DecorationImage(
                  image: AssetImage('assets/main_img.png'),
                  fit: BoxFit.cover,
                ),
              ),
            ),
          ),
          // 텍스트와 이미지 컨테이너
          Positioned(
            top: containerHeight - 30,
            left: (screenWidth - 390) / 2,
            child: Container(
              width: 390,
              height: 85,
              child: Stack(
                children: [
                  // 배경 둥근 컨테이너
                  Positioned(
                    left: 10,
                    top: 0,
                    child: Container(
                      width: 368,
                      height: 85,
                      decoration: ShapeDecoration(
                        color: const Color(0xE532325D),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(180),
                        ),
                        shadows: [
                          const BoxShadow(
                            color: Color(0x3F000000),
                            blurRadius: 4,
                            offset: Offset(0, 4),
                            spreadRadius: 0,
                          )
                        ],
                      ),
                    ),
                  ),
                  // 텍스트
                  Positioned(
                    left: 112,
                    top: 15,
                    child: SizedBox(
                      width: 250,
                      height: 40,
                      child: Text(
                        '한적한 금요일 저녁,\n취기를 원하신다면..',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontFamily: 'GyeonggiBatangOTF',
                          fontWeight: FontWeight.w400,
                          height: 1.5,
                        ),
                      ),
                    ),
                  ),
                  // bartender_point 이미지
                  Positioned(
                    left: 25,
                    top: 5,
                    child: Container(
                      width: 60,
                      height: 70,
                      decoration: BoxDecoration(
                        image: const DecorationImage(
                          image: AssetImage('assets/bartender_point.png'),
                          fit: BoxFit.fill,
                        ),
                        shape: BoxShape.circle,
                        boxShadow: [
                          const BoxShadow(
                            color: Color(0x3F000000),
                            blurRadius: 4,
                            offset: Offset(0, 4),
                            spreadRadius: 0,
                          )
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          // 칵테일 메뉴: 첫 번째 줄
          Positioned(
            top: containerHeight + 70,
            left: 0,
            right: 0,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    cocktailCard('갓파더', '#묵직 #스모키', 'assets/godfather.png'),
                    const SizedBox(width: 16),
                    cocktailCard('준벅', '#산도 #묵직', 'assets/june_bug.png'),
                    const SizedBox(width: 16),
                    cocktailCard('모스크 뮬', '#강한 도수 #묵직', 'assets/moscow_mule.png'),
                  ],
                ),
              ),
            ),
          ),
          // 칵테일 메뉴: 두 번째 줄
          Positioned(
            top: containerHeight + 350,
            left: 0,
            right: 0,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    cocktailCard('진 토닉', '#깔끔 #쓴맛', 'assets/jin_tonic.png'),
                    const SizedBox(width: 16),
                    cocktailCard('스크류 드라이버', '#상큼 #오렌지', 'assets/screwdriver.png'),
                  ],
                ),
              ),
            ),
          ),
          // 메뉴바 추가
          Positioned(
            bottom: 40,
            left: (screenWidth - 301) / 2,
            child: Opacity(
              opacity: 0.90,
              child: Container(
                width: 301,
                height: 73,
                child: Stack(
                  children: [
                    // 배경 컨테이너
                    Positioned(
                      left: 0,
                      top: 0,
                      child: Container(
                        width: 301,
                        height: 73,
                        decoration: ShapeDecoration(
                          color: const Color(0xFF070A21),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(57),
                          ),
                        ),
                      ),
                    ),
                    // 메뉴 선택 표시
                    Positioned(
                      left: 33,
                      top: 60,
                      child: Container(
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          image: const DecorationImage(
                            image: AssetImage('assets/menu_selection.png'),
                            fit: BoxFit.fill,
                          ),
                        ),
                      ),
                    ),
                    // 메뉴 아이콘
                    Positioned(
                      left: 20,
                      top: 10,
                      child: Container(
                        width: 40,
                        height: 40,
                        child: Stack(
                          children: [
                            Positioned.fill(
                              child: Image.asset('assets/light.png'),
                            ),
                            Positioned.fill(
                              child: Image.asset('assets/selected.png'),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Positioned(
                      left: 90,
                      top: 16,
                      child: Image.asset(
                        'assets/normal1.png',
                        width: 40,
                        height: 40,
                        fit: BoxFit.fill,
                      ),
                    ),
                    Positioned(
                      left: 160,
                      top: 16,
                      child: Image.asset(
                        'assets/normal2.png',
                        width: 40,
                        height: 40,
                        fit: BoxFit.fill,
                      ),
                    ),
                    Positioned(
                      left: 230,
                      top: 16,
                      child: Image.asset(
                        'assets/normal3.png',
                        width: 40,
                        height: 40,
                        fit: BoxFit.fill,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget cocktailCard(String title, String tags, String assetPath) {
    return Container(
      width: 154,
      height: 236,
      child: Stack(
        children: [
          Positioned(
            left: 0,
            top: 76,
            child: Container(
              width: 152,
              height: 160,
              decoration: ShapeDecoration(
                color: const Color(0xE51D1C38),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(19),
                ),
              ),
            ),
          ),
          Positioned(
            left: 0,
            top: 0,
            child: Container(
              width: 152,
              height: 152,
              decoration: ShapeDecoration(
                image: DecorationImage(
                  image: AssetImage(assetPath),
                  fit: BoxFit.fill,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                shadows: [
                  const BoxShadow(
                    color: Color(0x3F000000),
                    blurRadius: 4,
                    offset: Offset(0, 4),
                    spreadRadius: 0,
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            left: 0,
            top: 160,
            child: SizedBox(
              width: 152,
              height: 68,
              child: Column(
                children: [
                  Text(
                    title,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Color(0xFFFFDD45),
                      fontSize: 20,
                      fontFamily: 'GyeonggiBatangOTF',
                      fontWeight: FontWeight.w700,
                      height: 1.2,
                    ),
                  ),
                  Text(
                    tags,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Color(0xFFD0D0EE),
                      fontSize: 16,
                      fontFamily: 'GyeonggiBatangOTF',
                      fontWeight: FontWeight.w400,
                      height: 1.2,
                    ),
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

void main() {
  runApp(MaterialApp(
    home: RoundedScreenWithBackground(
      containerHeight: 400, // 둥근 화면의 높이
    ),
  ));
}
