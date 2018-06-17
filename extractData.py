from pyvirtualdisplay import Display
from selenium import webdriver
from Infos import GCuser, GCpass
import os
import psycopg2 # To work with PostGIS

# from selenium.webdriver.common.keys import Keys # to send keys on navigation. Not used so far.

# Few importante links
url_gc_login = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
url_gc_post_auth = 'https://connect.garmin.com/post-auth/login?'
url_gc_search = 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?'
#url_gc_gpx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/'
#url_gc_tcx_activity = 'http://connect.garmin.com/proxy/activity-service-1.1/tcx/activity/'
url_gc_original_activity = 'http://connect.garmin.com/proxy/download-service/files/activity/'

## New endpoints
url_gc_tcx_activity = 'https://connect.garmin.com/modern/proxy/download-service/export/tcx/activity/'
url_gc_gpx_activity = 'https://connect.garmin.com/modern/proxy/download-service/export/gpx/activity/'
# https://connect.garmin.com/proxy/activity-search-service-1.0/json/activities? # por JSON

# creating display
display = Display(visible=0, size=(1080, 1920))
display.start()

# Configuring web driver
options = webdriver.ChromeOptions()
# Defining the download folder
Activitywd = "Activities"
# Creating folder if not exists
if not os.path.exists(Activitywd):
    os.makedirs(Activitywd)
# Altering doanload options to desired folder
options.add_argument("download.default_directory="+Activitywd)
# starting the driver
browser = webdriver.Chrome(chrome_options=options)

# Getting login page with the driver
browser.get('https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false')
#print(browser.title)
# "Asserts" keyword is used to verify the conditions. In this line, we are confirming whether the title is correct or not.
assert "GARMIN Authentication Application" in browser.title

# As we are in the login page, need to identify the usename and password element
username = browser.find_element_by_id("username")
password = browser.find_element_by_id("password")

# Once those were found, let fill them
username.send_keys(GCuser)
password.send_keys(GCpass)
# let's login
browser.find_element_by_id("login-btn-signin").click()

# Once logged in, lets go to activities page
browser.get('https://connect.garmin.com/modern/activities')
#print(browser.title)
assert "Garmin Connect" in browser.title

# Now we are in the activity page, lets donwload the summary:
# Lets find the "export button" and click on it
#browser.find_element_by_class_name("export-btn").click()
# It is possible to send key "RETURN"...
#browser.find_element_by_class_name("export-btn").send_keys(Keys.RETURN)

# now going to each activity
activities = browser.find_elements_by_class_name("inline-edit-target ")
#browser.find_elements_by_xpath('//a[@href="'+variable+'"]');
#browser.find_elements_by_partial_link_text('Corrida')

# Removing wrong activities and getting ID from rihgt activities
ids = []
for a in activities:
    # a=activities[0]
    # a.text
    # a.get_attribute('href')
    if not a.text:
        activities.remove(a)
    else:
        ids.append(a.get_attribute('href').split("/")[-1])

print( "Total Activities: " + str(len(activities)))

#Connection configuration to PostgreSQL/GIS database
try:
    conn = psycopg2.connect("dbname='GarminTest' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database.")

cur.execute("CREATE TABLE activitiesid (id serial PRIMARY KEY, garmin_id text);")


for id in ids:
    # id = ids[1]
    cur.execute("INSERT INTO activitiesid (garmin_id) VALUES (%s)", [id])


conn.commit()
cur.close()
conn.close()
"""
class DBHelper:
    def __init__(self, dbname="gastos.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
"""


def get_garmin_id():
    stmt = "SELECT garmin_id FROM activitiesid"
    return [x[0] for x in cur.execute(stmt)]

cur.execute(stmt)
l=cur.fetchall()
l[0][0]
saved_ids = get_garmin_id()

from time import sleep
for a in range(0, len(activities)):
    if not activities[a].text:
        print("OK")
        #pass
    else:
        print(a)
        print(activities[a].text)
        # Doing this we go to activitie page
        activities[a].click()
        sleep(5)
        gear = browser.find_element_by_class_name("icon-gear")
        gear.click()
        sleep(5)
        browser.save_screenshot('screenshot.png')
        #gpx = browser.find_element_by_id("btn-export-gpx")
        #gpx.text
        #gpx.click()
        #sleep(20)
        browser.back()
        sleep(5)


activities[0].text
#activities[0].text.isspace()

browser.back()

# Doing this we go to activitie page
activities[27].click()
browser.save_screenshot('screenshot.png')

browser.current_url

gear = browser.find_element_by_class_name("icon-gear")
gear.click()
browser.save_screenshot('screenshot.png')

gpx = browser.find_element_by_id("btn-export-gpx")
gpx.text
gpx.click()


# Experiments

#tryng to get href
#activities[27].text
#act_id = activities[27].get_attribute('href')
#act_id = act_id.split("/")[len(act_id.split("/"))-1]
#import urllib.request
# Download the file from `url` and save it locally under `file_name`:
#down = 'https://connect.garmin.com/modern/proxy/download-service/export/gpx/activity/2662026807'
#urllib.request.urlretrieve(down, './2662026807.gpx')

# About windows
#for handle in browser.window_handles:
#    print(handle)

#browser.switch_to_window('CDwindow-C2E16168D5EDEB2C227593B2AABC72DB')
#browser.save_screenshot('screenshot.png')




# Connect to an existing database
conn = psycopg2.connect("dbname='GarminTest' user='postgres' host='localhost' password='postgres'")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("CREATE TABLE test2 (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test2 (num) VALUES (%s)",(102,))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test2;")
cur.fetchone()
cur.fetchall()

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()