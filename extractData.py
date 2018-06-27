from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from Infos import GCuser, GCpass
import os
import psycopg2 # To work with PostGIS
from selenium.webdriver.common.keys import Keys # to send keys on navigation. Not used so far.

# creating display
display = Display(visible=0, size=(1080, 1920))
display.start()

# Configuring web driver
#options = webdriver.ChromeOptions()
# Defining the download folder
Activitywd = "Activities"
# Creating folder if not exists
if not os.path.exists(Activitywd):
    os.makedirs(Activitywd)
# Altering doanload options to desired folder
#options.add_argument("download.default_directory="+Activitywd)
# starting the driver
browser = webdriver.Chrome()

# Getting login page with the driver
browser.get('https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false')

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
assert "Garmin Connect" in browser.title

# now going to each activity
#browser.save_screenshot("screen1.png")

#from selenium.webdriver.common.action_chains import ActionChains
#body = browser.find_element_by_xpath('/html/body')
#body.click() # rodei varias vezes ate chegar no maximo de activities
#ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()# rodei varias vezes ate chegar no maximo de activities
#browser.save_screenshot("screen2.png")

# Getting activities twice to clean some fake activities (without link)
activities = browser.find_elements_by_class_name("inline-edit-target ")
act = browser.find_elements_by_class_name("inline-edit-target ")
#len(activities)

# Removing wrong activities and getting ID from rihgt activities
ids = []
remove_id = []

#len(act)
#len(activities)
for a in act:
    if not a.text:
        activities.remove(a)
    elif a.get_attribute("href") is None:
        activities.remove(a)
    else:
        ids.append(a.get_attribute('href').split("/")[-1])

#len(ids)
#len(activities)
#len(act)
print( "Total Activities: " + str(len(activities)))

#Connection configuration to PostgreSQL/GIS database
try:
    conn = psycopg2.connect("dbname='GarminTest' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database.")

cur.execute("CREATE TABLE IF NOT EXISTS activitiesid (id serial PRIMARY KEY, garmin_id text);")

# Inserting IDs to the data base
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
    try:
        conn = psycopg2.connect("dbname='GarminTest' user='postgres' host='localhost' password='postgres'")
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database.")
    stmt = "SELECT garmin_id FROM activitiesid"
    cur.execute(stmt)
    return [x[0] for x in cur.fetchall()]

saved_ids = get_garmin_id()
saved_ids = []

keep = True
#for a in range(0, len(activities)):
a=0
while keep:
    if browser.current_url.split("/")[-1] == 'activities':
        if not activities[a].text:
            print("pass")
            #pass
        else:
            print(activities[a].text)
            # Doing this we go to activitie page
            #try:
            activities[a].click()
            sleep(5)

    gear = browser.find_element_by_class_name("icon-gear")
    sleep(2)
    gear.click()
    sleep(2)
    #browser.save_screenshot('screenshot.png')
    print("Getting CSV")
    csv = browser.find_element_by_id("btn-export-csv")
    sleep(2)
    csv.text
    csv.click()
    print("Is there a map?")
    sleep(2)
    map = browser.find_element_by_id("activityMapViewPlaceholder")
    sleep(2)
    map.text
    # map.click()
    if map.text:
        gear = browser.find_element_by_class_name("icon-gear")
        sleep(2)
        gear.click()
        sleep(2)
        gpx = browser.find_element_by_id("btn-export-gpx")
        sleep(2)
        gpx.text
        gpx.click()
        sleep(2)

    print("Going to next")
    browser.find_element_by_class_name("page-previous").click()
    sleep(2)
    nxtid = browser.current_url.split("/")[-1]
    sleep(2)
    if nxtid in saved_ids:
        keep = False
        sleep(1)
        #except:
        #print("Não DEU")




            #browser.save_screenshot('screenshot.png')
            gpx = browser.find_element_by_id("btn-export-gpx")
            sleep(5)
            #gpx.text
            gpx.click()
            sleep(5)
            browser.back()
            sleep(5)
        except:
            print("Não DEU")
        finally:
            print("FIM")

"""
for a in range(0, len(activities)):
    #while keep:
        if not activities[a].text:
            print("pass")
            #pass
        else:
            print(a)
            print(activities[a].text)
            # Doing this we go to activitie page
            #try:
            activities[a].click()
            sleep(5)
            gear = browser.find_element_by_class_name("icon-gear")
            sleep(5)
            gear.click()
            sleep(5)
            #browser.save_screenshot('screenshot.png')
            print("Getting CSV")
            csv = browser.find_element_by_id("btn-export-csv")
            sleep(5)
            csv.text
            csv.click()
            print("Is there a map?")
            sleep(5)

def findMap():
    map = browser.find_element_by_id("activityMapViewPlaceholder")
    sleep(5)
    map.text
    if map.text:
        getGPX()

def getGPX():
    gear = browser.find_element_by_class_name("icon-gear")
    sleep(5)
    gear.click()
    sleep(5)
    gpx = browser.find_element_by_id("btn-export-gpx")
    sleep(5)
    gpx.text
    gpx.click()
    sleep(5)

def goNext(saved_ids):
    print("Going to next")
    browser.find_element_by_class_name("page-previous").click()
    sleep(5)
    nxtid = browser.current_url.split("/")[-1]
    if nxtid in saved_ids:
        break
"""

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

# Few importante links
"""
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
"""

# Now we are in the activity page, lets donwload the summary:
# Lets find the "export button" and click on it
#browser.find_element_by_class_name("export-btn").click()
# It is possible to send key "RETURN"...
#browser.find_element_by_class_name("export-btn").send_keys(Keys.RETURN)

#browser.find_elements_by_xpath('//a[@href="'+variable+'"]');
#browser.find_elements_by_partial_link_text('Corrida')
# https://stackoverflow.com/questions/11328940/check-if-list-item-contains-items-from-another-list#11329522