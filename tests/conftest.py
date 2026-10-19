import pytest
import requests

from config import BASE_URL, REQUEST_TIMEOUT
from helpers import unique_user


@pytest.fixture
def api():
    with requests.Session() as session:
        session.headers.update({"Content-Type": "application/json"})
        yield session


@pytest.fixture
def registered_user(api):
    user = unique_user()
    response = api.post(f"{BASE_URL}/api/auth/register", json=user,
                        timeout=REQUEST_TIMEOUT)
    token = None
    try:
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["success"] is True
        token = payload["accessToken"]
        assert token.startswith("Bearer ")
        yield {**user, "accessToken": token}
    finally:
        if token is not None:
            cleanup = api.delete(f"{BASE_URL}/api/auth/user",
                                 headers={"Authorization": token},
                                 timeout=REQUEST_TIMEOUT)
            assert cleanup.status_code == 202, (
                f"User cleanup failed: {cleanup.status_code} {cleanup.text}"
            )


@pytest.fixture
def auth_headers(request):
    # Guest order tests must not create a registered user as a side effect.
    if request.param is False:
        return {}
    registered = request.getfixturevalue("registered_user")
    return {"Authorization": registered["accessToken"]}


@pytest.fixture
def ingredients(api):
    response = api.get(f"{BASE_URL}/api/ingredients", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["success"] is True and payload["data"]
    buns = [x["_id"] for x in payload["data"] if x["type"] == "bun"]
    toppings = [x["_id"] for x in payload["data"] if x["type"] != "bun"]
    assert buns and toppings
    return [buns[0], toppings[0], buns[0]]
