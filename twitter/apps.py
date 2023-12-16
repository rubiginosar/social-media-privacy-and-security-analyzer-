import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


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
# driver.get("https://twitter.com/settings/sessions")
# time.sleep(2)

# # Find all elements within the parent element
# elements = driver.find_elements(By.CSS_SELECTOR, '[aria-selected="false"][role="tab"]')
# elems= elements[9:]
# # Write the contents to sessions.txt
# with open('sessions.txt', 'w', encoding='utf-8') as file:
#     for element in elems:
#         file.write(element.text + '\n')



# # Close the browser window
# # driver.quit()
# driver.get("https://twitter.com/settings/off_twitter_activity")
# time.sleep(2)
# # password = driver.find_element(
# #     By.XPATH, "//input[@type='password']"
# # )
# # password.send_keys("saadprojet123")
# # all_buttons = driver.find_elements(
# #     By.XPATH, "//div[@role='button']"
# # )
# # all_buttons[-1].click()

# checkbox = driver.find_element(By.CSS_SELECTOR,'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('inferred_id.txt', 'w') as file:
#     file.write(f"{is_checked}\n")

# driver.get("https://twitter.com/settings/delegate")
# time.sleep(2)
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('delegation.txt', 'w') as file:
#     if is_checked:
#         try:
#         # Target the div when the checkbox is on
#             checked_div = driver.find_element(By.CSS_SELECTOR, 'input[name="allow_others_delegation"]')
#             if checked_div.is_selected():
#                  file.write("checked: allow others delegation\n")
#             else: 
#                 file.write("checked: Only allow people you follow to invite you.")
#         except:
#             print("Checkbox is checked, but the specific div isn't.")
#     else:
#     # Target the div when the checkbox is off
#         file.write("not checked.")

# driver.get("https://twitter.com/settings/tagging")
# time.sleep(2)
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('tags.txt', 'w') as file:
#     if is_checked:
#         try:
#         # Target the div when the checkbox is on
#             elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"][name="allow_media_tagging"]')
#             position = "Anyone can tag you"
#             for element in elements:
#     # Check if the element is checked
#                 if element.is_selected():
#                     file.write(f"checked: {position}")
#                     break  # Stop the loop after finding the checked element

#     # Increment the position counter
#                 position = "Only people you follow can tag you"
#             # if checked_div.is_selected():
#             #      file.write("checked: Anyone can tag you\n")
#             # else: 
#             #     print("checked: Only people you follow can tag you.")
#         except:
#             print("Checkbox is checked, but the specific div isn't.")
#     else:
#     # Target the div when the checkbox is off
#         file.write("not checked.")

# driver.get("https://twitter.com/settings/audience_and_tagging")
# time.sleep(2)

# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('tags.txt', 'a') as file:
#     if is_checked:
#         file.write("The checkbox is checked.")
#     else:
#         file.write("The checkbox is not checked.")

# driver.get("https://twitter.com/settings/your_tweets")
# time.sleep(2)

# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('posts.txt', 'w') as file:
#     if is_checked:
#         file.write("The checkbox is checked.")
#     else:
#         file.write("The checkbox is not checked.")
# driver.get("https://twitter.com/settings/location")
# time.sleep(2)

# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('posts.txt', 'a') as file:
#     if is_checked:
#         file.write("The checkbox is checked\n.")
#     else:
#         file.write("The checkbox is not checked\n.")

# driver.get("https://twitter.com/settings/content_you_see")
# time.sleep(2)

# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('content.txt', 'w') as file:
#     if is_checked:
#         file.write("The checkbox is checked.")
#     else:
#         file.write("The checkbox is not checked.")
# driver.get("https://twitter.com/settings/search")
# time.sleep(2)

# checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# with open('search.txt', 'w') as file:
#     for checkbox in checkboxes:
#         is_checked = checkbox.is_selected()
#         if is_checked:
#             file.write("The checkbox is checked.\n")
#         else:
#             file.write("The checkbox is not checked.\n")

# driver.get("https://twitter.com/settings/notifications/advanced_filters")
# time.sleep(2)

# checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# with open('muted_notif.txt', 'w') as file:
#     for checkbox in checkboxes:
#         is_checked = checkbox.is_selected()
#         if is_checked:
#             file.write("The checkbox is checked.\n")
#         else:
#             file.write("The checkbox is not checked.\n")

