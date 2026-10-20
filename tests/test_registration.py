import allure
import pytest

from config import BASE_URL, REQUEST_TIMEOUT
from helpers import unique_user


@allure.feature("Создание пользователя")
class TestRegistration:
    @allure.title("Регистрация уникального пользователя")
    def test_register_unique_user(self, api):
        user = unique_user()
        response = api.post(f"{BASE_URL}/api/auth/register", json=user, timeout=REQUEST_TIMEOUT)
        try:
            assert response.status_code == 200, response.text
            data = response.json()
            assert data["success"] is True
            assert data["user"] == {"email": user["email"], "name": user["name"]}
            assert data["accessToken"].startswith("Bearer ")
            assert data["refreshToken"]
        finally:
            if response.status_code == 200 and response.json().get("accessToken"):
                cleanup = api.delete(f"{BASE_URL}/api/auth/user",
                                     headers={"Authorization": response.json()["accessToken"]},
                                     timeout=REQUEST_TIMEOUT)
                assert cleanup.status_code == 202, (
                    f"Could not clean up registered user: {cleanup.status_code} {cleanup.text}"
                )

    @allure.title("Нельзя повторно зарегистрировать того же пользователя")
    def test_register_duplicate_user(self, api, registered_user):
        payload = {key: registered_user[key] for key in ("email", "password", "name")}
        response = api.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 403
        assert response.json() == {"success": False, "message": "User already exists"}

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Отсутствует обязательное поле: {missing_field}")
    def test_register_without_required_field(self, api, missing_field):
        payload = unique_user()
        payload.pop(missing_field)
        response = api.post(f"{BASE_URL}/api/auth/register", json=payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }
