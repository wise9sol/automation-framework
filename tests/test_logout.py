import pytest
from pages.login_page import LoginPage

@pytest.mark.ui
def test_logout_after_login(page):
    login = LoginPage(page)

    login.goto()
    login.login("tomsmith", "SuperSecretPassword!")

    # confirm we're in the secure area by checking logout link exists
    assert login.is_logout_visible()

    login.logout()
    message = login.get_flash_text()

    assert "You logged out of the secure area!" in message