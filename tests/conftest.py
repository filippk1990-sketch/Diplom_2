import pytest
import requests

from api_client import APIClient
from helpers import unique_user


@pytest.fixture
def api():
    with requests.Session() as session:
        session.headers.update({"Content-Type": "application/json"})
        yield APIClient(session)


@pytest.fixture
def created_users(api):
    """Collect access tokens and remove created users even when a test fails."""
    tokens = []
    yield tokens
    for token in tokens:
        api.delete_user(token)


@pytest.fixture
def registered_user(api, created_users):
    user = unique_user()
    payload = api.register(user).json()
    token = payload["accessToken"]
    created_users.append(token)
    return {**user, "accessToken": token}


@pytest.fixture
def auth_headers(request):
    """Guests must not create a registered user just for an order test."""
    if request.param is False:
        return {}
    user = request.getfixturevalue("registered_user")
    return {"Authorization": user["accessToken"]}


@pytest.fixture
def ingredients(api):
    items = api.get_ingredients().json()["data"]
    bun_id = next(item["_id"] for item in items if item["type"] == "bun")
    filling_id = next(item["_id"] for item in items if item["type"] != "bun")
    return [bun_id, filling_id, bun_id]
