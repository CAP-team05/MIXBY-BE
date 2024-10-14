import 'package:flutter/material.dart';

class Menu extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // MediaQuery를 사용하여 화면 너비를 가져옴
    double screenWidth = MediaQuery.of(context).size.width;

    return Container(
      height: 80, // 높이를 줄임
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(
            color: Colors.black, // 검은색 테두리
            width: 2, // 테두리 두께
          ),
        ),
      ),
      child: Stack(
        clipBehavior: Clip.none, // 자식 위젯이 부모의 경계를 넘을 수 있도록 설정
        children: [
          // 아이콘과 텍스트를 감싸는 Container
          Positioned(
            left: 0,
            right: 0,
            top: 10,
            child: Container(
              width: screenWidth, // 화면 너비에 맞춤
              height: 70, // 높이 설정
              decoration: ShapeDecoration(
                color: Color(0xFFD9D9D9), // 배경색 설정
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.only(
                  ),
                ),
                // 테두리 설정
                shadows: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.2), // 그림자 색상
                    blurRadius: 4, // 블러 반경
                    offset: Offset(0, 2), // 그림자 위치
                  ),
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround, // 간격 조정
                children: [
                  // My Drinks 텍스트 (왼쪽)
                  GestureDetector(
                    onTap: () {
                      // My Drinks 클릭 시 동작 추가
                    },
                    child: Column(
                      mainAxisSize: MainAxisSize.min, // 자식 크기에 맞게 설정
                      children: [
                        Text(
                          "My", // 첫 번째 부분
                          style: TextStyle(
                            fontSize: 18, // 텍스트 크기 조정 (약간 줄임)
                            fontWeight: FontWeight.bold, // 굵은 텍스트
                            color: Colors.black, // 텍스트 색상
                          ),
                        ),
                        SizedBox(height: 4), // 텍스트 간의 간격 (줄임)
                        Text(
                          "Drinks", // 두 번째 부분
                          style: TextStyle(
                            fontSize: 18, // 텍스트 크기 조정 (약간 줄임)
                            fontWeight: FontWeight.bold, // 굵은 텍스트
                            color: Colors.black, // 텍스트 색상
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Home 아이콘 (중앙)
                  GestureDetector(
                    onTap: () {
                      // 여기에서 아이콘 클릭 시 동작 추가
                    },
                    child: Container(
                      width: 250, // 아이콘 크기 조정
                      height: 250, // 아이콘 크기 조정
                      decoration: BoxDecoration(
                        color: Colors.transparent, // 투명 배경색
                      ),
                      child: Image.asset(
                        'assets/icons/glass.png', // glass 사진 경로
                        fit: BoxFit.cover, // 1:1 비율 유지
                      ),
                    ),
                  ),

                  // Recipe 텍스트 (오른쪽)
                  GestureDetector(
                    onTap: () {
                      // Recipe 클릭 시 동작 추가
                    },
                    child: Text(
                      "Recipe", // 텍스트
                      style: TextStyle(
                        fontSize: 18, // 텍스트 크기 조정 (약간 줄임)
                        fontWeight: FontWeight.bold, // 굵은 텍스트
                        color: Colors.black, // 텍스트 색상
                      ),
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
