"""
칵테일 추천 관련 서비스
"""

import os
import json
import logging
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.cocktail_matcher import match_cocktail_in_json

load_dotenv()
logger = logging.getLogger(__name__)


class RecommendationService:
    """칵테일 추천을 담당하는 서비스 클래스"""

    def __init__(self):
        self.client = None
        self.rag_service = None
        use_rag_env = os.getenv("USE_RAG", "false")
        self.use_rag = use_rag_env.lower() == "true" if use_rag_env else False

        # RAG 사용 설정일 때만 초기화
        if self.use_rag:
            from app.services.rag_service import RAGService

            self.rag_service = RAGService()

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

            # RAG를 사용하는 경우
            use_rag_for_request = self.use_rag and self.rag_service
            if use_rag_for_request:
                # cocktail_list를 파싱하여 code 리스트 추출
                cocktail_codes = self._parse_cocktail_codes(cocktail_list)

                # codes가 비어있으면 이 요청에서만 RAG 사용 안 함
                if not cocktail_codes:
                    logger.warning("cocktail codes가 비어있어 이 요청에서는 RAG를 사용하지 않습니다")
                    use_rag_for_request = False

            if use_rag_for_request:
                # 계절, 시간, 날씨에 대해 RAG 검색 수행
                contexts = [season, time, weather]
                context_names = ["계절", "시간대", "날씨"]
                rag_contexts = []
                selected_cocktail_codes = set()  # 이미 선택된 칵테일 추적

                for i, context in enumerate(contexts):
                    query = f"{context}에 어울리는 칵테일"

                    # 이미 선택된 칵테일을 제외한 목록으로 검색
                    available_codes = [code for code in cocktail_codes if code not in selected_cocktail_codes]

                    # 사용 가능한 칵테일이 없으면 전체 목록 사용
                    search_codes = available_codes if available_codes else cocktail_codes

                    relevant_cocktails = self.rag_service.search_cocktails(
                        query=query, n_results=5, cocktail_list=search_codes
                    )

                    if relevant_cocktails:
                        context_text = f"\n[{context_names[i]}: {context}에 어울리는 칵테일]\n"
                        for cocktail in relevant_cocktails[:3]:  # 상위 3개만
                            context_text += f"- {cocktail.get('english_name', '')}\n"
                            # 첫 번째 칵테일을 선택된 것으로 표시 (다음 검색에서 제외)
                            if cocktail.get('code'):
                                selected_cocktail_codes.add(str(cocktail.get('code')))
                                break  # 각 컨텍스트마다 1개만 선택
                        rag_contexts.append(context_text)

                # RAG 검색 결과를 프롬프트에 포함
                rag_context_text = "\n".join(rag_contexts)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [계절, 시간대, 날씨]를 입력 받고 각 요소에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    f"아래는 각 요소에 추천 가능한 칵테일 목록입니다:\n{rag_context_text}\n"
                    "추천은 반드시 위 목록에 있는 칵테일의 영어 이름만 사용하세요. 다른 칵테일을 추천하지 마세요.\n"
                    "중요 규칙:\n"
                    "1. \"name\" 필드에는 반드시 위 목록의 영어 칵테일 이름만 정확히 입력하세요.\n"
                    "2. 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요.\n"
                    "3. 첫 번째는 계절에 어울리는 칵테일, 두 번째는 시간대에 어울리는 칵테일, 세 번째는 날씨에 어울리는 칵테일을 각각 다르게 추천하세요."
                )
            else:
                # 기존 방식 (RAG 미사용)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [계절, 시간대, 날씨]를 입력 받고 각 요소에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다.\n"
                    "중요: 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요."
                )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": [{"text": system_prompt, "type": "text"}]},
                    {
                        "role": "user",
                        "content": [{"text": f"제공된 페르소나는 다음과 같습니다: {persona}", "type": "text"}],
                    },
                    {
                        "role": "user",
                        "content": [{"text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}", "type": "text"}],
                    },
                    {
                        "role": "user",
                        "content": [{"text": f"당신은 [{season}, {time}, {weather}]에 대해서 추천합니다.", "type": "text"}],
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            response_content = response.choices[0].message.content
            matched_response = match_cocktail_in_json(cocktail_list, response_content)

            return json.dumps(matched_response, ensure_ascii=False, indent=4)

        except Exception as e:
            logger.error(f"기본 추천 생성 중 오류 발생: {e}", exc_info=True)
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

            # RAG를 사용하는 경우
            use_rag_for_request = self.use_rag and self.rag_service
            if use_rag_for_request:
                # cocktail_list를 파싱하여 code 리스트 추출
                cocktail_codes = self._parse_cocktail_codes(cocktail_list)

                # codes가 비어있으면 이 요청에서만 RAG 사용 안 함
                if not cocktail_codes:
                    logger.warning("cocktail codes가 비어있어 이 요청에서는 RAG를 사용하지 않습니다")
                    use_rag_for_request = False

            if use_rag_for_request:
                # 각 감정에 대해 RAG 검색 수행
                feelings = ["행복", "피곤", "화남"]
                rag_contexts = []
                selected_cocktail_codes = set()  # 이미 선택된 칵테일 추적

                for feeling in feelings:
                    query = f"{feeling}한 감정에 어울리는 칵테일"

                    # 이미 선택된 칵테일을 제외한 목록으로 검색
                    available_codes = [code for code in cocktail_codes if code not in selected_cocktail_codes]

                    # 사용 가능한 칵테일이 없으면 전체 목록 사용
                    search_codes = available_codes if available_codes else cocktail_codes

                    relevant_cocktails = self.rag_service.search_cocktails(
                        query=query, n_results=5, cocktail_list=search_codes
                    )

                    if relevant_cocktails:
                        context = f"\n[{feeling}에 어울리는 칵테일]\n"
                        for cocktail in relevant_cocktails[:3]:  # 상위 3개만
                            context += f"- {cocktail.get('english_name', '')}\n"
                            # 첫 번째 칵테일을 선택된 것으로 표시 (다음 검색에서 제외)
                            if cocktail.get('code'):
                                selected_cocktail_codes.add(str(cocktail.get('code')))
                                break  # 각 감정마다 1개만 선택
                        rag_contexts.append(context)

                # RAG 검색 결과를 프롬프트에 포함
                rag_context_text = "\n".join(rag_contexts)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [행복, 피곤, 화남] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    f"아래는 각 감정에 추천 가능한 칵테일 목록입니다:\n{rag_context_text}\n"
                    "추천은 반드시 위 목록에 있는 칵테일의 영어 이름만 사용하세요. 다른 칵테일을 추천하지 마세요.\n"
                    "중요 규칙:\n"
                    "1. \"name\" 필드에는 반드시 위 목록의 영어 칵테일 이름만 정확히 입력하세요.\n"
                    "2. 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요.\n"
                    "3. 첫 번째는 행복할 때, 두 번째는 피곤할 때, 세 번째는 화날 때 어울리는 칵테일을 각각 다르게 추천하세요."
                )
            else:
                # 기존 방식 (RAG 미사용)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [행복, 피곤, 화남] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다.\n"
                    "중요: 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요."
                )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": [{"text": system_prompt, "type": "text"}]},
                    {
                        "role": "user",
                        "content": [{"text": f"제공된 페르소나는 다음과 같습니다: {persona}", "type": "text"}],
                    },
                    {
                        "role": "user",
                        "content": [{"text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}", "type": "text"}],
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            response_content = response.choices[0].message.content
            matched_response = match_cocktail_in_json(cocktail_list, response_content)

            return json.dumps(matched_response, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"감정 기반 추천 생성 중 오류 발생: {e}")
            return json.dumps({"error": "추천 생성에 실패했습니다."}, ensure_ascii=False)

    def _parse_cocktail_codes(self, cocktail_list: str) -> List[str]:
        """칵테일 목록 문자열에서 code 리스트를 추출합니다.

        Args:
            cocktail_list: 칵테일 목록 문자열 (JSON 또는 텍스트)

        Returns:
            칵테일 code 리스트
        """
        from app.utils.data_loader import data_loader
        import re

        codes = []
        try:
            # JSON 형식으로 파싱 시도
            cocktails = json.loads(cocktail_list)
            if isinstance(cocktails, list):
                # 모든 레시피 로드 (이름으로 code 찾기 위해)
                all_recipes = data_loader.get_all_recipes()

                for item in cocktails:
                    if isinstance(item, dict):
                        # 딕셔너리 형태 (code 필드가 있는 경우)
                        if item.get("code"):
                            codes.append(str(item.get("code")))
                    elif isinstance(item, str):
                        # 문자열 형태 (칵테일 이름)
                        # 정규화: 공백 제거, 소문자 변환
                        item_normalized = re.sub(r'\s+', '', item.lower())

                        found = False
                        for recipe in all_recipes:
                            korean_name = re.sub(r'\s+', '', recipe.get("korean_name", "").lower())
                            english_name = re.sub(r'\s+', '', recipe.get("english_name", "").lower())

                            # 정확히 일치하거나 포함 관계 확인
                            if (korean_name == item_normalized or
                                english_name == item_normalized or
                                item_normalized in korean_name or
                                item_normalized in english_name):
                                codes.append(str(recipe.get("code")))
                                found = True
                                logger.info(f"'{item}' 매칭됨: {recipe.get('korean_name')} (code: {recipe.get('code')})")
                                break

                        if not found:
                            logger.warning(f"'{item}' 칵테일을 찾을 수 없습니다")
        except (json.JSONDecodeError, AttributeError) as e:
            # JSON이 아닌 경우 무시
            logger.error(f"cocktail_list 파싱 오류: {e}")
            pass

        logger.info(f"최종 파싱된 codes: {codes}")
        return codes
    
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

            # RAG를 사용하는 경우
            use_rag_for_request = self.use_rag and self.rag_service
            if use_rag_for_request:
                # cocktail_list를 파싱하여 code 리스트 추출
                cocktail_codes = self._parse_cocktail_codes(cocktail_list)

                # codes가 비어있으면 이 요청에서만 RAG 사용 안 함
                if not cocktail_codes:
                    logger.warning("cocktail codes가 비어있어 이 요청에서는 RAG를 사용하지 않습니다")
                    use_rag_for_request = False

            if use_rag_for_request:
                # 각 상황에 대해 RAG 검색 수행
                situations = ["바쁨", "한가", "여행"]
                rag_contexts = []
                selected_cocktail_codes = set()  # 이미 선택된 칵테일 추적

                for situation in situations:
                    query = f"{situation} 상황에 어울리는 칵테일"

                    # 이미 선택된 칵테일을 제외한 목록으로 검색
                    available_codes = [code for code in cocktail_codes if code not in selected_cocktail_codes]

                    # 사용 가능한 칵테일이 없으면 전체 목록 사용
                    search_codes = available_codes if available_codes else cocktail_codes

                    relevant_cocktails = self.rag_service.search_cocktails(
                        query=query, n_results=5, cocktail_list=search_codes
                    )

                    if relevant_cocktails:
                        context = f"\n[{situation} 상황에 어울리는 칵테일]\n"
                        for cocktail in relevant_cocktails[:3]:  # 상위 3개만
                            context += f"- {cocktail.get('english_name', '')}\n"
                            # 첫 번째 칵테일을 선택된 것으로 표시 (다음 검색에서 제외)
                            if cocktail.get('code'):
                                selected_cocktail_codes.add(str(cocktail.get('code')))
                                break  # 각 상황마다 1개만 선택
                        rag_contexts.append(context)

                # RAG 검색 결과를 프롬프트에 포함
                rag_context_text = "\n".join(rag_contexts)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [바쁨, 한가, 여행] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    f"아래는 각 상황에 추천 가능한 칵테일 목록입니다:\n{rag_context_text}\n"
                    "추천은 반드시 위 목록에 있는 칵테일의 영어 이름만 사용하세요. 다른 칵테일을 추천하지 마세요.\n"
                    "중요 규칙:\n"
                    "1. \"name\" 필드에는 반드시 위 목록의 영어 칵테일 이름만 정확히 입력하세요.\n"
                    "2. 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요.\n"
                    "3. 첫 번째는 바쁠 때, 두 번째는 한가할 때, 세 번째는 여행 중일 때 어울리는 칵테일을 각각 다르게 추천하세요."
                )

            else:
                # 기존 방식 (RAG 미사용)
                system_prompt = (
                    "당신은 전문 칵테일 소믈리에입니다. 사용자에게 가장 적합한 칵테일을 추천하기 위해 사용자의 페르소나 정보를 바탕으로 추천을 제공합니다.\n"
                    "당신은 20대 소믈리에이고 편안하고 부담없는 말투를 갖고 있습니다.\n"
                    "칵테일은 \"name\" 태그, 추천 요소는 \"tag\"태그, 추천 이유는 \"reason\" 태그에 담아 \"recommendation\" 태그에 담긴 json으로 제시합니다.\n"
                    "당신은 [바쁨, 한가, 여행] 상황에 대해 추천하는 칵테일 1종씩 총 3종을 반드시 순서대로 추천합니다.\n"
                    "당신은 갖고 있는 칵테일 중 3종을 추천하고 그 이유를 50자 내로 설명합니다.\n"
                    "추천은 항상 갖고 있는 칵테일에 포함된 칵테일만 작성합니다.\n"
                    "중요: 3개의 추천은 반드시 서로 다른 칵테일이어야 합니다. 같은 칵테일을 중복으로 추천하지 마세요."
                )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": [{"text": system_prompt, "type": "text"}]},
                    {
                        "role": "user",
                        "content": [{"text": f"제공된 페르소나는 다음과 같습니다: {persona}", "type": "text"}],
                    },
                    {
                        "role": "user",
                        "content": [{"text": f"당신이 갖고 있는 칵테일은 다음과 같습니다: {cocktail_list}", "type": "text"}],
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            response_content = response.choices[0].message.content
            
            matched_response = match_cocktail_in_json(cocktail_list, response_content)

            return json.dumps(matched_response, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"상황 기반 추천 생성 중 오류 발생: {e}")
            return json.dumps({"error": "추천 생성에 실패했습니다."}, ensure_ascii=False)
