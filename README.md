# Garmin Connect data export
**About this project:** The main idea of this project is to not only extract all activities data from Garmin Connect for those who use its system, but also to organize both GPX and CSV data on a **PostGIS** database. 

:warning: **Obviously, this project has no relation to Garmin and its use should be tke care of its rigth**.

## Setup:
If you are not interested on organizing your data on PostGIS, ou can skip the database installation and use only function related on [GCExport](#TODO insert link!).  
More info about [spatial database](https://postgis.net/).

#### PostgreSQL

**Make sure you have defined above elements on [Infos.py](#TODO inser link to title):**

* Database created with GIS extensions;
* User and password to refered database;
* Privileges to the database;

```dbSpecifications
# Data base creation:
sudo su postgres
psql
CREATE DATABASE dbName; # creates database
\q # exit
psql dbName # go to recently created data base

# create GIS extensions
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology; 
# create user and password
CREATE USER usrName WITH PASSWORD 'usrPassWord'; 
# give privileges to new user
GRANT ALL PRIVILEGES ON DATABASE dbName TO usrName; 
\q # exit database
exit # exit as superuser postgres
```
**Info.py** exemple
```buildoutcfg
GCuser="YOUR_USER_NAME"
GCpass="YOUR_PASSWORD"
databaseServer = "database_host"
databaseName = "dbName"
databaseUser = "usrName"
databasePW = "usrPassWord"
```
Then, run [setup.py](#TODO create this setup.py which will create all tables IF not exists)
```
from sqlalchemy_views import CreateView, DropView
from sqlalchemy.sql import text
from sqlalchemy import Table

con, meta = connect(databaseUser, databasePW, databaseName, databaseServer, port = 5432)

view = Table('garmin_ids', meta)
definition = text("SELECT distinct(\"idGarmin\") FROM summary")

create_view = CreateView(view, definition, or_replace=True)
print(create_view)
```
## Python 3 module used in this project
:heavy_check_mark: [Selenium](https://selenium-python.readthedocs.io/)  
:heavy_check_mark: [osgeo](http://gdal.org/python/)  
:heavy_check_mark: [SQLAlchemy](http://www.sqlalchemy.org/)  
:heavy_check_mark: [GeoSQLAlchemy](https://geoalchemy-2.readthedocs.io/en/latest/)  
:heavy_check_mark: [psycopg2](http://initd.org/psycopg/docs/)  
:heavy_check_mark: [pyvirtualdisplay](http://pyvirtualdisplay.readthedocs.io/en/latest/)  
:heavy_check_mark: [pandas](https://readthedocs.org/projects/pandas/)  
:heavy_check_mark: [geopandas](http://geopandas.org/index.html)  
  
#### Important consideration about installation  
* [Installing and config Chrome for Selenium](https://christopher.su/2015/selenium-chromedriver-ubuntu/)  
* **[Consider Chrome Driver latest version](https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip)**  
* **sqlalchemy_views**  

### About codes:
   
* [infos.py](#TODO insert link): Set of important parameters and informations that will be necessary, as mentioned before;
* [others.py](#TODO insert all codes) 

## Useful links:
* Selenium  
  * https://www.guru99.com/selenium-python.html  
  * http://www.thetaranights.com/login-to-a-website-using-selenium-python-python-selenium-example/  
  * https://selenium-python.readthedocs.io/
* SQLAlchemy  
  * http://www.sqlalchemy.org/library.html#tutorials
  * https://suhas.org/sqlalchemy-tutorial/
  * http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html  
* psycopg2
  * http://initd.org/psycopg/docs/
  * https://wiki.postgresql.org/wiki/Psycopg2_Tutorial  
* Gdal  
  * http://gdal.org/functions_c.html#index_c  
* General 
  * https://ocefpaf.github.io/python4oceanographers/  



### *Garmin Connect* links

[url_gc_login](https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false)  
[url_gc_post_auth](https://connect.garmin.com/post-auth/login?)  
[url_gc_search](http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?)  
[url_gc_gpx_activity](http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/)  
[url_gc_tcx_activity](http://connect.garmin.com/proxy/activity-service-1.1/tcx/activity/)  
[url_gc_original_activity](http://connect.garmin.com/proxy/download-service/files/activity/)  

#### New endpoints
[url_gc_tcx_activity](https://connect.garmin.com/modern/proxy/download-service/export/tcx/activity/)  
[url_gc_gpx_activity](https://connect.garmin.com/modern/proxy/download-service/export/gpx/activity/)  
[por JSON](https://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?)