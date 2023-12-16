from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import time
import json
import re
import os
from flask import Flask, render_template, request,redirect, session
from flask_mysqldb import MySQL
import pymysql


app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_root'
app.config['MYSQL_DB'] = 'projet'
app.config['MYSQL_PORT'] = 3307 
app.config['MYSQL_CHARSET'] = 'utf8mb4' 

mysql = MySQL(app)
#################definition des fonctions#################
import bcrypt

# Hash a password
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

# Verify a password
def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

# Example of hashing a password before storing it in the database
# password = "user_password"
# hashed_password = hash_password(password)

def login_is_valid(username_or_email, password):
    # This is where you would perform your actual validation logic
    # For instance, querying your database to check if the credentials are valid
    # Replace this logic with your own logic to validate the user

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username_or_email, username_or_email))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return True  # Valid credentials
    else:
        return False  # Invalid credentials

#################definition des fonctions#################
@app.route('/')
def home():
    return render_template('projet.html')

# @app.route('/registration')
# def registration():
#     return render_template('registration.html')
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                # Password matches, log the user in
                user_id = user[0]  # Assuming user_id is in the first position
                session['user'] = {'email': email, 'user_id': user_id}
                return render_template('Login.html')  # Redirect to the dashboard after successful login

        # Invalid credentials or user does not exist
            else:
                return "Invalid email or password. Please try again or register."

    return render_template('registration.html')

# def registration():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Check if the user exists
#         with mysql.connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
#     # Password matches, log the user in
#                 session['user'] = {'email': email,}
#                 return render_template('chose.html')  # Redirect to the dashboard after successful login
#             else:
#     # Invalid credentials
#                 return "Invalid email or password. Please try again or register."

#     return render_template('registration.html')



# @app.route('/register')
# def register():
#     return render_template('register.html') 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Hash the password before storing it in the database
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            # User already exists with the given email
            return "User with this email already exists!"
        else:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
            mysql.connection.commit()
            cur.close()
            user_id = user[0]  # Assuming user_id is in the first position
            session['user'] = {'email': email, 'user_id': user_id}
            # session['user'] = {'email': email}
            return render_template('chose.html')  # Redirect to login page after registration
    return render_template('register.html')

@app.route('/options')
def options():
    return render_template('options.html') 

@app.route('/Login')
def Login():
    return render_template('chose.html') 

# @app.route('/dashboard/<platform>')
# def dashboard(platform):
#     if platform == 'Facebook':
#         return render_template('dashboradfb.html')
#     elif platform == 'Twitter':
#         return render_template('dashboardtw.html')
#     else:
#         # Handle cases where an invalid platform is requested
#         return "Invalid platform requested"

@app.route('/dashboard1')
def dashboard1():
    cur = mysql.connection.cursor()
    email = session['user']['email']
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cur.fetchone()[0]
    
    facebook_menaces_query = """
    SELECT date, comment, table_name
    FROM projet.menaces
    WHERE table_name IN ('comments', 'likes', 'post', 'tag', 'search')
    AND user_id = %s
    ORDER BY date DESC
    LIMIT 15
    """
    cur.execute(facebook_menaces_query, (user_id,))
    latest_facebook_menaces = cur.fetchall()


    logins_query = """
    SELECT DISTINCT date, login_action
    FROM projet.logins
    WHERE user_id = %s
    LIMIT 20
"""
    cur.execute(logins_query, (user_id,))
    unique_logins = cur.fetchall()

    devices_query = """
    SELECT DISTINCT date, device
    FROM projet.devices
    WHERE user_id = %s
    LIMIT 20
"""
    cur.execute(devices_query, (user_id,))
    unique_devices = cur.fetchall()
    
    return render_template('dashboradfb.html', latest_facebook_menaces=latest_facebook_menaces, unique_logins=unique_logins, unique_devices=unique_devices)


