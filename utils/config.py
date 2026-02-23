import os

BASE_URL = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/login")

HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
SLOW_MO = int(os.getenv("SLOW_MO", "0"))