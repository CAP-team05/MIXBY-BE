import 'package:flutter/material.dart';

class DrinkBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity, // 화면 너비에 맞춤
      padding: EdgeInsets.symmetric(vertical: 10), // 위아래 패딩 추가
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal, // 수평 스크롤
        child: Row(
          children: [
            // 데킬라 선라이즈 카드
            _buildDrinkCard(
              '데킬라 선라이즈',
              '98% 일치',
              'assets/image/tequila_sunrise.png',
            ),
            // 김렛 카드
            _buildDrinkCard(
              '김렛',
              '95% 일치',
              'assets/image/gimlet.png',
            ),
            // 골드러쉬 카드
            _buildDrinkCard(
              '골드러쉬',
              '92% 일치',
              'assets/image/gold_rush.png',
            ),
          ],
        ),
      ),
    );
  }

  // 칵테일 카드 위젯을 생성하는 헬퍼 메서드
  Widget _buildDrinkCard(String name, String matchPercent, String imagePath) {
    return Container(
      margin: EdgeInsets.only(right: 10, top: 300), // 카드 간 간격 조정 및 아래쪽 간격 추가
      width: 160, // 카드 너비
      height: 200, // 카드 높이 조정
      decoration: BoxDecoration(
        border: Border.all(color: Colors.black, width: 2), // 검은 테두리 추가
        borderRadius: BorderRadius.circular(20), // 카드 모서리 둥글게
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
          ClipRRect(
            borderRadius: BorderRadius.circular(20), // 이미지 둥글게
            child: Container(
              width: double.infinity, // 카드 너비에 맞춤
              height: double.infinity, // 카드 높이에 맞춤
              decoration: BoxDecoration(
                image: DecorationImage(
                  image: AssetImage(imagePath), // 이미지 경로
                  fit: BoxFit.cover, // 이미지 비율에 맞게 조정
                ),
              ),
            ),
          ),
          // 상단 배너 (회색 박스)
          Positioned(
            top: 0,
            child: Container(
              width: 160, // 카드 너비와 같게 설정
              height: 25, // 상단 배너 높이 조정
              decoration: ShapeDecoration(
                color: Color(0x7FB5B5B5),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(20),
                    topRight: Radius.circular(20),
                  ),
                ),
              ),
              child: Center(
                child: Text(
                  matchPercent, // 매칭 퍼센트를 상단 배너에 배치
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 14, // 폰트 크기 조정
                    fontFamily: 'GmarketSans',
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
            ),
          ),
          // 하단 배너 (회색 박스)
          Positioned(
            left: 0,
            bottom: 0,
            child: Container(
              width: 160, // 카드 너비와 같게 설정
              height: 25, // 하단 배너 높이 조정
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
          // 칵테일 이름 (하단 배너에 배치)
          Positioned(
            left: 0, // X축 중앙 조정
            bottom: 5, // 하단 배너 위에 위치
            child: Container(
              width: 160, // 카드 너비와 같게 설정
              child: Text(
                name,
                textAlign: TextAlign.center, // 텍스트 중앙 정렬
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 14, // 폰트 크기 조정
                  fontFamily: 'GmarketSans',
                  fontWeight: FontWeight.w500,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
