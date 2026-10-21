import allure
import pytest

from helpers import unique_user


@allure.feature("Создание пользователя")
class TestRegistration:
    @allure.title("Регистрация уникального пользователя")
    def test_register_unique_user(self, api, created_users):
        user = unique_user()
        response = api.register(user)
        data = response.json()
        created_users.append(data["accessToken"])

        assert response.status_code == 200, response.text
        assert data["success"] is True
        assert data["user"] == {"email": user["email"], "name": user["name"]}
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]

    @allure.title("Повторная регистрация пользователя")
    def test_register_duplicate_user(self, api, registered_user):
        user = {key: registered_user[key] for key in ("email", "password", "name")}
        response = api.register(user)
        assert response.status_code == 403
        assert response.json() == {
            "success": False, "message": "User already exists",
        }

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Отсутствует обязательное поле: {missing_field}")
    def test_register_without_required_field(self, api, missing_field):
        user = unique_user()
        user.pop(missing_field)
        response = api.register(user)
        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields",
        }
