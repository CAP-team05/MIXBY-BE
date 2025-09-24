"""
데이터 로더 테스트
"""
import pytest
from app.utils.data_loader import DataLoader


@pytest.fixture
def data_loader():
    """테스트용 데이터 로더 인스턴스를 생성합니다."""
    return DataLoader()


def test_get_all_drinks(data_loader):
    """모든 음료 데이터를 가져오는 기능을 테스트합니다."""
    drinks = data_loader.get_all_drinks()
    assert isinstance(drinks, list)
    assert len(drinks) > 0
    
    # 첫 번째 음료가 필요한 필드를 가지고 있는지 확인
    if drinks:
        first_drink = drinks[0]
        assert "code" in first_drink
        assert "name" in first_drink


def test_get_all_recipes(data_loader):
    """모든 레시피 데이터를 가져오는 기능을 테스트합니다."""
    recipes = data_loader.get_all_recipes()
    assert isinstance(recipes, list)
    assert len(recipes) > 0
    
    # 첫 번째 레시피가 필요한 필드를 가지고 있는지 확인
    if recipes:
        first_recipe = recipes[0]
        assert "code" in first_recipe
        assert "ingredients" in first_recipe


def test_get_all_ingredients(data_loader):
    """모든 재료 데이터를 가져오는 기능을 테스트합니다."""
    ingredients = data_loader.get_all_ingredients()
    assert isinstance(ingredients, list)
    assert len(ingredients) > 0


def test_get_all_challenges(data_loader):
    """모든 챌린지 데이터를 가져오는 기능을 테스트합니다."""
    challenges = data_loader.get_all_challenges()
    assert isinstance(challenges, list)
    assert len(challenges) > 0


def test_cache_functionality(data_loader):
    """캐시 기능을 테스트합니다."""
    # 첫 번째 로드
    drinks1 = data_loader.get_all_drinks()
    
    # 두 번째 로드 (캐시에서 가져와야 함)
    drinks2 = data_loader.get_all_drinks()
    
    # 같은 객체여야 함 (캐시에서 가져왔으므로)
    assert drinks1 is drinks2


def test_clear_cache(data_loader):
    """캐시 초기화 기능을 테스트합니다."""
    # 데이터 로드하여 캐시 생성
    data_loader.get_all_drinks()
    
    # 캐시 초기화
    data_loader.clear_cache()
    
    # 캐시가 비어있는지 확인
    assert len(data_loader._cache) == 0


def test_file_not_found_error(data_loader):
    """존재하지 않는 파일을 로드할 때 에러가 발생하는지 테스트합니다."""
    with pytest.raises(FileNotFoundError):
        data_loader.load_json("nonexistent_file.json")
