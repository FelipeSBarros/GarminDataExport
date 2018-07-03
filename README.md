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

# SQL
```
pip install psycopg2 sqlalchemy
```

# Useful links:
* [Installing and config Chrome for Selenium](https://christopher.su/2015/selenium-chromedriver-ubuntu/)  
[**Consider Chrome Driver latest version**](https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip)
* https://www.guru99.com/selenium-python.html  
* http://www.thetaranights.com/login-to-a-website-using-selenium-python-python-selenium-example/  
* https://selenium-python.readthedocs.io/  
* http://www.sqlalchemy.org/library.html#tutorials  
* http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html  
* http://docs.sqlalchemy.org/en/rel_1_0/index.html  
* http://initd.org/psycopg/docs/
* https://wiki.postgresql.org/wiki/Psycopg2_Tutorial  




# Installing Chrome Drive:
