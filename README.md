# Diplom_2 — Stellar Burgers / API

Все сценарии регистрации, входа и создания заказов; `pytest`, `requests`, `allure-pytest`.

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest --alluredir=allure-results
allure serve allure-results
```

Тестовые учётные записи создаются в фикстурах и удаляются через `DELETE /api/auth/user` (при нормальном завершении теста). Параметризация покрывает все три отсутствующих поля. Для ответа 500 на неправильный идентификатор проверяется код и отсутствие успешного результата; сервер может возвращать HTML.

Переменные: `STELLAR_URL` (базовый адрес), `REQUEST_TIMEOUT` (секунды). Ветка: `develop2`.

Внимание: документация PDF допускает создание заказа без авторизации (HTTP 200 с ингредиентами), хотя описание UI говорит об обязательной авторизации для кнопки оформления. API-тест следует поведению эндпоинта и проверяет гостевой заказ.
