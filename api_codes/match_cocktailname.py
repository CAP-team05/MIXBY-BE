from rapidfuzz import process
import json


def match_cocktail_in_json(cocktail_list, response_str):
    response = json.loads(response_str)

    # 매칭 로직
    name_list = cocktail_list.split(', ')
    for item in response['recommendation']:
        if item['name'] not in name_list:
            match = process.extractOne(item['name'], name_list)
            if match:
                item['name'] = match[0]
    return response_str
# test case for match_cocktail_in_json
# _cocktail_list = "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니, 블랙 러시안, 롱 아일랜드 아이스티, 준벅, 미도리사워, 마가리타, 블루 라군"
# _response = {"recommendation":[{"name":"미도리사워","tag":"가을","reason":"가을의 쌀쌀한 밤에 달콤함과 신선함을 더해줘요."},{"name":"블루 라군","tag":"저녁","reason":"한 잔으로 저녁을 특별하게, 달콤한 느낌이 물씬!"},{"name":"핀콜라다","tag":"눈","reason":"눈 내리는 날, 달콤함과 함께 열대 섬의 기분을!"},{"name":"모스크뮬","tag":"행복","reason":"상큼한 생강과 라임이 행복한 기분을 더해줄 거예요."},{"name":"롱 아일랜드 아이스티","tag":"피곤","reason":"강력한 조화로 피로를 날려버리기에 제격이에요."},{"name":"마가리타","tag":"화남","reason":"상큼한 맛으로 기분 전환, 스트레스를 잊게 해주죠."},{"name":"보드카토닉","tag":"바쁨","reason":"간편하면서도 시원한 느낌, 바쁜 시간에 딱이에요!"},{"name":"준벅","tag":"한가","reason":"여유롭게 한 잔하며 즐기기 좋은 달콤함을 가졌죠."},{"name":"스크류 드라이버","tag":"여행","reason":"여행의 추억을 떠올리며 상큼한 오렌지 맛을!"}]}
# print(match_cocktail_in_json(_cocktail_list, _response))