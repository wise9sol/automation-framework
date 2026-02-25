import pytest
from ui.flows.auth_flow import AuthFlow

@pytest.mark.ui
def test_logout_after_login(page, default_user):
    login = AuthFlow(page).login_default_user(default_user)
    assert login.is_logout_visible()

    login.logout()
    assert "You logged out of the secure area!" in login.get_flash_text()