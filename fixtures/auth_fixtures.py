from pathlib import Path
import pytest

from ui.pages.login_page import LoginPage

AUTH_DIR = Path(".auth")
STATE_PATH = AUTH_DIR / "storage_state.json"


@pytest.fixture(scope="session")
def storage_state(browser, default_user):
    """
    Create storage state once per test session.
    If it already exists, reuse it.
    """
    AUTH_DIR.mkdir(exist_ok=True)

    if STATE_PATH.exists() and STATE_PATH.stat().st_size > 0:
        return str(STATE_PATH)

    # Create a fresh context, login once, then save state
    context = browser.new_context()
    page = context.new_page()

    login = LoginPage(page)
    login.goto()
    login.login(default_user["username"], default_user["password"])

    # Quick sanity: logout link should exist after login
    page.wait_for_selector('a[href="/logout"]', timeout=10_000)

    context.storage_state(path=str(STATE_PATH))
    context.close()
    return str(STATE_PATH)


@pytest.fixture
def auth_context(browser, storage_state):
    """
    New context per test, but already authenticated.
    """
    context = browser.new_context(storage_state=storage_state)
    yield context
    context.close()


@pytest.fixture
def auth_page(auth_context):
    page = auth_context.new_page()
    yield page