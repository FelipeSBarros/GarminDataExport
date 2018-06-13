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
browser.find_element_by_class_name("export-btn").click()
# It is possible to send key "RETURN"...
browser.find_element_by_class_name("export-btn").send_keys(Keys.RETURN)

# now going to each activity
browser.find_elements_by_class_name("inline-edit-target")
browser.find_elements_by_partial_link_text('Corrida')
print( "Total Activities: " + str(len(activities)))
#browser.find_element_by_class_name("inline-edit-target").click()
inside = activities[0].click()
for a in range(0, len(activities)):
    if not activities[a]=='':
        print(activities[a].text)

activities[0].text
activities[0].text.isspace()

# About windows
#for handle in browser.window_handles:
#    print(handle)

#browser.switch_to_window('CDwindow-C2E16168D5EDEB2C227593B2AABC72DB')
#browser.save_screenshot('screenshot.png')