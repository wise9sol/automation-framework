from pathlib import Path
import pytest

from filelock import FileLock

from ui.pages.login_page import LoginPage
from utils.config import BASE_URL
from utils.env import ENV

AUTH_DIR = Path(".auth")
STATE_PATH = AUTH_DIR / f"storage_state_{ENV}.json"

@pytest.fixture(scope="session")
def storage_state(browser, default_user):
    """
    Create storage state once per test session per ENV.
    Safe for parallel runs using a file lock.
    """
    AUTH_DIR.mkdir(exist_ok=True)

    lock = FileLock(str(STATE_PATH) + ".lock", timeout=60)

    with lock:
        if STATE_PATH.exists() and STATE_PATH.stat().st_size > 0:
            return str(STATE_PATH)

        context = browser.new_context()
        page = context.new_page()

        login = LoginPage(page)
        login.goto()
        login.login(default_user["username"], default_user["password"])

        page.goto(f"{BASE_URL}/secure", wait_until="domcontentloaded")
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