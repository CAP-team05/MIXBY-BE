# Mixby
Mixby로 자신의 퍼스널라이징 바텐더를 만들어보세요!

![image](https://github.com/user-attachments/assets/747107a7-f835-4cd7-a6db-80dd297e0a8a)

## Introduction
이 repository는 mixby의 **백엔드**를 다룹니다.  
> [Swift Mixby](https://github.com/CAP-team05/Swift_Mixby)에서 프론트앤드 코드를 참고하세요!  
> 해당 백엔드 코드는 자체 서버에서 돌아가고 있습니다.  
> 따라서 swift mixby repository에서는 localhost가 아닌 다른 api address를 사용하고 있습니다.  

## How to test
1. 이 repository를 clone 해주세요.
```bash
git clone https://github.com/CAP-team05/Mixby
```
2. clone 받은 폴더로 이동합니다.
```bash
cd Mixby
```
3. 프로젝트 root에 `.env`파일을 만들고 안에 내용을 채워주세요.
```python
OPENAI_API_KEY=sk-proj-***************
OPENWEATHER_API_KEY=cf790*************
```
> openai api, openweathermap api 키를 발급받고 해당 부분을 채우면 됩니다.
4. 프로젝트 root에서 실행하면 됩니다.
```bash
code .
```
이후 `api_codes/runServer.py` 실행합니다.

5. library가 설치되어 있지 않다면 해당되는 library를 install 해주세요.
```bash
pip install flask
.
.
.
etc.
```

## Directory Structure
### api_codes
서버에서 실행하는 주요 코드입니다.
1. json_files  
레시피 정보, 주류 정보 등 데이터베이스를 저장해두는 폴더입니다.  
데이터의 양이 대단히 많진 않기 때문에 json으로 구현했습니다.
2. static  
이미지 파일과  같이 정적인 resource를 보관하는 폴더입니다.  
3. *.py  
서버를 돌릴 때 사용되는 코드들입니다.  
json_files, static 폴더들에서 get 요청을 통해서 값을 넘겨주거나 post 요청들을 처리하는 코드들이 작성되어 있습니다.

### backend_codes
데이터를 수집할 때 사용했던 코드입니다.

### reco_codes
추천 알고리즘을 테스트하면서 사용했던 코드입니다.

### .env
api키와 같이 보안이 필요한 key 값들을 저장해두었습니다.  
