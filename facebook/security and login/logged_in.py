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
driver.get('https://www.facebook.com/100060663511589/allactivity?category_key=ACTIVESESSIONS&entry_point=ayi_hub')
print("Navigated to Privacy Checkup")

try:
    main_elements = driver.find_elements(By.XPATH, "//span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h']/span[@class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']")
    with open('logged.txt', 'w') as file:
        for main_element in main_elements:
            text = main_element.text.strip()
            file.write(f"{text}\n")
            print(f"Extracted text '{text}' written to logged.txt")
        elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1xmvt09') and contains(@class, 'x1lliihq') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'x4zkp8e') and contains(@class, 'x3x7a5m') and contains(@class, 'x1nxh6w3') and contains(@class, 'x1sibtaa') and contains(@class, 'xo1l8bm') and contains(@class, 'xzsf02u') and contains(@class, 'x1yc453h')]")
        for element in elements:
            sub_element = element.find_element(By.XPATH, "./span[contains(@class, 'x1lliihq')]")
            text = sub_element.text.strip()
            file.write(f"{text}\n")
            print(f"Extracted text '{text}' written to logged.txt")


    driver.quit()
    print("Browser closed")
except Exception as e:
    print(f"Exception occurred: {str(e)}")