# Test project Garmin Data Export

First installing and configuring Chrome to user on selenium
```
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()
driver.get('http://christopher.su')
print driver.title
```


# Useful links:
* [Installing and config Chrome for Selenium](https://christopher.su/2015/selenium-chromedriver-ubuntu/)  
*