from pyvirtualdisplay import Display
from selenium import webdriver
from Infos import GCuser, GCpass
from selenium.webdriver.common.keys import Keys

display = Display(visible=0, size=(1080, 1920))
display.start()

browser = webdriver.Chrome()
#driver.get('https://connect.garmin.com/')
#browser.get('https://connect.garmin.com/en-US/signin')
#browser.get('http://garmin.com/es-AR/signin')
browser.get('https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false')
print(browser.title)
assert "GARMIN Authentication Application" in browser.title # "Asserts" keyword is used to verify the conditions. In this line, we are confirming whether the title is correct or not. For that, we will compare the title with the string which is given.
username = browser.find_element_by_id("username")
#username = browser.find_element_by_xpath("//input[@id='username']")
#username = browser.find_element_by_class_name("login_email")
password = browser.find_element_by_id("password")

username.send_keys(GCuser)
password.send_keys(GCpass)

browser.find_element_by_id("login-btn-signin").click()


#browser.get('http://connect.garmin.com/proxy/download-service/files/activity/')
browser.get('https://connect.garmin.com/modern/activities')

browser.find_elements_by_class_name("filter-container")
browser.find_elements_by_class_name("manual-activity-btn")
browser.find_elements_by_class_name("export-btn")
exprt=browser.find_elements_by_class_name("export-btn")

#exprt[0].send_keys(Keys.TAB) # tab over to not-visible element
#exprt[0].send_keys(Keys.TAB) # tab over to not-visible element
exprt[0].send_keys(Keys.RETURN)
exprt[0].click()

for handle in browser.window_handles:
    print(handle)

browser.switch_to_window('CDwindow-C2E16168D5EDEB2C227593B2AABC72DB')
browser.save_screenshot('screenshot.png')



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