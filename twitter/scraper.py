# from time import sleep
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import Chrome, ChromeOptions
# from selenium.webdriver.support.wait import WebDriverWait
# import selenium.webdriver.support.expected_conditions as EC

# def get_tweet_data(article):
#     user = article.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.split('\n')
#     name = user[0]
#     username = user[1]
#     postdate = user[-1]
#     tweetText = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

#     return name, username, postdate, tweetText

# options = ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# driver = Chrome(options=options)

# wait = WebDriverWait(driver, 10)
# driver.get("https://twitter.com/login")

# username = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="text"]')))
# username.send_keys("saadprojet")
# username.send_keys(Keys.ENTER)

# password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
# password.send_keys('saadprojet123')
# password.send_keys(Keys.ENTER)

# search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[data-testid="SearchBox_Search_Input"]')))
# search_box.send_keys('saadprojet')
# search_box.send_keys(Keys.ENTER)

# wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]')))
# data = []
# tweet_ids = set()
# last_position = driver.execute_script("return window.pageYOffset;")
# scrolling = True

# while scrolling:
#     page_articles = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
#     for article in page_articles:
#         tweet = get_tweet_data(article)
#         if tweet:
#             tweet_id = ''.join(tweet)
#             if tweet_id not in tweet_ids:
#                 tweet_ids.add(tweet_id)
#                 data.append(tweet)

#     scroll_attempt = 0
#     while True:
#         driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
#         sleep(3)
#         current_position = driver.execute_script("return window.pageYOffset;")
#         if last_position == current_position:
#             scroll_attempt += 1

#             if scroll_attempt >= 3:
#                 scrolling = False
#                 break
#             else:
#                 sleep(2)
#         else:
#             last_position = current_position
#             break

# with open('data.txt', 'w', encoding='utf-8') as file:
#     for tweet_data in data:
#         file.write(str(tweet_data) + '\n')
#    data=[]
#     cursor = mysql.connection.cursor()
#     cursor.execute('DROP TABLE IF EXISTS tweets')
#     mysql.connection.commit()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS tweets (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         user_id INT,
#         username VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#         postdate VARCHAR(255),
#         tweetText TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#         FOREIGN KEY (user_id) REFERENCES users(id)
#     )
# ''')
#     mysql.connection.commit()
#     with open('data.txt', 'r', encoding='utf-8') as file:
#         for line in file:
#             tweet_data = eval(line)  # Convert string tuple to an actual tuple
#             data.append(tweet_data)
#     email = session['user']['email']
#     cur.execute("SELECT id FROM users WHERE email = %s", (email,))
#     user_id = cur.fetchone()[0]
# # Insert scraped data into the table
#     for tweet_data in data:
#         name, username, postdate, tweetText = tweet_data
#         tweetText = tweetText.replace("'", "''")  # Escape single quotes before insertion
#         cursor.execute("INSERT INTO tweets (user_id,name, username, postdate, tweetText) VALUES (%s, %s, %s, %s, %s)",
#                    (user_id,name, username, postdate, tweetText))

# # Commit the changes
#     mysql.connection.commit()

# # Close the cursor and connection
#     cursor.close()
#     mysql.connection.close()