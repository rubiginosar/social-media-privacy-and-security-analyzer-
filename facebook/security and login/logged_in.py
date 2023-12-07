from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json

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

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

# Extract text from all date elements
dates = [date_element.text.strip() for date_element in date_elements]

# Write extracted data to comments.txt file
with open('log_in.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(dates))

# Quit the WebDriver
driver.quit()
import re

with open('log_in.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Split the text into date-comment pairs
comments = re.findall(r'(\w+ \d{1,2}, \d{4})\n([\s\S]*?)(?=\w+ \d{1,2}, \d{4}\n|\Z)', data)

# Organize comments by date
comments_data = {}
current_date = None

for comment in comments:
    date = comment[0]
    comment_text = comment[1].strip().split('\n')  # Split multiple comments into a list
    
    if current_date == date:
        comments_data[date].extend(comment_text)
    else:
        current_date = date
        comments_data[date] = comment_text

# Save as JSON with comments as separate strings
with open('log_in.json', 'w', encoding='utf-8') as json_file:
    json.dump(comments_data, json_file, ensure_ascii=False, indent=4)
