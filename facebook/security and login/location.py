from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

usr = "saadprojet@gmail.com"
pwd = "saadprojet123"

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://www.facebook.com/')
print("Opened Facebook")

wait = WebDriverWait(driver, 10)

username_box = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
username_box.send_keys(usr)
print("Email Id entered")

password_box = wait.until(EC.element_to_be_clickable((By.ID, 'pass')))
password_box.send_keys(pwd)
print("Password entered")

login_box = wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
login_box.click()
print("Logged in")

time.sleep(5)
driver.get('https://www.facebook.com/primary_location/info')
print("Navigated to Privacy Checkup")

try:
    # Find the element by XPath
    span_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.x193iq5w")))
    last_element = span_elements[-8].text.strip()
    with open('prim_location.txt', 'w') as file:
        file.write(last_element + '\n')
        print(f"Extracted text '{last_element}' written to logged.txt")

    driver.quit()
    print("Browser closed")
except Exception as e:
    print(f"Exception occurred: {str(e)}")