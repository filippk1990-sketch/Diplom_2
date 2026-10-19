import allure
import pytest
from config import BASE_URL, REQUEST_TIMEOUT


@allure.feature("Создание заказа")
class TestOrders:
    @pytest.mark.parametrize("authorized", [True, False], ids=["auth", "guest"])
    @allure.title("Создание заказа с ингредиентами, авторизация={authorized}")
    def test_create_order_with_ingredients(self, api, registered_user, ingredients, authorized):
        headers = {"Authorization": registered_user["accessToken"]} if authorized else {}
        response = api.post(f"{BASE_URL}/api/orders", json={"ingredients": ingredients},
                            headers=headers, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["order"]["number"], int)
        assert data["order"]["number"] > 0
        assert data["name"]

    @pytest.mark.parametrize("authorized", [True, False], ids=["auth", "guest"])
    @allure.title("Нельзя создать заказ без ингредиентов, авторизация={authorized}")
    def test_create_order_without_ingredients(self, api, registered_user, authorized):
        headers = {"Authorization": registered_user["accessToken"]} if authorized else {}
        response = api.post(f"{BASE_URL}/api/orders", json={"ingredients": []},
                            headers=headers, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 400
        assert response.json() == {
            "success": False, "message": "Ingredient ids must be provided"
        }

    @allure.title("Неверный хеш ингредиента возвращает ошибку сервера")
    def test_create_order_with_invalid_ingredient_hash(self, api, registered_user):
        response = api.post(f"{BASE_URL}/api/orders", json={"ingredients": ["not-a-valid-id"]},
                            headers={"Authorization": registered_user["accessToken"]},
                            timeout=REQUEST_TIMEOUT)
        assert response.status_code == 500
        assert "success\":true" not in response.text.replace(" ", "").lower()
