from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

username = ""
password = ""
url = "https://www.facebook.com/login.php/"

# Use EdgeChromiumDriverManager to automatically download the Edge WebDriver
edge_path = EdgeChromiumDriverManager().install()

# Use the Edge WebDriver path in the webdriver.Edge method
driver = webdriver.Edge(edge_path)
driver.get(url)