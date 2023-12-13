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
driver.get("https://twitter.com/settings/sessions")
time.sleep(2)

# Find all elements within the parent element
elements = driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"][role="tab"]')
elems= elements[9:]
# Write the contents to sessions.txt
with open('sessions.txt', 'w', encoding='utf-8') as file:
    for element in elems:
        file.write(element.text + '\n')

# Close the browser window
# driver.quit()
driver.get("https://twitter.com/settings/off_twitter_activity")
time.sleep(2)
# password = driver.find_element(
#     By.XPATH, "//input[@type='password']"
# )
# password.send_keys("saadprojet123")
# all_buttons = driver.find_elements(
#     By.XPATH, "//div[@role='button']"
# )
# all_buttons[-1].click()

checkbox = driver.find_element(By.CSS_SELECTOR,'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('inferred_id.txt', 'w') as file:
    file.write(f"{is_checked}\n")

driver.get("https://twitter.com/settings/delegate")
time.sleep(2)
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('delegation.txt', 'w') as file:
    if is_checked:
        try:
        # Target the div when the checkbox is on
            checked_div = driver.find_element(By.CSS_SELECTOR, 'input[name="allow_others_delegation"]')
            if checked_div.is_selected():
                 file.write("checked: allow others delegation\n")
            else: 
                file.write("checked: Only allow people you follow to invite you.")
        except:
            print("Checkbox is checked, but the specific div isn't.")
    else:
    # Target the div when the checkbox is off
        file.write("not checked.")

driver.get("https://twitter.com/settings/tagging")
time.sleep(2)
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('tags.txt', 'w') as file:
    if is_checked:
        try:
        # Target the div when the checkbox is on
            elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"][name="allow_media_tagging"]')
            position = "Anyone can tag you"
            for element in elements:
    # Check if the element is checked
                if element.is_selected():
                    file.write(f"checked: {position}")
                    break  # Stop the loop after finding the checked element

    # Increment the position counter
                position = "Only people you follow can tag you"
            # if checked_div.is_selected():
            #      file.write("checked: Anyone can tag you\n")
            # else: 
            #     print("checked: Only people you follow can tag you.")
        except:
            print("Checkbox is checked, but the specific div isn't.")
    else:
    # Target the div when the checkbox is off
        file.write("not checked.")

driver.get("https://twitter.com/settings/audience_and_tagging")
time.sleep(2)

checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('tags.txt', 'a') as file:
    if is_checked:
        file.write("The checkbox is checked.")
    else:
        file.write("The checkbox is not checked.")

driver.get("https://twitter.com/settings/your_tweets")
time.sleep(2)

checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('posts.txt', 'w') as file:
    if is_checked:
        file.write("The checkbox is checked.")
    else:
        file.write("The checkbox is not checked.")
driver.get("https://twitter.com/settings/location")
time.sleep(2)

checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('posts.txt', 'a') as file:
    if is_checked:
        file.write("The checkbox is checked\n.")
    else:
        file.write("The checkbox is not checked\n.")

driver.get("https://twitter.com/settings/content_you_see")
time.sleep(2)

checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('content.txt', 'w') as file:
    if is_checked:
        file.write("The checkbox is checked.")
    else:
        file.write("The checkbox is not checked.")
driver.get("https://twitter.com/settings/search")
time.sleep(2)

checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
with open('search.txt', 'w') as file:
    for checkbox in checkboxes:
        is_checked = checkbox.is_selected()
        if is_checked:
            file.write("The checkbox is checked.\n")
        else:
            file.write("The checkbox is not checked.\n")

driver.get("https://twitter.com/settings/notifications/advanced_filters")
time.sleep(2)

checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
with open('muted_notif.txt', 'w') as file:
    for checkbox in checkboxes:
        is_checked = checkbox.is_selected()
        if is_checked:
            file.write("The checkbox is checked.\n")
        else:
            file.write("The checkbox is not checked.\n")

driver.get("https://twitter.com/settings/direct_messages")
time.sleep(2)
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# Check if the checkbox is selected
# is_checked = checkbox.is_selected()
with open('messages.txt', 'w') as file:
    # if is_checked:
        try:
        # Target the div when the checkbox is on
            elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"][name="allow_dms_from"]')
            position = 1
            for element in elements:
    # Check if the element is checked
                if element.is_selected():
                    file.write(f"checked: {position}")
                    break  # Stop the loop after finding the checked element
 # Increment the position counter
                position += 1
        except:
            print("Checkbox is checked, but the specific div isn't.")
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('messages.txt', 'a') as file:
    if is_checked:
        file.write("The checkbox is checked.")
    else:
        file.write("The checkbox is not checked.")

driver.get("https://twitter.com/settings/spaces")
time.sleep(2)
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('spaces.txt', 'w') as file:
    file.write(str(is_checked))

driver.get("https://twitter.com/settings/contacts")
time.sleep(2)

checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
with open('contacts.txt', 'w') as file:
    for checkbox in checkboxes:
        is_checked = checkbox.is_selected()
        if is_checked:
            file.write("The checkbox is checked.\n")
        else:
            file.write("The checkbox is not checked.\n")

driver.get("https://twitter.com/settings/data_sharing_with_business_partners")
time.sleep(2)
checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
is_checked = checkbox.is_selected()
with open('data_sharing.txt', 'w') as file:
    file.write(str(is_checked))

driver.get("https://twitter.com/settings/account/login_verification")
time.sleep(2)
checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# Check if the checkbox is selected
with open('2facts.txt', 'w') as file:
    for checkbox in checkboxes:
        is_checked = checkbox.is_selected()
        if is_checked:
            file.write("The checkbox is checked.\n")
        else:
            file.write("The checkbox is not checked.\n")
# Close the browser window
driver.quit()