@app.route('/dashboard2')
def dashboard2():
    cur = mysql.connection.cursor()
    email = session['user']['email']
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cur.fetchone()[0]
    query = """
        SELECT
        device,
        date,
        location
        FROM
        projet.twt_sessions
        WHERE
        user_id = %s
        ORDER BY
        date DESC
        LIMIT
        15
    """

    cur.execute(query, (user_id,))
    latest_sessions = cur.fetchall()
    tweet_menaces_query = """
    SELECT date, comment
    FROM projet.menaces
    WHERE table_name = 'tweet'
    AND
    user_id = %s
    ORDER BY
    date DESC
    LIMIT
    15
"""
    cur.execute(tweet_menaces_query,(user_id,))
    latest_tweet_menaces = cur.fetchall()

    return render_template('dashboardtw.html',latest_sessions=latest_sessions,latest_tweet_menaces=latest_tweet_menaces) 
# @app.route('/Login1')
# def Login1():
#     return render_template('Login1.html') 


# @app.route('/chose')
# def chose():
#     return render_template('chose.html') 


@app.route('/chose', methods=['GET', 'POST'])
def chose():
    if request.method == 'POST':
        if 'platform' in request.form:
            platform = request.form['platform']

            if platform == 'Facebook':
                return redirect('/analyze')
            elif platform == 'Twitter':
                return redirect('/analyze1')

    return render_template('chose.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'platform' in request.form:
            platform = request.form['platform']

            if platform == 'Facebook':
                return redirect('/dashboard1')
            elif platform == 'Twitter':
                return redirect('/dashboard2')

    return render_template('dashboard.html')

@app.route('/password')
def password():
    return render_template('password.html')

@app.route('/save_strength', methods=['POST'])
def save_strength():
    password_strength = request.form.get('password_strength')

    if password_strength:
        with open('password_strength.txt', 'w') as file:
            file.write(password_strength)

    return redirect('facebook_analysis')

@app.route('/analyze')
def analyze():
    # Add code for rendering the Facebook analysis page
    return render_template('analyse.html')

@app.route('/analyze1')
def analyze1():
    # Add code for rendering the Facebook analysis page
    return render_template('analyse1.html')

@app.route('/analyze_facebook', methods=['POST'])
def analyze_facebook():
    #Your Inform
    #usr = "saadprojet@gmail.com"
    #pwd = "saadprojet123"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.facebook.com/')
    print("Opened Facebook")

    wait = WebDriverWait(driver, 10)

    username_box = wait.until(EC.element_to_be_clickable((By.ID, 'email')))
    #username_box.send_keys(usr)
    print("Email Id entered")

    password_box = wait.until(EC.element_to_be_clickable((By.ID, 'pass')))
    #password_box.send_keys(pwd)
    print("Password entered")

    login_box = wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
    #login_box.click()
    print("Logged in")

    try:
        #contact information
        time.sleep(25)
        driver.get('https://www.facebook.com/your_information/?tab=your_information&tile=personal_info_grouping')
        print("Navigated to Privacy Checkup")
        time.sleep(5)
        main_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Your contact information')]")))
        main_element.click()  # Click on the found element
        
        time.sleep(5)  # Give time for the page to load after clicking

        # Find the specific element with the desired classes
        target_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'xzpqnlu') and contains(@class, 'x179tack') and contains(@class, 'x10l6tqk')]")))

        with open('facebook.txt', 'w') as file:
            for target_element in target_elements:
                text_inside_element = target_element.text.strip()
                if text_inside_element:  # Vérifier si le texte n'est pas vide
                    file.write(f"{text_inside_element}\n")
                    print(f"Text inside the element: {text_inside_element}")
        
        time.sleep(2)  # Delay to ensure the page loads

        # how people can find you and contcat you
        driver.get('https://www.facebook.com/settings/?tab=how_people_find_and_contact_you')
        print("Navigated to how people can find you and contact you ")

        # Scroll down to the buttons using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Extract text from elements starting with 'Edit privacy'
        buttons_after_continue = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@aria-label, 'Edit privacy')]")))
        with open('facebook.txt', 'a') as file:
            for button in buttons_after_continue:
                sharing_with_element = button.find_element(By.XPATH, ".//span")
                extracted_text = sharing_with_element.text.strip()
                if extracted_text:
                    file.write(f"{extracted_text}\n")
                    print(f"Extracted text '{extracted_text}' written to find.txt")
        
        checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[role='switch']")))
        is_enabled = checkbox.get_attribute('checked')
        
        with open('facebook.txt', 'a') as file:
            file.write(f"Is Enabled: {is_enabled}\n")
            print(f"Is Enabled: {is_enabled}")
        
        message_requests_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[contains(@class, "x1lliihq") and contains(@class, "x6ikm8r") and contains(@class, "x10wlt62") and contains(@class, "x1n2onr6")]/ancestor::div[contains(@class, "x1i10hfl")]')))
        with open('facebook.txt', 'a') as file:
            for button in message_requests_buttons:
                button_text = button.text.strip() if button.text else "No text available"
                file.write(f"{button_text}\n")
                print("Text inside the button:", button_text)
        # Navigating to the desired link
        time.sleep(2)  # Delay to ensure the page loads
        #followers and public content
        driver.get('https://www.facebook.com/settings/?tab=followers_and_public_content')
        print("Navigated to followers and public content") 
        # Scroll down to the buttons using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elements = driver.find_elements(By.CLASS_NAME, 'x1i10hfl')  # Replace 'x1i10hfl' with the actual class name
        
        last_six_elements =elements[-9:-7] + elements[-5:-2]
        
        with open('facebook.txt', 'a') as file:
            for element in last_six_elements:
                text = element.text.strip()
                if text:
                    file.write(f"{text}\n")
                    print(f"Extracted text '{text}' written to last_six_elements.txt")

        switches = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[role='switch']")))
        with open('facebook.txt', 'a') as file:
            for switch in switches:
                is_enabled = switch.get_attribute('checked')
                file.write(f"Is Enabled: {is_enabled}\n")
                print(f"Is Enabled: {is_enabled}")
                file.flush()  # Ensure the data is written immediately
        #login alerts
        time.sleep(2)
        driver.get('https://accountscenter.facebook.com/password_and_security/login_alerts')
        print("Navigated to login alerts")
        span_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.x1lliihq")))
        last_element = span_elements[-1].text.strip()
        
        with open('facebook.txt', 'a') as file:
            file.write(last_element + '\n')
            print(f"Extracted text '{last_element}' written to last_element.txt")
        time.sleep(2) # Delay to ensure the page loads

        # Navigating to posts
        driver.get('https://www.facebook.com/settings/?tab=posts')
        print("Navigated to Privacy Checkup")
        # Scroll down to the buttons using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Extract text from elements starting with 'Edit privacy'
        buttons_after_continue = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@aria-label, 'Edit privacy')]")))
        with open('facebook.txt', 'a') as file:
            for button in buttons_after_continue:
                sharing_with_element = button.find_element(By.XPATH, ".//span")
                extracted_text = sharing_with_element.text.strip()
                if extracted_text:
                    file.write(f"{extracted_text}\n")
                    print(f"Extracted text '{extracted_text}' written to post.txt") 
        time.sleep(2)  # Delay to ensure the page loads

        # Navigating to the 'Stories' section
        driver.get('https://www.facebook.com/settings/?tab=stories')
        print("Navigated to Stories section")     
        # Scroll down to load all elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Waiting for elements to load

        # Extract text from elements starting with 'Edit privacy'
        buttons_after_continue = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@aria-label, 'Edit privacy')]")))
        with open('facebook.txt', 'a') as file:
            for button in buttons_after_continue:
                sharing_with_element = button.find_element(By.XPATH, ".//span")
                extracted_text = sharing_with_element.text.strip()
                file.write(f"{extracted_text}\n")
                print(f"Extracted text '{extracted_text}' written to stories.txt")

        # Extract text from switch elements
        switches = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[role='switch']")))
        with open('facebook.txt', 'a') as file:
            for switch in switches:
                is_enabled = switch.get_attribute('checked')
                file.write(f"Is Enabled: {is_enabled}\n")
                print(f"Is Enabled: {is_enabled}")
                file.flush()  # Ensure the data is written immediately 
        time.sleep(2) # Delay to ensure the page loads

        # Navigating to profile and tagging
        driver.get('https://www.facebook.com/settings/?tab=profile_and_tagging')
        print("Navigated to Privacy Checkup")
        # Scroll down to the buttons using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[starts-with(@aria-label, 'Edit privacy')]")))
        
        with open('facebook.txt', 'a') as file:
            for element in elements:
                text = element.text.strip()
                if text:  # Vérifier si le texte n'est pas vide
                    file.write(f"{text}\n")
                    print(f"Extracted text '{text}' written to tagging.txt")

        switches = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[role='switch']")))
        with open('facebook.txt', 'a') as file:
            for switch in switches:
                is_enabled = switch.get_attribute('checked')
                file.write(f"Is Enabled: {is_enabled}\n")
                print(f"Is Enabled: {is_enabled}")
                file.flush()  # Assurez-vous que les données sont écrites immédiatement

        time.sleep(5)
        driver.get('https://www.facebook.com/100060663511589/allactivity?activity_history=false&category_key=COMMENTSCLUSTER&manage_mode=false&should_load_landing_page=false')
        time.sleep(2)
        print("Navigated to interactions, your comments")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

        # Extract text from all date elements
        dates = [date_element.text.strip() for date_element in date_elements]

        # Write extracted data to comments.txt file
        with open('comments.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(dates))
        with open('comments.txt', 'r', encoding='utf-8') as file:
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

        cur = mysql.connection.cursor()
        email = session['user']['email']
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()[0]
        for date, comments_list in comments_data.items():
            for comment_text in comments_list:
                cur.execute("INSERT INTO comments (user_id, date, comment) VALUES (%s, %s, %s)",
                    (user_id, f'{date}', comment_text))
                mysql.connection.commit()
        
        #devices
        driver.get('https://www.facebook.com/100060663511589/allactivity?activity_history=false&category_key=RECOGNIZEDDEVICES&manage_mode=false&should_load_landing_page=false')
        print("Navigated to Privacy Checkup")
        time.sleep(5)
        date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

# Extract text from all date elements
        dates = [date_element.text.strip() for date_element in date_elements]
        with open('devices.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(dates))
        with open('devices.txt', 'r', encoding='utf-8') as file:
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

# Save as JSON with comments as separate stringscur = mysql.connection.cursor()
        email = session['user']['email']
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()[0]
        for date, comments_list in comments_data.items():
                for comments_text in comments_list:
                    cur.execute("INSERT INTO devices (user_id, date, device) VALUES (%s, %s, %s)",
                    (user_id, f'{date}', comment_text))
                    mysql.connection.commit()
        

        time.sleep(5)
        driver.get('https://www.facebook.com/100060663511589/allactivity/?category_key=LIKEDPOSTS&entry_point=ayi_hub')
        time.sleep(2)
        print("Navigated to Privacy Checkup")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

        # Extract text from all date elements
        dates = [date_element.text.strip() for date_element in date_elements]

        # Write extracted data to comments.txt file
        with open('likes.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(dates))

        with open('likes.txt', 'r', encoding='utf-8') as file:
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
        
        cur = mysql.connection.cursor()
        email = session['user']['email']
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()[0]  # Retrieve the user's ID from the database

    # Assuming you have extracted data and stored it in variables like 'target_elements', 'span_elements', 'posts_data', 'devices_data'
    # Replace these with your actual extracted data

    # Insert extracted contact information into facebook_contact_info table
        for date, comments_list in comments_data.items():
            for comment_text in comments_list:
                cur.execute("INSERT INTO likes (user_id, date, like_action) VALUES (%s, %s, %s)",
                    (user_id, f'{date}', comment_text))
                mysql.connection.commit()
        
        time.sleep(5)
        #primary location
        driver.get('https://www.facebook.com/primary_location/info')
        print("Navigated to primary location")

        # Find the element by XPath
        span_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.x193iq5w")))
        last_element = span_elements[-8].text.strip()
        with open('prim_location.txt', 'w') as file:
            file.write(last_element + '\n')
            print(f"Extracted text '{last_element}' written to logged.txt")
        # cur = mysql.connection.cursor()
        # email = session['user']['email']
        # cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        # user_id = cur.fetchone()[0]
        # cur.execute("INSERT INTO prim_location (user_id, location) VALUES (%s, %s)", (user_id,{last_element},))
        # mysql.connection.commit()
        time.sleep(5)
        #logged in
        driver.get('https://www.facebook.com/100060663511589/allactivity?category_key=ACTIVESESSIONS&entry_point=ayi_hub')
        print("Navigated to logged in")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

# Extract text from all date elements
        dates = [date_element.text.strip() for date_element in date_elements]

# Write extracted data to comments.txt file
        with open('log_in.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(dates))
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
            
            cur = mysql.connection.cursor()
            email = session['user']['email']
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]
            for date, comments_list in comments_data.items():
                for comments_text in comments_list:
                    cur.execute("INSERT INTO logins (user_id, date, login_action) VALUES (%s, %s, %s)",
            (user_id, date, comments_text))
                    mysql.connection.commit()

            time.sleep(5)
            driver.get('https://www.facebook.com/100060663511589/allactivity?activity_history=false&category_key=MANAGEPOSTSPHOTOSANDVIDEOS&manage_mode=false&should_load_landing_page=false')
            time.sleep(2)
            print("Navigated to Privacy Checkup")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

            # Extract text from all date elements
            dates = [date_element.text.strip() for date_element in date_elements]

            # Write extracted data to comments.txt file
            with open('posts.txt', 'w', encoding='utf-8') as file:
                file.write('\n'.join(dates))


            with open('posts.txt', 'r', encoding='utf-8') as file:
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

            cur = mysql.connection.cursor()
            email = session['user']['email']
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]
            for date, comments_list in comments_data.items():
                for comments_text in comments_list:
                    cur.execute("INSERT INTO posts (user_id, date, post_content) VALUES (%s, %s, %s)",
                    (user_id, f'{date}', comment_text))
                    mysql.connection.commit()

            time.sleep(5)
            driver.get('https://www.facebook.com/100060663511589/allactivity?activity_history=false&category_key=MANAGETAGSBYOTHERSCLUSTER&manage_mode=false&should_load_landing_page=false')
            time.sleep(2)
            print("Navigated to Privacy Checkup")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

            # Extract text from all date elements
            dates = [date_element.text.strip() for date_element in date_elements]

            # Write extracted data to comments.txt file
            with open('tags.txt', 'w', encoding='utf-8') as file:
                file.write('\n'.join(dates))
            with open('tags.txt', 'r', encoding='utf-8') as file:
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

            cur = mysql.connection.cursor()
            email = session['user']['email']
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]
            for date, comments_list in comments_data.items():
                for comments_text in comments_list:
                    cur.execute("INSERT INTO tags (user_id, date, tag_content) VALUES (%s, %s, %s)",
                    (user_id, f'{date}', comment_text))
                    mysql.connection.commit()
            time.sleep(5)
            driver.get('https://www.facebook.com/100060663511589/allactivity?activity_history=false&category_key=SEARCH&manage_mode=false&should_load_landing_page=false')
            time.sleep(2)
            print("Navigated to Privacy Checkup")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            date_elements = driver.find_elements('css selector', 'span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6.x1j85h84')

# Extract text from all date elements
            dates = [date_element.text.strip() for date_element in date_elements]

# Write extracted data to comments.txt file
            with open('search.txt', 'w', encoding='utf-8') as file:
                file.write('\n'.join(dates))

            with open('search.txt', 'r', encoding='utf-8') as file:
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
                cur = mysql.connection.cursor()
                email = session['user']['email']
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                user_id = cur.fetchone()[0]
                for date, comments_list in comments_data.items():
                    for comment_text in comments_list:
                        if isinstance(comment_text, list):  # Check if comment_text is a list
                            for text in comment_text:
                                cur.execute("INSERT INTO searches (user_id, date, search) VALUES (%s, %s, %s)",
                            (user_id, f'{date}', text))
                        else:
                            cur.execute("INSERT INTO searches (user_id, date, search) VALUES (%s, %s, %s)",
                        (user_id, f'{date}', comment_text))
                            mysql.connection.commit()

            driver.quit()
        print("Browser closed")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    return ''

@app.route('/analyze_twitter', methods=['POST'])
def analyze_twitter():
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

# Read data from sessions.txt and filter out lines with '·'
    with open('sessions.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines() if '·' not in line]

        sessions = []
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                platform_location = lines[i].strip()
                time_info = lines[i + 2].strip()
                session_data = {
            'platform': platform_location,
            'location': lines[i + 1].strip(),
            'time': time_info
        }
                sessions.append(session_data)
            else:
                break  # Exit the loop if there are not enough lines for a complete set

# MySQL Database Insertion
        cur = mysql.connection.cursor()
        email = session['user']['email']
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        user_id = cur.fetchone()[0]

        for session_data in sessions:
            timestamp = session_data['time']
            device = session_data['platform']
            location = session_data['location']
            

            cur.execute("INSERT INTO twt_sessions (date, device, location, user_id) VALUES (%s, %s, %s, %s)",
                (timestamp, device, location, user_id))
        mysql.connection.commit()

        cur.close()  # Close the cursor after all operations are done

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
    with open('twitter.txt', 'w') as file:
        file.write(f"{is_checked}\n")

    driver.get("https://twitter.com/settings/delegate")
    time.sleep(2)
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
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
            file.write("not checked\n")

    driver.get("https://twitter.com/settings/tagging")
    time.sleep(2)
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            try:
            # Target the div when the checkbox is on
                elements = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"][name="allow_media_tagging"]')
                position = "Anyone can tag you"
                for element in elements:
        # Check if the element is checked
                    if element.is_selected():
                        file.write(f"checked: {position}\n")
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
            file.write("not checked\n")

    driver.get("https://twitter.com/settings/audience_and_tagging")
    time.sleep(2)

    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            file.write("The checkbox is checked\n")
        else:
            file.write("The checkbox is not checked\n")

    driver.get("https://twitter.com/settings/your_tweets")
    time.sleep(2)

    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            file.write("The checkbox is checked")
        else:
            file.write("The checkbox is not checked")
    driver.get("https://twitter.com/settings/location")
    time.sleep(2)

    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            file.write("\nThe checkbox is checked\n")
        else:
            file.write("\nThe checkbox is not checked\n")

    driver.get("https://twitter.com/settings/content_you_see")
    time.sleep(2)

    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            file.write("The checkbox is checked\n")
        else:
            file.write("The checkbox is not checked\n")
    driver.get("https://twitter.com/settings/search")
    time.sleep(2)

    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    with open('twitter.txt', 'a') as file:
        for checkbox in checkboxes:
            is_checked = checkbox.is_selected()
            if is_checked:
                file.write("The checkbox is checked\n")
            else:
                file.write("The checkbox is not checked\n")

    driver.get("https://twitter.com/settings/notifications/advanced_filters")
    time.sleep(2)

    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    with open('twitter.txt', 'a') as file:
        for checkbox in checkboxes:
            is_checked = checkbox.is_selected()
            if is_checked:
                file.write("The checkbox is checked\n")
            else:
                file.write("The checkbox is not checked\n")

    driver.get("https://twitter.com/settings/direct_messages")
    time.sleep(2)
    # checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

    # Check if the checkbox is selected
    # is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
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
                print("Checkbox is checked, but the specific div isn't")
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        if is_checked:
            file.write("\nThe checkbox is checked")
        else:
            file.write("\nThe checkbox is not checked\n")

    driver.get("https://twitter.com/settings/spaces")
    time.sleep(2)
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][role="switch"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        file.write(f"\n{str(is_checked)}")

    driver.get("https://twitter.com/settings/contacts")
    time.sleep(2)

    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    with open('twitter.txt', 'a') as file:
        for checkbox in checkboxes:
            is_checked = checkbox.is_selected()
            if is_checked:
                file.write("\nThe checkbox is checked")
            else:
                file.write("\nThe checkbox is not checked")

    driver.get("https://twitter.com/settings/data_sharing_with_business_partners")
    time.sleep(2)
    checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    is_checked = checkbox.is_selected()
    with open('twitter.txt', 'a') as file:
        file.write(f"\n{str(is_checked)}")

    driver.get("https://twitter.com/settings/account/login_verification")
    time.sleep(2)
    checkboxes = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')

    # Check if the checkbox is selected
    with open('twitter.txt', 'a') as file:
        for checkbox in checkboxes:
            is_checked = checkbox.is_selected()
            if is_checked:
                file.write("\nThe checkbox is checked")
            else:
                file.write("\nThe checkbox is not checked")

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
    # Close the browser window
        driver.quit()
    data=[]
    cursor = mysql.connection.cursor()
#     cursor.execute('DROP TABLE IF EXISTS tweets')
#     mysql.connection.commit()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS tweets (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         user_id INT,
#         name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#         username VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#         postdate VARCHAR(255),
#         tweetText TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
#         FOREIGN KEY (user_id) REFERENCES users(id)
#     )
# ''')
#     mysql.connection.commit()
    email = session['user']['email']
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()[0]
    with open('data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            tweet_data = eval(line)  # Convert string tuple to an actual tuple
            data.append(tweet_data)
# Insert scraped data into the table
    for tweet_data in data:
        name, username, postdate, tweetText = tweet_data
        tweetText = tweetText.replace("'", "''")  # Escape single quotes before insertion
        cursor.execute("INSERT INTO tweets (user_id,name, username, postdate, tweetText) VALUES (%s, %s, %s, %s, %s)",
                   (user_id,name, username, postdate, tweetText))

# Commit the changes
    mysql.connection.commit()

# Close the cursor and connection
    cursor.close()
    mysql.connection.close()

    return ''

from difflib import SequenceMatcher

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def calculate_similarity_percentage(file1, file2):
    # Use SequenceMatcher to compare the two files
    sequence_matcher = SequenceMatcher(None, file1, file2)
    similarity_ratio = sequence_matcher.ratio()

    # Calculate the percentage similarity
    similarity_percentage = int(similarity_ratio * 90)

    return similarity_percentage

@app.route('/pourcentage')

def pourcentage():
    file_path_facebook = 'facebook.txt'
    file_path_ideal = 'Ideal1.txt'

    # Read the contents of the files
    facebook_content = read_file(file_path_facebook)
    ideal_content = read_file(file_path_ideal)

    # Calculate the similarity percentage
    percentage = calculate_similarity_percentage(facebook_content, ideal_content)

    # Read the content of the password_strength file
    with open('password_strength.txt', 'r') as file:
        password_strength_content = file.read()

    # Update the percentage based on the content of password_strength
    if 'Weak' in password_strength_content:
        percentage += 3
    elif 'Medium' in password_strength_content:
        percentage += 5
    elif 'Strong' in password_strength_content:
        percentage += 10

    # Define a function to check comments for negative/hate speech
    def check_comments_for_menaces():
        # Establish a database connection within the application context
        with app.app_context():
            cur=mysql.connection.cursor()
            email = session['user']['email']
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            user_id = cur.fetchone()[0]
            cur.execute("SELECT date, comment FROM comments WHERE user_id = %s",(user_id,))
            comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
            with open('negative_words.txt', 'r') as file:
                negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
            for date, comment_text in comments_data:
                for word in negative_words:
                    if word in comment_text:
                        # Save detected comments to the 'menaces' table
                        cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s, %s, %s, %s)",
                                    (user_id,'comments', date, comment_text))
                        mysql.connection.commit()
                        break  # Break once a negative word is found in the comment
            
            cur.execute("SELECT date, like_action FROM likes WHERE user_id = %s",(user_id,))
            comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
            with open('negative_words.txt', 'r') as file:
                negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
            for date, comment_text in comments_data:
                for word in negative_words:
                    if word in comment_text:
                        # Save detected comments to the 'menaces' table
                        cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s, %s, %s, %s)",
                                    (user_id,'likes', date, comment_text))
                        mysql.connection.commit()
                        break  # Break once a negative word is found in the comment
            
            cur.execute("SELECT date, tag_content FROM tags WHERE user_id = %s",(user_id,))
            comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
            with open('negative_words.txt', 'r') as file:
                negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
            for date, comment_text in comments_data:
                for word in negative_words:
                    if word in comment_text:
                        # Save detected comments to the 'menaces' table
                        cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s, %s, %s, %s)",
                                    (user_id,'tag', date, comment_text))
                        mysql.connection.commit()
                        break  # Break once a negative word is found in the comment
            
            cur.execute("SELECT date, search FROM searches WHERE user_id = %s",(user_id,))
            comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
            with open('negative_words.txt', 'r') as file:
                negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
            for date, comment_text in comments_data:
                for word in negative_words:
                    if word in comment_text:
                        # Save detected comments to the 'menaces' table
                        cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s, %s, %s, %s)",
                                    (user_id, 'search', date, comment_text))
                        mysql.connection.commit()
                        break  # Break once a negative word is found in the comment
            
            cur.execute("SELECT date, post_content FROM posts WHERE user_id = %s",(user_id,))
            comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
            with open('negative_words.txt', 'r') as file:
                negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
            for date, comment_text in comments_data:
                for word in negative_words:
                    if word in comment_text:
                        # Save detected comments to the 'menaces' table
                        cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s, %s, %s, %s)",
                                    (user_id,'post', date, comment_text))
                        mysql.connection.commit()
                        break 
    check_comments_for_menaces() # Break once a negative word is found in the comment
    return render_template('pourcentage.html',similarity_percentage=percentage) 

