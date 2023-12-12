from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'pass_root'
app.config['MYSQL_DB'] = 'projet'
app.config['MYSQL_PORT'] = 3307 

mysql = MySQL(app)

# Define a function to check comments for negative/hate speech
def check_comments_for_menaces():
    # Establish a database connection within the application context
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT date, comment FROM comments")
        comments_data = cur.fetchall()

        # Load negative/hate speech terms from a text file
        with open('negative_words.txt', 'r') as file:
            negative_words = file.read().splitlines()

        # Iterate through comments to detect negative/hate speech
        for date, comment_text in comments_data:
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (table_name, date, comment) VALUES (%s, %s, %s)",
                                ('comments', date, comment_text))
                    mysql.connection.commit()
                    break  # Break once a negative word is found in the comment
        
        cur.execute("SELECT date, like_action FROM likes")
        comments_data = cur.fetchall()

        # Load negative/hate speech terms from a text file
        with open('negative_words.txt', 'r') as file:
            negative_words = file.read().splitlines()

        # Iterate through comments to detect negative/hate speech
        for date, comment_text in comments_data:
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (table_name, date, comment) VALUES (%s, %s, %s)",
                                ('likes', date, comment_text))
                    mysql.connection.commit()
                    break  # Break once a negative word is found in the comment
        
        cur.execute("SELECT date, tag_content FROM tags")
        comments_data = cur.fetchall()

        # Load negative/hate speech terms from a text file
        with open('negative_words.txt', 'r') as file:
            negative_words = file.read().splitlines()

        # Iterate through comments to detect negative/hate speech
        for date, comment_text in comments_data:
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (table_name, date, comment) VALUES (%s, %s, %s)",
                                ('tag', date, comment_text))
                    mysql.connection.commit()
                    break  # Break once a negative word is found in the comment
        
        cur.execute("SELECT date, search FROM searches")
        comments_data = cur.fetchall()

        # Load negative/hate speech terms from a text file
        with open('negative_words.txt', 'r') as file:
            negative_words = file.read().splitlines()

        # Iterate through comments to detect negative/hate speech
        for date, comment_text in comments_data:
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (table_name, date, comment) VALUES (%s, %s, %s)",
                                ('search', date, comment_text))
                    mysql.connection.commit()
                    break  # Break once a negative word is found in the comment
        
        cur.execute("SELECT date, post_content FROM posts")
        comments_data = cur.fetchall()

        # Load negative/hate speech terms from a text file
        with open('negative_words.txt', 'r') as file:
            negative_words = file.read().splitlines()

        # Iterate through comments to detect negative/hate speech
        for date, comment_text in comments_data:
            for word in negative_words:
                if word in comment_text:
                    # Save detected comments to the 'menaces' table
                    cur.execute("INSERT INTO menaces (table_name, date, comment) VALUES (%s, %s, %s)",
                                ('post', date, comment_text))
                    mysql.connection.commit()
                    break  # Break once a negative word is found in the comment

# Now, you can call this function within a route or another part of your Flask application
@app.route('/process_comments')
def process_comments():
    check_comments_for_menaces()
    return 'Comments checked for negative/hate speech'

def extract_unique_ips():
    with app.app_context():
        cur = mysql.connection.cursor()

        # Fetch distinct combinations of date and login from the logins table
        cur.execute("SELECT DISTINCT date, login_action FROM logins")
        unique_logins = cur.fetchall()

        # Insert unique combinations into the ip_address table
        for login_info in unique_logins:
            date, login = login_info
            cur.execute("INSERT INTO ip_address (date, login) VALUES (%s, %s)", (date, login))
            mysql.connection.commit()



if __name__ == '__main__':
    app.run(debug=True)
