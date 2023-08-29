import json
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from lib.helper import wait_exists

URL = "http://healthmate.withings.com/"
CHROME_EXEC = '/Users/amasson/Downloads/chromedriver-mac-arm64/chromedriver'  # replace with the path to your chromedriver
COOKIE_FILE = 'cookies.json'


def add_cookies(driver):
    with open(COOKIE_FILE, 'r') as openfile:
        # Reading from json file
        cookies = json.load(openfile)

    for cookie in cookies:
        driver.add_cookie(cookie)


# Setup function to initialize webdriver
@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(executable_path=CHROME_EXEC)
    request.cls.driver = driver

    # Open the page to get to the correct domain before loading cookies
    driver.get(URL)
    try:
        add_cookies(driver)
    except Exception as e:
        print(f"Seems like there are no cookies to add: {e}")
        driver.has_cookies = False
    else:
        driver.has_cookies = True
        # Reload the page with cookies
        driver.get(URL)

    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestWithings:
    login = "testa+base@withings.com"
    passwd = "@Coucou!12345"

    def accept_cookies(self):
        """
        Accept cookies
        """
        wait_exists(self.get_cookies_button)
        self.get_cookies_button().click()

    def get_cookies_button(self):
        return self.driver.find_element(By.CLASS_NAME, "accept-all")

    def enter_email(self):
        self.driver.find_element(By.CLASS_NAME, "email").send_keys(self.login)

    def click_next(self):
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def get_login_with_password(self):
        return self.driver.find_element(By.LINK_TEXT, 'Login with password instead')

    def wait_for_login_with_password(self):
        wait_exists(self.get_login_with_password)

    def click_login_with_password(self):
        self.get_login_with_password().click()

    def get_password_field(self):
        return self.driver.find_element(By.ID, 'password')

    def wait_for_login_with_password_page(self):
        wait_exists(self.get_password_field)

    def write_password(self):
        self.get_password_field().send_keys(self.passwd)

    def wait_home_page(self):
        wait_exists(self.get_plus_button)

    def get_plus_button(self):
        return self.driver.find_element(By.CLASS_NAME, "addbutton")

    def click_plus_button(self):
        self.get_plus_button().click()

    @staticmethod
    def wait_plus_menu():
        time.sleep(1)

    def click_plus_menu_weight(self):
        self.driver.find_element(By.XPATH, "//li[@data-trigger='app:weight:graph:add']").click()

    def setup_method(self):
        if not self.driver.has_cookies:
            self.accept_cookies()
            self.enter_email()
            self.click_next()
            self.wait_for_login_with_password()
            self.click_login_with_password()
            self.wait_for_login_with_password_page()
            self.write_password()
            self.click_next()
        self.wait_home_page()

        # Save cookies
        with open(COOKIE_FILE, "w") as outfile:
            json.dump(self.driver.get_cookies(), outfile)

        self.click_plus_button()
        self.wait_plus_menu()
        self.click_plus_menu_weight()

    def test_blank(self):
        import ipdb;ipdb.set_trace()  # FIXME REMOVE ME
        pass
