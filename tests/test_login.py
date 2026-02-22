import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
def test_login_success(page):
    login = LoginPage(page)

    login.goto()
    login.login("tomsmith", "SuperSecretPassword!")

    message = login.get_flash_text()
    assert "You logged into a secure area!" in message