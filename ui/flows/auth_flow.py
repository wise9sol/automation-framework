from ui.pages.login_page import LoginPage

class AuthFlow:
    def __init__(self, page):
        self.page = page

    def login_default_user(self) -> LoginPage:
        login = LoginPage(self.page)
        login.goto()
        login.login("tomsmith", "SuperSecretPassword!")
        return login