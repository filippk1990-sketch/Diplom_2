import allure


@allure.feature("Логин пользователя")
class TestLogin:
    @allure.title("Вход существующего пользователя")
    def test_login_existing_user(self, api, registered_user):
        response = api.login({
            "email": registered_user["email"],
            "password": registered_user["password"],
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == registered_user["email"]
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]

    @allure.title("Вход с неправильным email")
    def test_login_incorrect_email(self, api, registered_user):
        response = api.login({
            "email": "invalid@example.com",
            "password": registered_user["password"],
        })
        assert response.status_code == 401
        assert response.json() == {
            "success": False, "message": "email or password are incorrect",
        }

    @allure.title("Вход с неправильным паролем")
    def test_login_incorrect_password(self, api, registered_user):
        response = api.login({
            "email": registered_user["email"],
            "password": "wrong-password",
        })
        assert response.status_code == 401
        assert response.json() == {
            "success": False, "message": "email or password are incorrect",
        }

    @allure.title("Вход с неправильным email и паролем")
    def test_login_incorrect_email_and_password(self, api, registered_user):
        response = api.login({
            "email": "invalid@example.com",
            "password": "wrong-password",
        })
        assert response.status_code == 401
        assert response.json() == {
            "success": False, "message": "email or password are incorrect",
        }
