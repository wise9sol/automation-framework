import pytest
from utils.config import BASE_URL
from ui.pages.login_page import LoginPage

@pytest.mark.ui
def test_logout_after_login(auth_page):
    # go to a page that requires auth
    auth_page.goto(f"{BASE_URL}/secure", wait_until="domcontentloaded")

    login = LoginPage(auth_page)
    assert login.is_logout_visible()

    login.logout()
    assert "You logged out of the secure area!" in login.get_flash_text()