import 'package:flutter/material.dart';

class ReleaseView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start, // 좌측 정렬
      children: [
        // "최근 해금한 레시피에요!" 텍스트
        Container(
          alignment: Alignment.centerLeft,
          child: Text(
            '최근 해금한 레시피에요!',
            style: TextStyle(
              color: Colors.black,
              fontSize: 24,
              fontFamily: 'Gmarket Sans TTF',
              fontWeight: FontWeight.w500,
            ),
          ),
        ),
        // 음료 카드 1: 미도리 사워
        _buildDrinkCard('미도리 사워'),
        // 음료 카드 2: 잭콕
        _buildDrinkCard('잭콕'),
        // 음료 카드 3: 모히또
        _buildDrinkCard('모히또'),
      ],
    );
  }

  // 음료 카드를 만드는 함수
  Widget _buildDrinkCard(String drinkName) {
    return Container(
      width: 240,
      height: 60, // 카드 높이 조정
      margin: EdgeInsets.only(bottom: 10), // 카드 간 간격 조정
      child: Stack(
        children: [
          Positioned(
            left: 0,
            top: 0,
            child: Container(
              width: 240,
              height: 40, // 높이를 카드와 맞추기
              decoration: ShapeDecoration(
                color: Colors.white,
                shape: RoundedRectangleBorder(
                  side: BorderSide(width: 1, color: Color(0xFFC5C5C5)),
                  borderRadius: BorderRadius.circular(10),
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
          Positioned(
            left: 11,
            top: 6,
            child: Container(
              width: 25,
              height: 18,
              child: FlutterLogo(),
            ),
          ),
          Positioned(
            left: 36,
            top: 6, // 텍스트 위치 조정
            child: SizedBox(
              width: 150,
              child: Text(
                drinkName,
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 18,
                  fontFamily: 'Gmarket Sans TTF',
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
