from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome()
#driver.get('https://connect.garmin.com/')
browser.get('https://connect.garmin.com/en-US/signin')

print(driver.title)
#assert "Facebook" in driver.title # "Asserts" keyword is used to verify the conditions. In this line, we are confirming whether the title is correct or not. For that, we will compare the title with the string which is given.
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")

username.send_keys("YourUsername")
password.send_keys("Pa55worD")

selenium.find_element_by_name("submit").click()
login_attempt = browser.find_element_by_xpath("//*[@type='submit']") #http://www.thetaranights.com/login-to-a-website-using-selenium-python-python-selenium-example/
login_attempt.submit()