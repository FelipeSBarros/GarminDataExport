from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()
driver.get('https://connect.garmin.com/')
print(driver.title)