from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
import time

WEBSITE = "https://www.instagram.com/"
PATH = "chromedriver.exe"

class IGScrapper:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.driver = self.__initilize_driver()

    def __initilize_driver(self):
        return webdriver.Chrome(PATH)

    def login(self):
        self.driver.get(WEBSITE)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@aria-label="Phone number, username, or email"]'))).send_keys(self.__username)
        self.driver.find_element_by_xpath('//input[@aria-label="Password"]').send_keys(self.__password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//img[@alt="Instagram"]'))).click()
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(),"Not Now")]'))).click()
        except Exception as e:
            print(e)
            return False
        return True

if __name__ == "__main__":
    load_dotenv()
    scraper = IGScrapper(os.environ['USER'], os.environ['PASSWORD'])
    scraper.login()