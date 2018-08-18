# Garmin Connect data export
**About this project:** The main idea of this project is to not only extract all activities data from Garmin Connect for those who use its system, but also to organize both GPX and CSV data on a **PostGIS** database. 

:warning: **Obviously, this project has no relation to Garmin and its use should be tke care of its rigth**.

## Python 3 module used in this project
:heavy_check_mark: [Selenium](https://selenium-python.readthedocs.io/)  
:heavy_check_mark: [osgeo](http://gdal.org/python/)  
:heavy_check_mark: [SQLAlchemy](http://www.sqlalchemy.org/)  
:heavy_check_mark: [GeoSQLAlchemy](https://geoalchemy-2.readthedocs.io/en/latest/)  
:heavy_check_mark: [psycopg2](http://initd.org/psycopg/docs/)  
:heavy_check_mark: [pyvirtualdisplay](http://pyvirtualdisplay.readthedocs.io/en/latest/)  
:heavy_check_mark: [pandas](https://readthedocs.org/projects/pandas/)  
:heavy_check_mark: [geopandas](http://geopandas.org/index.html)  

## Setup:
If you are not interested on organizing your data on PostGIS, ou can skip the database installation and use only function related on [extracting data](#3-extracting-data) but don't skip [info.py](#2-setting-up-infopy-file).  
More info about [spatial database](https://postgis.net/).

### 1) Setup PostgreSQL/GIS

**Make sure you have defined above elements on [Infos.py](#2-setting-up-infopy-file):**

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
### 2) Setting up Info.py file
Make sure you have all aditional information necessary to run the code on **Info.py** file, like shown below:
```buildoutcfg
GCuser="YOUR_USER_NAME" # Garmin Connect User Name
GCpass="YOUR_PASSWORD" # Garmin Connect Password
databaseServer = "database_host" # Database Serve adress
databaseName = "dbName" # Database Name
databaseUser = "usrName" # Database User Name
databasePW = "usrPassWord" # Database Password
```

### 3) Extracting data
On **[UsingGC.py](https://github.com/FelipeSBarros/GarminDataExport/blob/refactorFunction/UsingGC.py)** you have the codes to:

#### 3.1) Extract your data from Garmin Connect
A few functions were created uding selenium module.
 They are imported bu
```
from GCExtract import GarminConnect as GC
```
And they are:  

- **GC.login(userName, passWord)** which will login to the website and return the webdriver logged in;  
- **GC.getActivities(saved_ids)** which will navigate thru the activities downloading partials **CSV** and **GPX** files. The parameter *saved_ids* are the garmin activities ID already saved on the database which can be retrieved using the function *[get_garmin_id](https://github.com/FelipeSBarros/GarminDataExport/blob/refactorFunction/dbSetup.py#L203)* from *[dbSetup.py](#32-creating-database-tables)*

#### 3.2) Create database tables
By importing the **[dbSetup.py](https://github.com/FelipeSBarros/GarminDataExport/blob/refactorFunction/dbSetup.py)** all tables will be created to host your data after extracting it from the Garmin Connect Web Site.
Also we will retriece the *con* and *meta* objects to work with SQLAlchemy and the *get_garmin_id* function.
```dbSetup
from dbSetup import con, meta, get_garmin_id
```
:warning: According to GEOSQLAlchemy [documentation](https://geoalchemy-2.readthedocs.io/en/0.2.6/types.html) the spatial index are created by default. 

### 3) Importing data
Two functions were designed to import the data retrieve from Garmin Connect to the database>

- gpx2pg(con, meta, inFolder, inFormat)
- csv2pg(con, meta, inFolder, inFormat)  

Where: 

* *con* is the SQLAlchemy engine;
* *meta* is the SQLAlchemy metadata;
* *inFolder* the path to folder where the files are saved;
* *inFormat* is the file extention:
   * 'gpx': when usin gpx2pg;
   * 'csv': when using csv2pg;

**Example:**
```
inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities2'
inFormat = "gpx"

gpx2pg(con, meta, inFolder, inFormat)
```
  
## Important consideration about installation  
* [Installing and config Chrome for Selenium](https://christopher.su/2015/selenium-chromedriver-ubuntu/)  
* :warning: **[Consider Chrome Driver latest version](https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip)**  

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
  * [Bulk insertion](https://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy)

## *Garmin Connect* links

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