# driver.get("https://twitter.com/settings/direct_messages")
# time.sleep(2)
# # checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# # Check if the checkbox is selected
# # is_checked = checkbox.is_selected()
# with open('messages.txt', 'w') as file:
#     # if is_checked:
#         try:
#         # Target the div when the checkbox is on
#             elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"][name="allow_dms_from"]')
#             position = 1
#             for element in elements:
#     # Check if the element is checked
#                 if element.is_selected():
#                     file.write(f"checked: {position}")
#                     break  # Stop the loop after finding the checked element
#  # Increment the position counter
#                 position += 1
#         except:
#             print("Checkbox is checked, but the specific div isn't.")
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('messages.txt', 'a') as file:
#     if is_checked:
#         file.write("The checkbox is checked.")
#     else:
#         file.write("The checkbox is not checked.")

# driver.get("https://twitter.com/settings/spaces")
# time.sleep(2)
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('spaces.txt', 'w') as file:
#     file.write(str(is_checked))

# driver.get("https://twitter.com/settings/contacts")
# time.sleep(2)

# checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# with open('contacts.txt', 'w') as file:
#     for checkbox in checkboxes:
#         is_checked = checkbox.is_selected()
#         if is_checked:
#             file.write("The checkbox is checked.\n")
#         else:
#             file.write("The checkbox is not checked.\n")

# driver.get("https://twitter.com/settings/data_sharing_with_business_partners")
# time.sleep(2)
# checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# is_checked = checkbox.is_selected()
# with open('data_sharing.txt', 'w') as file:
#     file.write(str(is_checked))

# driver.get("https://twitter.com/settings/account/login_verification")
# time.sleep(2)
# checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

# # Check if the checkbox is selected
# with open('2facts.txt', 'w') as file:
#     for checkbox in checkboxes:
#         is_checked = checkbox.is_selected()
#         if is_checked:
#             file.write("The checkbox is checked.\n")
#         else:
#             file.write("The checkbox is not checked.\n")
# # Close the browser window

from selenium.webdriver.common.keys import Keys
# driver.get("https://twitter.com/saadprojet")
# time.sleep(10)
driver.get("https://twitter.com/saadprojet")
time.sleep(10)
def get_tweet_data(article):
    user = article.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.split('\n')
    name = user[0]
    username = user[1]
    postdate = user[-1]
    tweetText = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

    return name, username, postdate, tweetText
SCROLL_PAUSE_TIME = 3  # Adjust the pause time between scrolls if needed

# Get scroll height
last_position = driver.execute_script("return document.body.scrollHeight")
data = []

# Your code to initiate the driver and navigate to the page

# Scroll and collect tweets until no more new tweets are loaded
scroll_attempt = 0
while True:
    page_articles = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
    for article in page_articles:
        tweet = get_tweet_data(article)
        if tweet:
            data.append(tweet)

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(3)  # Adjust the sleep time according to the page load speed

    # Check if new scroll position is the same as last scroll position
    current_position = driver.execute_script("return window.pageYOffset;")
    if last_position == current_position:
        scroll_attempt += 1
        if scroll_attempt >= 3:  # You can adjust the number of attempts
            break  # Exit the loop if no new tweets are loaded after multiple attempts
    else:
        last_position = current_position
        scroll_attempt = 0  # Reset scroll attempt counter

# Write collected tweets to a file
with open('data.txt', 'w', encoding='utf-8') as file:
    for tweet_data in data:
        file.write(str(tweet_data) + '\n')
# Find tweet elements
# tweet_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')


# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# Extract tweet content
# user_name_element = driver.find_elements(By.XPATH,'//span[contains(@class, "css-1qaijid") and contains(text(), "@")]')
# user_name = user_name_element[1].text

# # Find and extract time
# time_element = driver.find_element(By.CSS_SELECTOR,'time')
# time = time_element.get_attribute('datetime')
# div_element = driver.find_elements(By.CSS_SELECTOR,'div[data-testid="tweetText"]')
# div_text = div_element.text

# # Write extracted data to a file
# with open('data.txt', 'w') as file:
#     file.write(f"User Name: {user_name}\n")
#     file.write(f"Time: {time}\n")
#     file.write(f"Text: {div_text}\n")

driver.get("https://twitter.com/saadprojet")
time.sleep(10)
driver.quit()