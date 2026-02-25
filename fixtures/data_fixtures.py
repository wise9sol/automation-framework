import pytest
from utils.data_loader import load_json

@pytest.fixture(scope="session")
def users():
    return load_json("data/users.json")

@pytest.fixture(scope="session")
def default_user(users):
    return users["default_user"]

@pytest.fixture(scope="session")
def bad_user(users):
    return users["bad_user"]