import allure
import pytest
from config import BASE_URL, REQUEST_TIMEOUT


@allure.feature("Логин пользователя")
class TestLogin:
    @allure.title("Вход существующего пользователя")
    def test_login_existing_user(self, api, registered_user):
        response = api.post(f"{BASE_URL}/api/auth/login", json={
            "email": registered_user["email"], "password": registered_user["password"]
        }, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == registered_user["email"]
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]

    @pytest.mark.parametrize("wrong_field", ["email", "password", "both"])
    @allure.title("Вход с неверными учётными данными: {wrong_field}")
    def test_login_wrong_credentials(self, api, registered_user, wrong_field):
        payload = {"email": registered_user["email"],
                   "password": registered_user["password"]}
        if wrong_field in ("email", "both"):
            payload["email"] = "invalid@example.com"
        if wrong_field in ("password", "both"):
            payload["password"] = "wrong-password"
        response = api.post(f"{BASE_URL}/api/auth/login", json=payload, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "email or password are incorrect"}
