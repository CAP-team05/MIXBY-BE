import 'package:flutter/material.dart';
import 'drink_bar.dart'; // 기존 코드에서 이 파일을 import
import 'menu.dart'; // 추가한 menu.dart 파일 import

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
  bool _isDialogVisible = false; // 대화 박스 표시 여부
  String _currentDialogue = ""; // 현재 대화 내용
  List<String> _dialogue = [ // 대화 내용 리스트
    "안녕하세요!",
    "오늘은 어떤 술이 드시고 싶으신가요?",
    "오늘 날씨와 가장 잘 어울리는 술을 제가 추천해드릴게요!",
  ];
  int _dialogueIndex = 0; // 현재 대화 인덱스

  @override
  void initState() {
    super.initState();
    _startBlinkAnimation();
  }

  void _startBlinkAnimation() {
    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        _isVisible = !_isVisible;
      });
      _startBlinkAnimation();
    });
  }

  void _toggleDialog() {
    if (_dialogueIndex < _dialogue.length) {
      setState(() {
        _currentDialogue = ""; // 이전 대화 내용 초기화
        _isDialogVisible = true; // 대화 박스 표시
      });

      // 한 글자씩 나타내는 애니메이션
      String dialogue = _dialogue[_dialogueIndex];
      int dialogueLength = dialogue.length;

      for (int i = 0; i < dialogueLength; i++) {
        Future.delayed(Duration(milliseconds: 100 * i), () {
          setState(() {
            // 한 글자씩 추가하되, 줄바꿈 문자를 처리
            if (dialogue[i] == '\n') {
              _currentDialogue += '\n'; // 줄바꿈 처리
            } else {
              _currentDialogue += dialogue[i]; // 문자를 추가
            }
          });

          // 마지막 글자가 추가되면 다음 대화로 이동
          if (i == dialogueLength - 1) {
            _dialogueIndex++; // 다음 대화로 이동
          }
        });
      }
    } else {
      setState(() {
        _isDialogVisible = false; // 모든 대화가 끝나면 대화 박스 숨기기
      });
    }
  }



  @override
  Widget build(BuildContext context) {
    // MediaQuery를 사용하여 화면 너비를 가져옴
    double screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      body: Center(
        child: Container(
          width: screenWidth, // 화면 너비에 맞춤
          height: 844,
          color: Colors.white,
          child: Stack(
            children: [
              Positioned(
                left: 0,
                top: 0,
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
              Positioned(
                left: 0,
                top: 0,
                child: Container(
                  width: screenWidth,
                  height: 300,
                  decoration: BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage('assets/image/image1.png'),
                      fit: BoxFit.fill,
                    ),
                  ),
                ),
              ),
              Positioned(
                left: 0,
                top: 150,
                child: GestureDetector(
                  onTap: _toggleDialog,
                  child: Container(
                    width: screenWidth,
                    height: 150,
                    decoration: BoxDecoration(
                      image: DecorationImage(
                        image: AssetImage('assets/image/image2.png'),
                        fit: BoxFit.fill,
                      ),
                    ),
                  ),
                ),
              ),
              Positioned(
                child: DrinkBar(),
              ),
              Positioned(
                left: 0,
                top: 600,
                child: Container(
                  width: 250,
                  height: 120,
                  child: Stack(
                    children: [],
                  ),
                ),
              ),
              Positioned(
                right: 30,
                bottom: 560,
                child: AnimatedOpacity(
                  opacity: _isVisible ? 1.0 : 0.0,
                  duration: const Duration(milliseconds: 500),
                  child: GestureDetector(
                    onTap: _toggleDialog,
                    child: CustomPaint(
                      size: Size(15, 15),
                      painter: TriangleButtonPainter(),
                    ),
                  ),
                ),
              ),
              // 대화 박스 추가
              if (_isDialogVisible)
                Positioned(
                  left: 0,
                  top: 190,
                  child: Container(
                    width: screenWidth,
                    padding: const EdgeInsets.all(16),
                    color: Colors.transparent,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          _currentDialogue,
                          style: TextStyle(
                            fontFamily: 'DungGeunMo', // DungGeunMo 폰트 설정
                            fontSize: 21, // 폰트 크기 설정
                            fontWeight: FontWeight.bold,
                          ),
                          textAlign: TextAlign.left, // 텍스트 정렬
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: Menu(),
    );
  }
}

class TriangleButtonPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.black;

    final path = Path()
      ..moveTo(size.width / 2, size.height)
      ..lineTo(size.width, 0)
      ..lineTo(0, 0)
      ..close();

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}
