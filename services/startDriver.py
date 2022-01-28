from selenium import webdriver

def start():
    return webdriver.Chrome(executable_path='./services/chromedriver')

if __name__ == "__main__":
    pass