@app.route('/pourcentage1')
def pourcentage1():
    file_path_facebook = 'twitter.txt'
    file_path_ideal = 'Ideal1.txt'

    # Read the contents of the files
    facebook_content = read_file(file_path_facebook)
    ideal_content = read_file(file_path_ideal)

    # Calculate the similarity percentage
    percentage = calculate_similarity_percentage(facebook_content, ideal_content)

    # Read the content of the password_strength file
    with open('password_strength.txt', 'r') as file:
        password_strength_content = file.read()

    # Update the percentage based on the content of password_strength
    if 'Weak' in password_strength_content:
        percentage += 3
    elif 'Medium' in password_strength_content:
        percentage += 5
    elif 'Strong' in password_strength_content:
        percentage += 10
    cur=mysql.connection.cursor()
    email = session['user']['email']
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cur.fetchone()[0]
    cur.execute("SELECT * FROM tweets WHERE user_id = %s",(user_id,))
    comments_data = cur.fetchall()

            # Load negative/hate speech terms from a text file
    with open('negative_words.txt', 'r') as file:
        negative_words = file.read().splitlines()

            # Iterate through comments to detect negative/hate speech
        for row in comments_data:
    # Access the columns by their index positions
            date = row[4]  # Assuming date is the first column
            comment_text = row[5]
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (user_id, table_name, date, comment) VALUES (%s,%s, %s, %s)",
                                    (user_id,'tweet', date, comment_text))
                    mysql.connection.commit()

    return render_template('pourcentage1.html',similarity_percentage=percentage) 

if __name__ == '__main__':
    app.run(debug=True)
