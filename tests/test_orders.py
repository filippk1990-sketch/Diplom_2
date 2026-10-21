import allure
import pytest


@allure.feature("Создание заказа")
class TestOrders:
    @pytest.mark.parametrize("auth_headers", [True, False], indirect=True,
                             ids=["authorized", "guest"])
    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, api, ingredients, auth_headers):
        response = api.create_order(ingredients, auth_headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["order"]["number"], int)
        assert data["order"]["number"] > 0
        assert isinstance(data["name"], str) and data["name"].strip()

    @pytest.mark.parametrize("auth_headers", [True, False], indirect=True,
                             ids=["authorized", "guest"])
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api, auth_headers):
        response = api.create_order([], auth_headers)
        assert response.status_code == 400, response.text
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided",
        }

    @allure.title("Создание заказа с неверным идентификатором ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, api, registered_user):
        response = api.create_order(
            ["not-a-valid-id"],
            {"Authorization": registered_user["accessToken"]},
        )
        assert response.status_code == 500, response.text
