import pytest
from ui.flows.auth_flow import AuthFlow

@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(page):
    login = AuthFlow(page).login_default_user()
    assert "You logged into a secure area!" in login.get_flash_text()