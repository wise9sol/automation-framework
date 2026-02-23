# pages/login_page.py

from utils.config import BASE_URL, LOGIN_PATH

class LoginPage:
    def __init__(self, page):
        self.page = page

        # selectors
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = 'button[type="submit"]'
        self.flash_message = "#flash"
        self.logout_button = 'a[href="/logout"]'

    def goto(self):
        url = f"{BASE_URL}{LOGIN_PATH}"

        # Navigate and capture response (helps detect 5xx/odd loads)
        response = self.page.goto(url, wait_until="domcontentloaded")

        # If response exists and looks bad, retry once
        if response and not response.ok:
            self.page.reload(wait_until="domcontentloaded")

        # Ensure the login form is actually present (retry once if needed)
        try:
            self.page.wait_for_selector(self.username_input, state="visible", timeout=10_000)
        except Exception:
            # Sometimes the site serves a transient error page; reload fixes it
            self.page.reload(wait_until="domcontentloaded")
            self.page.wait_for_selector(self.username_input, state="visible", timeout=10_000)

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def logout(self):
        self.page.click(self.logout_button)

    def is_logout_visible(self) -> bool:
        return self.page.is_visible(self.logout_button)

    def get_flash_text(self) -> str:
        return self.page.inner_text(self.flash_message)