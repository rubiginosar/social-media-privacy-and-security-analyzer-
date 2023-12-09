from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
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
password = "user_password"
hashed_password = hash_password(password)

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
                session['user'] = {'email': email}
                return render_template('chose.html')  # Redirect to the dashboard after successful login
            else:
    # Invalid credentials
                return "Invalid email or password. Please try again or register."

    return render_template('registration.html')



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
            session['user'] = {'email': email}
            return render_template('chose.html')  # Redirect to login page after registration
    return render_template('register.html')

@app.route('/options')
def options():
    return render_template('options.html') 

@app.route('/Login')
def Login():
    return render_template('Login.html') 



@app.route('/chose')
def chose():
    return render_template('chose.html') 

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

@app.route('/analyze_facebook', methods=['POST'])
def analyze_facebook():
    #Your Inform
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

    try:
        #contact information
        time.sleep(5)
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

        # Save as JSON with comments as separate strings
        with open('comments.json', 'w', encoding='utf-8') as json_file:
            json.dump(comments_data, json_file, ensure_ascii=False, indent=4)

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

# Save as JSON with comments as separate strings
        with open('devices.json', 'w', encoding='utf-8') as json_file:
            json.dump(comments_data, json_file, ensure_ascii=False, indent=4)
        

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

        # Save as JSON with comments as separate strings
        with open('likes.json', 'w', encoding='utf-8') as json_file:
            json.dump(comments_data, json_file, ensure_ascii=False, indent=4)   
        
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

# Save as JSON with comments as separate strings
        with open('log_in.json', 'w', encoding='utf-8') as json_file:
            json.dump(comments_data, json_file, ensure_ascii=False, indent=4)




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

            # Save as JSON with comments as separate strings
            with open('posts.json', 'w', encoding='utf-8') as json_file:
                json.dump(comments_data, json_file, ensure_ascii=False, indent=4)

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

            # Save as JSON with comments as separate strings
            with open('tags.json', 'w', encoding='utf-8') as json_file:
                json.dump(comments_data, json_file, ensure_ascii=False, indent=4)
            driver.quit()
        print("Browser closed")
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    return ''
if __name__ == '__main__':
    app.run(debug=True)