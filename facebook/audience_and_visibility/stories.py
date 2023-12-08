from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

usr = "saadprojet@gmail.com"
pwd = "saadprojet123"

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")  # Disables notifications

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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

time.sleep(5)  # Delay to ensure the page loads

# Navigating to the 'Stories' section
driver.get('https://www.facebook.com/settings/?tab=stories')
print("Navigated to Stories section")

try:
    # Scroll down to load all elements
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Waiting for elements to load

    # Extract text from elements starting with 'Edit privacy'
    buttons_after_continue = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@aria-label, 'Edit privacy')]")))
    with open('stories.txt', 'w') as file:
        for button in buttons_after_continue:
            sharing_with_element = button.find_element(By.XPATH, ".//span")
            extracted_text = sharing_with_element.text.strip()
            file.write(f"{extracted_text}\n")
            print(f"Extracted text '{extracted_text}' written to stories.txt")

    # Extract text from switch elements
    switches = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[role='switch']")))
    with open('stories.txt', 'a') as file:
        for switch in switches:
            is_enabled = switch.get_attribute('checked')
            file.write(f"Is Enabled: {is_enabled}\n")
            print(f"Is Enabled: {is_enabled}")
            file.flush()  # Ensure the data is written immediately

    driver.close()
    print("Tab closed")
except Exception as e:
    print(f"Exception occurred: {str(e)}")
