import 'package:flutter/material.dart';

class Content2 extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 300, // Adjust the height as needed
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            _buildCocktailCard("assets/image/june_bug.png", "준벅", "#달콤 #향긋"),
            _buildCocktailCard("assets/image/gin_tonic.png", "진토닉", "#상큼 #청량"),
            _buildCocktailCard("assets/image/shot.png", "샷", "#강렬 #짧게"),
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
