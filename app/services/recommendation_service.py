"""
칵테일 추천 관련 서비스
"""

import os
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.cocktail_matcher import match_cocktail_in_json

load_dotenv()


class RecommendationService:
    """칵테일 추천을 담당하는 서비스 클래스"""
    
    def __init__(self):
        self.client = None
    
    def _get_client(self):
        """OpenAI 클라이언트를 지연 초기화합니다."""
        if self.client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
            self.client = OpenAI(api_key=api_key)
        return self.client
    
    def get_default_recommendation(self, persona: str, cocktail_list: str, 
                                 season: str, time: str, weather: str) -> str:
        """
        기본 추천 (계절, 시간, 날씨 기반)을 생성합니다.
        
        Args:
            persona: 사용자 페르소나
            cocktail_list: 보유한 칵테일 목록
            season: 계절
            time: 시간대  
            weather: 날씨
            
        Returns:
            추천 결과 JSON 문자열
        """
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "text": ("당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                                        "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                                        "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                                        "당신은 [계절, 시간대, 날씨]를 입력 받고 각 요소에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                                        "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                                        "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다."),
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"제공된 페르소나는 다음과 같습니다: {persona}",
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user", 
                        "content": [
                            {
                                "text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}",
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"당신은 [{season}, {time}, {weather}]에 대해서 추천합니다.",
                                "type": "text" 
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
            matched_response = match_cocktail_in_json(cocktail_list, response_content)
            
            return json.dumps(matched_response, ensure_ascii=False, indent=4)
            
        except Exception as e:
            print(f"기본 추천 생성 중 오류 발생: {e}")
            return json.dumps({"error": "추천 생성에 실패했습니다."}, ensure_ascii=False)
    
    def get_feeling_recommendation(self, persona: str, cocktail_list: str) -> str:
        """
        감정 기반 추천 (행복, 피곤, 화남)을 생성합니다.
        
        Args:
            persona: 사용자 페르소나
            cocktail_list: 보유한 칵테일 목록
            
        Returns:
            추천 결과 JSON 문자열
        """
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "text": ("당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                                        "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                                        "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                                        "당신은 [행복, 피곤, 화남] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                                        "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                                        "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다."),
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"제공된 페르소나는 다음과 같습니다: {persona}",
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}",
                                "type": "text"
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
            matched_response = match_cocktail_in_json(cocktail_list, response_content)
            
            return json.dumps(matched_response, ensure_ascii=False, indent=4)
            
        except Exception as e:
            print(f"감정 기반 추천 생성 중 오류 발생: {e}")
            return json.dumps({"error": "추천 생성에 실패했습니다."}, ensure_ascii=False)
    
    def get_situation_recommendation(self, persona: str, cocktail_list: str) -> str:
        """
        상황 기반 추천 (바쁨, 한가, 여행)을 생성합니다.
        
        Args:
            persona: 사용자 페르소나
            cocktail_list: 보유한 칵테일 목록
            
        Returns:
            추천 결과 JSON 문자열
        """
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "text": ("당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                                        "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                                        "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                                        "당신은 [바쁨, 한가, 여행] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                                        "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                                        "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다."),
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"제공된 페르소나는 다음과 같습니다: {persona}",
                                "type": "text"
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}",
                                "type": "text"
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
            matched_response = match_cocktail_in_json(cocktail_list, response_content)
            
            return json.dumps(matched_response, ensure_ascii=False, indent=4)
            
        except Exception as e:
            print(f"상황 기반 추천 생성 중 오류 발생: {e}")
            return json.dumps({"error": "추천 생성에 실패했습니다."}, ensure_ascii=False)