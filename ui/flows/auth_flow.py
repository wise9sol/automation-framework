from ui.pages.login_page import LoginPage

class AuthFlow:
    def __init__(self, page):
        self.page = page

    def login(self, username: str, password: str) -> LoginPage:
        login = LoginPage(self.page)
        login.goto()
        login.login(username, password)
        return login

    def login_default_user(self, user: dict) -> LoginPage:
        return self.login(user["username"], user["password"])