"""All HTTP operations and Allure steps for Stellar Burgers API tests."""

import allure

from config import BASE_URL, REQUEST_TIMEOUT


class APIClient:
    def __init__(self, session):
        self.session = session

    @allure.step("POST /api/auth/register — регистрация пользователя")
    def register(self, payload):
        return self.session.post(
            f"{BASE_URL}/api/auth/register",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    @allure.step("POST /api/auth/login — вход пользователя")
    def login(self, payload):
        return self.session.post(
            f"{BASE_URL}/api/auth/login",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    @allure.step("GET /api/ingredients — список ингредиентов")
    def get_ingredients(self):
        return self.session.get(
            f"{BASE_URL}/api/ingredients",
            timeout=REQUEST_TIMEOUT,
        )

    @allure.step("POST /api/orders — создание заказа")
    def create_order(self, ingredients, headers=None):
        return self.session.post(
            f"{BASE_URL}/api/orders",
            json={"ingredients": ingredients},
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    @allure.step("DELETE /api/auth/user — удаление тестового пользователя")
    def delete_user(self, token):
        return self.session.delete(
            f"{BASE_URL}/api/auth/user",
            headers={"Authorization": token},
            timeout=REQUEST_TIMEOUT,
        )
