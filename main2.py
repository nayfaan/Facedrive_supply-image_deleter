import services.startDriver
import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

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

def clear_media_library(driver):
    remaining_image_count = driver.find_element_by_css_selector(".displaying-num")
    remaining_image_count = int(re.sub("[^0-9]", "", remaining_image_count.get_attribute('innerHTML')))
    
    while remaining_image_count > 0:
        select_all_box = driver.find_element_by_css_selector("#cb-select-all-1")
        
        if not select_all_box.is_selected():
            select_all_box.click()
            
        while not select_all_box.is_selected():
            pass
            
        bulk_action = Select(driver.find_element_by_css_selector('#bulk-action-selector-top'))
        bulk_action.select_by_value("delete")
        
        apply_btn = driver.find_element_by_css_selector("#doaction")
        apply_btn.click()
        
        alert_exist = False
        while not alert_exist:
            try:
                alert_box_obj = driver.switch_to.alert
                alert_exist = True
                alert_box_obj.accept()
            except:
                pass
        
        new_remaining_image_count = remaining_image_count
        global url
        error_list = ["400 Bad Request",
                      "you are not allowed to delete this item",
                      "Web server is returning an unknown error",
                      "A timeout occurred", "Error in deleting the attachment",
                      "This item has already been deleted"]
        
        while new_remaining_image_count == remaining_image_count:
            try:
                new_remaining_image_count = driver.find_element_by_css_selector(".displaying-num")
                new_remaining_image_count = int(re.sub("[^0-9]", "", remaining_image_count.get_attribute('innerHTML')))
            except:
                found_errors = []
                for item in error_list:
                    found_item = driver.find_elements(By.XPATH,"//*[contains(text(),'" + item + "')]")
                    if len(found_item) > 0:
                        found_errors.append(found_item)
                if len(found_errors) > 0:
                    new_remaining_image_count = 0

                    driver.get(url)
                    driver.execute_script("location.reload(true);")
        
def run():    
    driver = services.startDriver.start()
    global url
    url = "https://facedrivesupply.com/wp-admin/upload.php?mode=list&attachment-filter=trash"
    driver.get(url)
    
    with open('./input/credentials.txt','r') as f:
        credentials = f.read().splitlines()
    
    login(driver,credentials[0],credentials[1])
    
    try:
        clear_media_library(driver)
    except Exception as e:
        print(str(e))
    finally:
        driver.close()

if __name__ == "__main__":
    run()
