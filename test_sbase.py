from seleniumbase import BaseCase
import time
class TestOpenGoogle(BaseCase):
    def test_google(self):
        self.open("https://www.google.com")
        time.sleep(10)
