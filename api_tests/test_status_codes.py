import pytest
import requests

@pytest.mark.api
def test_homepage_status_code_200():
    r = requests.get("https://the-internet.herokuapp.com/")
    assert r.status_code == 200

@pytest.mark.api
def test_login_page_status_code_200():
    r = requests.get("https://the-internet.herokuapp.com/login")
    assert r.status_code == 200