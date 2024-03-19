from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "http://localhost:8000/accounts/login/"

username = "olive"
password = "Azertylilivier59!"

username_path = '//*[@id="id_username"]'
password_path = '//*[@id="id_password"]'
login_btn_path = '//input[@type="submit" and @value="Login"]'
dashboard_btn_path = '//*[@id="dashboard"]/a'
select_all_path = '//*[@id="select-all-div"]/input'
delete_btn_path = '//button[@type="submit" and @class="delete-selected"]'

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)


# open page--------------------------------------------------------------------

browser.get(url)
browser.maximize_window()

# conection--------------------------------------------------------------------

username_field = WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, username_path))
)
username_field.clear()
username_field.send_keys(username)

password_field = browser.find_element(By.XPATH, password_path)
password_field.clear()
password_field.send_keys(password)

login_button = browser.find_element(By.XPATH, login_btn_path)
login_button.click()

# remove all crons-------------------------------------------------------------

dashboard_btn = WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, dashboard_btn_path))
)
dashboard_btn.click()

select_all = WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, select_all_path))
)
select_all.click()

delete_btn = browser.find_element(By.XPATH, delete_btn_path)
delete_btn.click()

alert = browser.switch_to.alert
alert.accept()
time.sleep(2)


# close------------------------------------------------------------------------

browser.quit()
