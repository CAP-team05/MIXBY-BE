"""
사용자 페르소나 생성 관련 서비스
"""

import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from app.services.recipe_service import RecipeService

load_dotenv()


class PersonaService:
    """사용자 페르소나 생성을 담당하는 서비스 클래스"""
    
    def __init__(self):
        self.client = None
        self.recipe_service = RecipeService()
    
    def _get_client(self):
        """OpenAI 클라이언트를 지연 초기화합니다."""
        if self.client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
            self.client = OpenAI(api_key=api_key)
        return self.client
    
    def get_drink_list_string(self, tasting_data: List[Dict[str, Any]]) -> str:
        """
        테이스팅 데이터를 문자열로 변환합니다.
        
        Args:
            tasting_data: 사용자의 테이스팅 데이터 리스트
            
        Returns:
            포맷된 드링크 리스트 문자열
        """
        drink_list = []
        
        for item in tasting_data:
            recipe = self.recipe_service.search_by_code(item.get("code", ""))
            if recipe:
                drink_info = [
                    recipe.get("korean_name", "알 수 없음"),
                    item.get("drinkDate", ""),
                    recipe.get("tag1", ""),
                    recipe.get("tag2", ""),
                    self._to_eval_string(item.get("eval", 0)),
                    self._to_eval_string(item.get("sweetness", 0)),
                    self._to_eval_string(item.get("sourness", 0)),
                    self._to_eval_string(item.get("alcohol", 0))
                ]
                
                formatted_info = "[" + ", ".join(drink_info) + "]"
                drink_list.append(formatted_info)
        
        return ", ".join(drink_list)
    
    def _to_eval_string(self, rating: int) -> str:
        """
        평점을 문자열로 변환합니다.
        
        Args:
            rating: 0-6 범위의 평점
            
        Returns:
            평점에 해당하는 문자열
        """
        eval_mapping = {
            0: "매우 불만",
            1: "대체로 불만", 
            2: "조금 불만",
            3: "보통",
            4: "조금 만족",
            5: "대체로 만족",
            6: "매우 만족"
        }
        return eval_mapping.get(rating, str(rating))
    
    def generate_persona(self, user_data: List[Dict[str, Any]], 
                        tasting_data: List[Dict[str, Any]]) -> str:
        """
        사용자 데이터와 테이스팅 데이터를 바탕으로 페르소나를 생성합니다.
        
        Args:
            user_data: 사용자 기본 정보
            tasting_data: 사용자의 테이스팅 데이터
            
        Returns:
            생성된 페르소나 문자열
        """
        if not user_data:
            raise ValueError("사용자 데이터가 필요합니다.")
        
        user_info = user_data[0]
        user_description = f"{user_info.get('name', '')}, {user_info.get('gender', '')}, {user_info.get('favoriteTaste', '')}"
        drink_list = self.get_drink_list_string(tasting_data)
        
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": ("당신은 전문 칵테일 소믈리에입니다.\n"
                                        "사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 요약하는 역할을 맡고 있습니다.\n"
                                        "사용자의 정보는 [이름, 나이, 선호하는 맛]로 입력됩니다.\n"
                                        "사용자가 먹은 칵테일은 [칵테일 이름, 사용자가 먹은 날짜, 칵테일 특징1, 칵테일 특징2, 사용자의 해당 칵테일 선호도, 해당 칵테일 단맛 평가, 해당 칵테일 산미 평가, 해당 칵테일 도수 평가]로 입력됩니다.\n"
                                        "사용자에 대한 정보와 먹어봤던 칵테일에 대한 설명을 보고 100자 정도로 사용자를 요약합니다.\n"
                                        "요약에 대한 설명은 Json으로 반환하며 태그 이름은 \"summary\"입니다.\n"
                                        "칵테일에 대한 특징을 반영한 요약을 제시합니다.")
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"사용자 정보는 다음과 같습니다: {user_description}"
                            }
                        ]
                    },
                    {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text",
                                "text": f"지금까지 사용자가 먹은 칵테일을 다음과 같습니다: {drink_list}"
                            }
                        ]
                    }
                ],
                response_format={"type": "json_object"},
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            response_content = response.choices[0].message.content
            parsed_response = json.loads(response_content)
            
            return parsed_response.get("summary", "페르소나 생성에 실패했습니다.")
            
        except Exception as e:
            print(f"페르소나 생성 중 오류 발생: {e}")
            return "페르소나 생성에 실패했습니다."