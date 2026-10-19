import allure
import pytest
from config import BASE_URL, REQUEST_TIMEOUT


@allure.feature("Создание заказа")
class TestOrders:
    @pytest.mark.parametrize("auth_headers", [True, False], indirect=True,
                             ids=["authorized", "guest"])
    @allure.title("Заказ с ингредиентами; авторизация={auth_headers}")
    def test_create_order_with_ingredients(self, api, ingredients, auth_headers):
        response = api.post(f"{BASE_URL}/api/orders",
                            json={"ingredients": ingredients},
                            headers=auth_headers, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["order"]["number"], int)
        assert data["order"]["number"] > 0
        assert isinstance(data["name"], str) and data["name"].strip()

    @pytest.mark.parametrize("auth_headers", [True, False], indirect=True,
                             ids=["authorized", "guest"])
    @allure.title("Заказ без ингредиентов; авторизация={auth_headers}")
    def test_create_order_without_ingredients(self, api, auth_headers):
        response = api.post(f"{BASE_URL}/api/orders", json={"ingredients": []},
                            headers=auth_headers, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 400, response.text
        assert response.json() == {
            "success": False, "message": "Ingredient ids must be provided"
        }

    @allure.title("Некорректный идентификатор ингредиента возвращает HTTP 500")
    def test_create_order_with_invalid_ingredient_hash(self, api, registered_user):
        response = api.post(
            f"{BASE_URL}/api/orders", json={"ingredients": ["not-a-valid-id"]},
            headers={"Authorization": registered_user["accessToken"]},
            timeout=REQUEST_TIMEOUT,
        )
        assert response.status_code == 500, response.text
        # API documentation specifies HTTP 500, not a stable JSON error schema.
        # The body must contain an error, rather than a success response.
        assert response.text.strip(), "Server returned empty error body"
        if "application/json" in response.headers.get("Content-Type", ""):
            assert response.json().get("success") is not True
