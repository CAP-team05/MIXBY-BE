from rapidfuzz import process
import json


def match_cocktail_in_json(cocktail_list, response_str):
    response = json.loads(response_str)
    first_key = next(iter(response))

    # 매칭 로직
    name_list = cocktail_list.split(', ')
    for item in response[first_key]:
        if item['name'] not in name_list:
            match = process.extractOne(item['name'], name_list)
            if match:
                item['name'] = match[0]
    return response
# test case for match_cocktail_in_json
# _cocktail_list = "스크류 드라이버, 보드카토닉, 모스크뮬, 마티니, 블랙 러시안, 롱 아일랜드 아이스티, 준벅, 미도리사워, 마가리타, 블루 라군"
# _response = {"recommendation":[{"name":"미도리","tag":"가을","reason":"가을의 쌀쌀한 밤에 달콤함과 신선함을 더해줘요."},{"name":"블루 라군","tag":"저녁","reason":"한 잔으로 저녁을 특별하게, 달콤한 느낌이 물씬!"},{"name":"스크류","tag":"눈","reason":"눈 내리는 날, 달콤함과 함께 열대 섬의 기분을!"},{"name":"모스크  뮬","tag":"행복","reason":"상큼한 생강과 라임이 행복한 기분을 더해줄 거예요."},{"name":"롱 아일랜드 아이스티","tag":"피곤","reason":"강력한 조화로 피로를 날려버리기에 제격이에요."},{"name":"마가리타","tag":"화남","reason":"상큼한 맛으로 기분 전환, 스트레스를 잊게 해주죠."},{"name":"보드카토닉","tag":"바쁨","reason":"간편하면서도 시원한 느낌, 바쁜 시간에 딱이에요!"},{"name":"준벅","tag":"한가","reason":"여유롭게 한 잔하며 즐기기 좋은 달콤함을 가졌죠."},{"name":"스크류 드라이버","tag":"여행","reason":"여행의 추억을 떠올리며 상큼한 오렌지 맛을!"}]}
# print(match_cocktail_in_json(_cocktail_list, _response))

def check_tag(season, time, weather, response_str):
    response = json.loads(response_str)
    firstkey = next(iter(response))
    tag_list = [season, time, weather, "행복", "피곤", "화남", "바쁨", "한가", "여행"]
    
    for item in response[firstkey]:
        if item['tag'] not in tag_list:
            match = process.extractOne(item['tag'][:2], tag_list)
            print(match)
            if match:
                item['tag'] = match[0]
                
    response[firstkey].sort(key=lambda x: tag_list.index(x['tag']))    
                
    return response

# _response = {
#     "recommendation": [
#         {
#             "name": "미도리사워",
#             "tag": "가을 분위기와 잘 어울리는 달콤함",
#             "reason": "가을 저녁의 분위기를 살릴 수 있는 최고의 선택입니다."
#         },
#         {
#             "name": "모스크뮬",
#             "tag": "눈 내리는 로맨틱한 저녁에 딱",
#             "reason": "차가운 날씨에 따뜻한 느낌을 더해줍니다."
#         },
#         {
#             "name": "블루 라군",
#             "tag": "저녁에 청량감을 더해줄 칵테일",
#             "reason": "여유로운 저녁에 마시면 기분이 상쾌해질 거예요."
#         },
#         {
#             "name": "미도리사워",
#             "tag": "행복한 순간을 더욱 특별하게",
#             "reason": "달콤한 맛이 행복한 기분을 높여줄 거예요."
#         },
#         {
#             "name": "모스크뮬",
#             "tag": "피곤할 때 상큼함을 제공하는 칵테일",
#             "reason": "상큼한 생강이 피로를 잊게 해줄 거예요."
#         },
#         {
#             "name": "롱 아일랜드 아이스티",
#             "tag": "화난 마음을 가라앉혀줄 강한 칵테일",
#             "reason": "다양한 맛이 화를 잊게 해줄 수 있어요."
#         },
#         {
#             "name": "블랙 러시안",
#             "tag": "바쁠 때 간편하게 즐길 수 있는 칵테일",
#             "reason": "짧고 강렬한 한 잔으로 잠시 휴식을."
#         },
#         {
#             "name": "마가리타",
#             "tag": "한가한 순간을 즐기기 좋은 칵테일",
#             "reason": "상큼하고 달콤한 청량감으로 여유를 즐기세요."
#         },
#         {
#             "name": "스크류 드라이버",
#             "tag": "여행의 추억을 떠올리게 하는 맛",
#             "reason": "달콤하면서도 이국적인 맛으로 기분 전환!"
#         }
#     ]
# }
# print(check_tag("가을", "저녁", "눈", _response))
