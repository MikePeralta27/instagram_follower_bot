from selenium import webdriver
import time

from selenium.common import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

URL = "https://www.instagram.com/"
LOGIN_URL = "accounts/login/"
SIMILAR_ACCOUNT = "cristiano"
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options)

    def login(self):
        # go to sign in page
        self.driver.get(f"{URL}{LOGIN_URL}")

        # Log in
        time.sleep(5)
        username = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[1]/div/label/input')
        username.send_keys(USERNAME)
        time.sleep(2)
        password = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div/div[2]/div/label/input')
        password.send_keys(PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)

        time.sleep(10)
        # Handling pops
        time.sleep(3)
        pass_save_not_now_button = self.driver.find_element(by=By.XPATH, value="//div[contains(text(), 'Not now')]")
        if pass_save_not_now_button:
            pass_save_not_now_button.click()

        time.sleep(4)
        not_now_notification_button = self.driver.find_element(by=By.XPATH,
                                                               value="//button[contains(text(), 'Not Now')]")
        if not_now_notification_button:
            not_now_notification_button.click()
        time.sleep(2)

    def find_followers(self):
        self.driver.get(f"{URL}{SIMILAR_ACCOUNT}/")
        time.sleep(10)
        followers_button = self.driver.find_element(by=By.XPATH, value="//a[contains(text(), 'followers')]")
        followers_button.click()
        time.sleep(6)
        # The xpath of the modal that shows the followers will change over time. Update yours accordingly.
        modal_xpath = "/html/body/div[6]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)
        for i in range(10):
            # In this case we're executing some Javascript, that's what the execute_script() method does. The method
            # can accept the script as well as an HTML element. The modal in this case, becomes the arguments[0] in
            # the script. Then we're using Javascript to say: "scroll the top of the modal (popup) element by the
            # height of the modal (popup)"
            time.sleep(4)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        follow_buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value='[class=" _acan _acap _acas _aj1- _ap30"]')

        for follow in follow_buttons:
            try:
                follow.click()
                time.sleep(2)

            except ElementClickInterceptedException:
                time.sleep(3)
                try:
                    ok_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'OK')]")
                    if ok_button:
                        time.sleep(2)
                        ok_button.click()

                    time.sleep(5)
                    cancel2_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                    if cancel2_button:
                        time.sleep(2)
                        cancel2_button.click()

                except NoSuchElementException:
                    print("No such element")
