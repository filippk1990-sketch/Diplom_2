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
    response = api.post(f"{BASE_URL}/api/auth/register", json=user, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["success"] is True, data
    token = data["accessToken"]
    yield {**user, "accessToken": token}
    cleanup = api.delete(f"{BASE_URL}/api/auth/user",
                         headers={"Authorization": token}, timeout=REQUEST_TIMEOUT)
    assert cleanup.status_code == 202, f"User cleanup failed: {cleanup.status_code} {cleanup.text}"


@pytest.fixture
def ingredients(api):
    response = api.get(f"{BASE_URL}/api/ingredients", timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["success"] is True and data["data"]
    buns = [item["_id"] for item in data["data"] if item["type"] == "bun"]
    fillings = [item["_id"] for item in data["data"] if item["type"] != "bun"]
    assert buns and fillings
    return [buns[0], fillings[0], buns[0]]
