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
driver.get('https://www.facebook.com/your_information/?tab=your_information&tile=personal_info_grouping')
print("Navigated to Privacy Checkup")
try:
    main_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Your contact information')]")))
    main_element.click()  # Click on the found element
    
    time.sleep(2)  # Give time for the page to load after clicking

    # Find the specific element with the desired classes
    target_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'xzpqnlu') and contains(@class, 'x179tack') and contains(@class, 'x10l6tqk')]")))

    with open('contact.txt', 'w') as file:
        for target_element in target_elements:
            # Get the text inside each element
            text_inside_element = target_element.text.strip()
            file.write(f"{text_inside_element}\n")
            print(f"Text inside the element: {text_inside_element}")

    driver.quit()
    print("Browser closed")
except Exception as e:
    print(f"Exception occurred: {str(e)}")