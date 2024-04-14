#!/usr/bin/env python3
"""Auto retrieve API Keys from forty-two account

This class use headless browser to log into your intranet
account and retrieve Client UID and Secret.
This class can also handle auto-regenerate and auto-replace your
current secret
"""

import logging
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime
import pyotp

__author__ = "Joonhyeok Han"
__credits__ = ["Joonhyeok Han"]
__license__ = "The Unlicense"
__version__ = "1.0.0"
__maintainer__ = "Joonhyeok Han"
__email__ = "joonhan@student.42.kr"
__status__ = "Production"

class fortytwo_auto_keys:
    def __init__(
            self,
            login: str,
            password: str,
            app_url: str,
            otp_secret: str = None,
            force_renew: bool = False,
            day_before_renew: int = 3,
            use_chrome: bool = True,
    ):
        """Initialize a browser and set parameters for current sessions

        Args:
                login (str): login of your 42 account
                password (str): password of you 42 account
                app_url (str): Intra url of the application. Format like https://profile.intra.42.fr/oauth/applications/[app_id]
                otp_secret (str, optional): OTP secret, use for generate TOTP. Defaults to None.
                force_renew (bool, optional): Force renew of secret. Defaults to False.
                day_before_renew (int, optional): Renew n days before end of validation.
                        Ignored if [force_renew == True]. Defaults to 3.
                use_chrome (bool, optional): If true will use chrome driver, otherwise Firefox. Defaults to True.
        """
        self.login = login
        self.password = password
        self.app_url = app_url
        self.otp_secret = otp_secret
        self.force_renew = force_renew
        self.day_before_renew = day_before_renew
        self.__keys = dict()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        if use_chrome:
            self.browser = webdriver.Chrome(options=options)
            # self.browser = webdriver.Chrome(ChromeDriverManager().install())
        else:
            self.browser = webdriver.Firefox(options=options)

        stealth(self.browser,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )
        self.browser.get(self.app_url)

    def __del__(self):
        """Destructor
        Close browser
        """
        self.browser.close()

    @property
    def keys(self):
        self.__parse_keys()
        return self.__keys

    def handle_login(self) -> None:
        """Handle fortytwo intra login
        Fill field login/password and click on login button
        """
        """Removed because of new login page
        sign_in_button = self.browser.find_element(By.XPATH, "//a[@class='btn btn-login-student']")
        sign_in_button.click()
        """
        login_field = self.browser.find_element(By.NAME, "username")
        password_field = self.browser.find_element(By.NAME, "password")
        login_field.clear()
        password_field.clear()
        login_field.send_keys(self.login)
        password_field.send_keys(self.password)
        self.browser.find_element(By.NAME, "login").click()
        logging.info("Login successful")

    def handle_totp(self) -> None:
        """Handle TOTP login
        Fill totp field and click on login button
        """
        code_generator = pyotp.TOTP(self.otp_secret)
        totp_field = self.browser.find_element(By.NAME, "users[code]")
        totp_field.clear()
        totp_field.send_keys(code_generator.now())
        self.browser.find_element(By.NAME, "commit").click()

    def get_validity_date(self) -> datetime:
        """Get date validity of the api secret

        Returns:
                datetime: Date time of end of validity
        """
        fields = self.browser.find_elements(By.CLASS_NAME, "rotation-actions")
        for field in fields:
            if "Valid until" in field.text:
                day, month, year = map(
                    int, field.text.split(' ')[2].split('/'))
                hour, minute = 10, 0
                iso_time = datetime(year, month, day, hour, minute)
                return iso_time

    def __can_replace(self) -> bool:
        """Test if "Replace now" button is present

        Returns:
            bool: True if button is present, false otherwise
        """
        try:
            self.replace_button = self.browser.find_element(
                By.LINK_TEXT, "Replace now")
        except NoSuchElementException:
            self.replace_button = None
            return False
        return True

    def __can_generate(self) -> bool:
        """Test if "Generate now" button is present

        Returns:
            bool: True is button is present
        """
        try:
            self.generate_button = self.browser.find_element(
                By.LINK_TEXT, "Generate now")
        except NoSuchElementException:
            self.generate_button = None
            return False
        return True

    def __time_to_renew(self) -> bool:
        """Test if it's time to renew the secret
        Use the parameter of the constructor. By default 5

        Returns:
            bool: True if it's time to generate new secret
        """
        validity = self.get_validity_date()
        delta = validity - datetime.now()
        if delta.days > self.day_before_renew:
            return False
        return True

    def __parse_keys(self) -> None:
        """Parse page to obtain API keys
        Use value in `data-copy`, can be (atm):
            - [data-app-uid-<appid>]
            - [data-app-secret-<appid>]
            - [data-app-next-secret-<appid>]
        Construct a dict with :
        {
            "uid": "<app-uid>",
            "secret": "<app-secret>",
            "next": "<app-next-secret>" (may not be present)
        }
        """
        keys = self.browser.find_elements(By.CLASS_NAME, 'copy')
        for key in keys:
            type = key.get_attribute("data-copy").split('-')[2]
            self.__keys[type] = key.get_attribute("data-clipboard-text")
        logging.info("Successfully API Keys parsed")

    def generate_new_secret(self) -> None:
        """Generate new secret.
        Emulate click on "Generate now" and "Replace now"
        """
        self.__can_generate()
        if self.generate_button:
            self.generate_button.click()
        sleep(2)
        self.__can_replace()
        if self.replace_button:
            self.replace_button.click()
        sleep(2)
        logging.info("New secret generated")

    def remove_modal(self):
        count = 0
        try:
            modal_close_button = self.browser.find_element(By.CSS_SELECTOR, "#flashModal .modal-header .close")
            while modal_close_button.is_displayed():
                logging.info("find modal(count: {})".format(count))
                modal_close_button.click()
                sleep(2)
                modal_close_button = self.browser.find_element(By.CSS_SELECTOR, "#flashModal .modal-header .close")
                count += 1
        except NoSuchElementException:
            logging.info("modal is all removed(total count: {})".format(count))

    def auto(self) -> None:
        """Automatic operations for defaults operation.
        Will do:
        1/ Handle login
            a/ If TOTP, handle totp
        2/ Cehck if a renew is needed
            a/ Generate if needed
        3/ Parse keys, will be accessible with keys propreties
        """
        self.handle_login()
        while "Otp" in self.browser.title:
            self.handle_totp()
        self.remove_modal()
        if self.force_renew or self.__time_to_renew():
            self.generate_new_secret()
        self.__parse_keys()
