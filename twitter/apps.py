import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# navigate to twitter's login page
driver = webdriver.Chrome()
driver.get("https://twitter.com/i/flow/login")

time.sleep(2)

# enter username
username = driver.find_element(By.TAG_NAME, "input")
username.send_keys("NesrineTbg")

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
password.send_keys("13022017")

time.sleep(2)

# press on the login button
all_buttons = driver.find_elements(
    By.XPATH, "//div[@role='button']"
)
all_buttons[-1].click()

time.sleep(2)
