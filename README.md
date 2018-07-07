# Garmin data export
**About this project:** The main idea of this project is to not only extract all activities data from Garmin Connect for those who use its system, but also to organize both GPX and CSV data on a **PostGIS** database. 

:warning: **Obviously, this project has no relation to Garmin and its use should be tke care of its rigth**.

## Python 3 module used in this project
:heavy_check_mark: [Selenium](https://selenium-python.readthedocs.io/)  
:heavy_check_mark: [osgeo](http://gdal.org/python/)  
:heavy_check_mark: [SQLAlchemy](http://www.sqlalchemy.org/)  
:heavy_check_mark: [psycopg2](http://initd.org/psycopg/docs/)  
:heavy_check_mark: [pyvirtualdisplay](http://pyvirtualdisplay.readthedocs.io/en/latest/)  
  
#### Important consideration about installation  
* [Installing and config Chrome for Selenium](https://christopher.su/2015/selenium-chromedriver-ubuntu/)  
* [**Consider Chrome Driver latest version**](https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip)

### About codes:
* [infos.py](): Set of important parameters and informations that will be necessary:
    * GCuser = "GarminUserName"
    * GCpass="GarminPassWord"
    * databaseServer = "localhost"
    * databaseName = "DBName"
    * databaseUser = "DBUser"
    * databasePW = "DBPassWord"
* [s]()

## Useful links:
* https://www.guru99.com/selenium-python.html  
* http://www.thetaranights.com/login-to-a-website-using-selenium-python-python-selenium-example/  
* https://selenium-python.readthedocs.io/  
* http://www.sqlalchemy.org/library.html#tutorials
* https://suhas.org/sqlalchemy-tutorial/
* http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html  
* http://docs.sqlalchemy.org/en/rel_1_0/index.html  
* http://initd.org/psycopg/docs/
* https://wiki.postgresql.org/wiki/Psycopg2_Tutorial  
* http://gdal.org/functions_c.html#index_c

## Data base creation:
```
postgres=# CREATE DATABASE tennis;
CREATE DATABASE
postgres=# CREATE USER federer WITH PASSWORD 'grandestslam';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE tennis TO federer;
GRANT
```