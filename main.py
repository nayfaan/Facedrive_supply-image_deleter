import services.startDriver
from services.startDriver import *
import csv
import time

def initiate_driver(driver, url):
    driver.get(url)
    
def login(driver,username,password):
    WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#user_login")))
    
    username_field = driver.find_element_by_css_selector("#user_login")
    username_field.clear()
    username_field.send_keys(username)
    
    WebDriverWait(driver, timeout=10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#user_pass")))
    
    password_field = driver.find_element_by_css_selector("#user_pass")
    password_field.clear()
    password_field.send_keys(password)
    time.sleep(0.3)
    password_field.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, timeout=60).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#wpcontent")))
    
def run():    
    driver = services.startDriver.start()
    initiate_driver(driver, "https://facedrivesupply.com/wp-admin/edit.php?post_type=product")
    
    '''with open('./input/credentials.txt','r') as f:
        credentials = f.read().splitlines()
    
    
    login(driver,credentials[0],credentials[1])
    
    try:
        scrap(driver,ids)
    except:
        pass
    finally:
        driver.close()'''

if __name__ == "__main__":
    run()
