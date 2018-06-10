from selenium import webdriver

from selenium.webdriver.common.keys import Keys

#chromedriver = 'C:\\chromedriver.exe'
drv = './chromedriver'
browser = webdriver.Chrome(executable_path=drv)
browser = webdriver.Firefox(executable_path='./geckodriver')
browser.get('http://www.example.com')

username = selenium.find_element_by_id("username")
password = selenium.find_element_by_id("password")

username.send_keys("YourUsername")
password.send_keys("Pa55worD")

selenium.find_element_by_name("submit").click()




options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options)