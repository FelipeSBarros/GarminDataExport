from pyvirtualdisplay import Display
from selenium import webdriver
from Infos import GCuser, GCpass
from selenium.webdriver.common.keys import Keys

# Few importante links
url_gc_login     = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
url_gc_post_auth = 'https://connect.garmin.com/post-auth/login?'
url_gc_search    = 'http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?'
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
#options = webdriver.ChromeOptions()
#options.add_argument("download.default_directory=C:/Downloads")

#driver = webdriver.Chrome(chrome_options=options)

# starting the driver
browser = webdriver.Chrome()
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
activities = browser.find_elements_by_class_name("inline-edit-target")
#browser.find_elements_by_xpath('//a[@href="'+variable+'"]');
#browser.find_elements_by_partial_link_text('Corrida')
print( "Total Activities: " + str(len(activities)))

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