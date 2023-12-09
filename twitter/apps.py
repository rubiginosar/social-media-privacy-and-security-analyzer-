import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

# navigate to twitter's login page
driver = webdriver.Chrome()
driver.get("https://twitter.com/i/flow/login")

time.sleep(2)

# enter username
username = driver.find_element(By.TAG_NAME, "input")
username.send_keys("saadprojet")

# press on the "next" button
all_buttons = driver.find_elements(
    By.XPATH, "//div[@role='button']"
)
all_buttons[-2].click()

time.sleep(2)

# enter password
password = driver.find_element(
    By.XPATH, "//input[@type='password']"
)
password.send_keys("saadprojet123")

time.sleep(2)

# press on the login button
all_buttons = driver.find_elements(
    By.XPATH, "//div[@role='button']"
)
all_buttons[-1].click()

time.sleep(2)

# search a keyword
driver.get("https://twitter.com/settings/account")
time.sleep(2)
all_buttons = driver.find_element(
    By.XPATH, "//div[contains(text(), 'Account information')]"
)
all_buttons.click()
time.sleep(2)