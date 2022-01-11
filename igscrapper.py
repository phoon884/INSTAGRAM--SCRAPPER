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
SHORT_WAIT = 2
MID_WAIT = 5
LONG_WAIT =  10

class IGScrapper:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.driver = self.__initilize_driver()
        self.profile_name = self.__login()

    def __initilize_driver(self):
        return webdriver.Chrome(PATH)

    def __login(self):
        self.driver.get(WEBSITE)
        WebDriverWait(self.driver, MID_WAIT).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@aria-label="Phone number, username, or email"]'))).send_keys(self.__username)
        self.driver.find_element_by_xpath(
            '//input[@aria-label="Password"]').send_keys(self.__password)
        time.sleep(SHORT_WAIT)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(SHORT_WAIT)
        try:
            WebDriverWait(self.driver, LONG_WAIT).until(EC.presence_of_element_located(
                (By.XPATH, '//img[@alt="Instagram"]'))).click()
            WebDriverWait(self.driver, MID_WAIT).until(EC.presence_of_element_located(
                (By.XPATH, '//button[contains(text(),"Not Now")]'))).click()
        except Exception as e:
            print(e)
            return None
        return self.driver.find_element_by_xpath('//a[@class="gmFkV"]').text

    def __scroll(self, element):
        for x in range(20):
            last_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", element)
            time.sleep(SHORT_WAIT)
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', element)
            current_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", element)
            if current_height == last_height:
                break

    def go_to_profile(self, profile_name):
        profile_url = WEBSITE + profile_name
        self.driver.get(profile_url)

    def go_to_home(self):
        self.driver.get(WEBSITE)

    def get_followers(self, profile_name):
        try:
            self.go_to_profile(profile_name)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//a[@href="/{}/followers/"]'.format(self.profile_name)))).click()
            scrollable_div = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="isgrP"]')))
            self.__scroll(scrollable_div)
            arr = self.driver.find_elements_by_xpath(
                '//img[@data-testid="user-avatar"]')
            array = []
            for img in arr:
                text = img.get_attribute('alt')
                text = text.replace("'s profile picture", '')
                if text == self.profile_name:
                    continue
                array.append(text)
            return array
        except Exception as e:
            print(e)
            return []
    def quit(self):
        if (self.driver != None):
            self.driver.quit();


if __name__ == "__main__":
    load_dotenv()
    scraper = IGScrapper(os.environ['USER'], os.environ['PASSWORD'])
    print(scraper.get_followers(scraper.profile_name))
    scraper.quit()
