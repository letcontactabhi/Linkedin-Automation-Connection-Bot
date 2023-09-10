from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import config

email = config.EMAIL
password = config.PASSWORD
url = config.URL
message = config.MESSAGE



# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# ----------------------------------
driver.get(url)

print('Signing to account ')
# First go to sign page 
sign_in = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div/p/a'))
)
sign_in.click()

# Wait for the email field to be present
email_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'username'))
)
email_field.send_keys(email)

# Wait for the password field to be present
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'password'))
)
password_field.send_keys(password)

# Submit the form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load after login
print('Wait for 1 minutes for manual CAPTCHA solving')
time.sleep(60)  # Wait for 1 minutes for manual CAPTCHA solving

# Continue with your automation...........................

# Define the base XPath for Connect buttons
connect_buttons_xpath = '(//button[contains(@aria-label,"Invite")])'

# Function to handle actions for each Connect button
def handle_connect_button(connect_button):
    print('Sending connection ')
    connect_button.click()

    add_note = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Add a note")]'))
    )
    add_note.click()

    custom_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@id="custom-message"]'))
    )
    custom_message.send_keys(message)

    send_now = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Send now")]'))
    )
    send_now.click()
    print('Connection has been sent successfully')
    time.sleep(5)  # Adjust as needed

# ........................... (previous code remains the same) ......................
# Loop through each Connect button and handle connection requests
while True:
    try:
        connect_buttons = driver.find_elements(By.XPATH, connect_buttons_xpath)

        if not connect_buttons:
            print("No Connect buttons found on this page. Scrolling down and trying to go to the next page...")
            
            # Scroll down the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(60)
            try:
                next_page_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
                if next_page_button.is_enabled():
                    next_page_button.click()
                    time.sleep(30)  # Wait for a minute before processing the next page
                    continue  # Skip the rest of the loop and start from the beginning
                else:
                    print("Next button is disabled. Exiting...")
                    break
            except Exception as e:
                print(f"Error while trying to go to the next page: {e}")
                break

        for connect_button in connect_buttons:
            try:
                handle_connect_button(connect_button)
            except Exception as e:
                print(f"Connect button: Not found {e}")
    except Exception as e:
        print(f"Error while processing Connect buttons: {e}")

# ... (rest of your code)

time.sleep(60)