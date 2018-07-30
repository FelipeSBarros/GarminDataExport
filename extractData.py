from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from Infos import GCuser, GCpass, databaseServer, databaseName, databaseUser, databasePW
import os
import sqlalchemy # To work with PostgreSQL
import geoalchemy2 # To work with PostgIS

loginPage = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
activitiesPage = 'https://connect.garmin.com/modern/activities'

def logIn(loginPage, GCuser, GCpass):
    # creating display
    display = Display(visible = 0, size = (1080, 1920))
    display.start()

    # Defining the download folder
    Activitywd = "Activities"
    # Creating folder if not exists
    if not os.path.exists(Activitywd):
        os.makedirs(Activitywd)

    # starting the driver
    #from selenium.webdriver.chrome.options import Options
    #chrome_options = Options()
    #chrome_options.add_experimental_option("prefs",{
    #    "download.default_directory": "/media/felipe/DATA/Repos/GarminProj"})
    #browser = webdriver.Chrome(chrome_options=chrome_options)
    browser = webdriver.Chrome()

    # Getting login page with the driver
    browser.get(loginPage)

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
    print("Logged in!")
    return browser

def get_garmin_id(con):
    """Get from database the activities ids already saved"""

    result = con.execute("select * from garmin_ids")
    return [x[0] for x in result]

def getActivities(browser, activitiesPage, saved_ids):
    """Find activities and browser in its page to get CSV and GPX, when it is the case"""

    # Once logged in, lets go to activities page
    browser.get(activitiesPage)
    assert "Garmin Connect" in browser.title

    # Getting activities twice to clean some fake activities (without link)
    activities = browser.find_elements_by_class_name("inline-edit-target ")
    act = browser.find_elements_by_class_name("inline-edit-target ")


    # Removing *wrong* activities and getting ID from right activities
    ids = []

    for a in act:
        if not a.text:
            activities.remove(a)
        elif a.get_attribute("href") is None:
            activities.remove(a)
        else:
            ids.append(a.get_attribute('href').split("/")[-1])

    print( "Total Activities: " + str(len(activities)))

    keep = True
    a=0
    while keep:
        if browser.current_url.split("/")[-1] == 'activities':
            print("In activities general page...")
            if not activities[a].text:
                print("pass")
                #pass
            else:
                # Going to activitie page
                print("Going to {} activitie page".format(activities[a].text))
                activities[a].click()
                sleep(5)

        # In activitie page, find the gear icon
        sleep(2)
        gear = browser.find_element_by_class_name("icon-gear")
        sleep(2)
        gear.click()
        sleep(2)
        print("Getting CSV")
        # Find CSV file and download
        csv = browser.find_element_by_id("btn-export-csv")
        sleep(2)
        csv.click()
        print("Is there a map?")
        sleep(2)
        # Find if there is a spatial infomation (map)
        map = browser.find_element_by_id("activityMapViewPlaceholder")
        sleep(2)
        if map.text:
            # If there is a map, doanload GPX file
            print("Getting Map...")
            gear = browser.find_element_by_class_name("icon-gear")
            sleep(2)
            gear.click()
            sleep(2)
            gpx = browser.find_element_by_id("btn-export-gpx")
            sleep(2)
            gpx.click()
            sleep(2)

        # Once done, use next icon co go to next activitie
        print("Going to next activitie...")
        browser.find_element_by_class_name("page-previous").click()
        sleep(2)
        nxtid = browser.current_url.split("/")[-1]
        sleep(2)
        if nxtid in saved_ids: #test if the current activitie is already saved or not.
            # If it is already saved, change keep to False, to stop *while* loop
            keep = False
            sleep(1)
            print("End of NEW activities download")

def connect(databaseUser, databasePW, databaseName, databaseServer, port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(databaseUser, databasePW, databaseServer, port, databaseName)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta


# Testing
con, meta = connect(databaseUser, databasePW, databaseName, databaseServer, port = 5432)

saved_ids = get_garmin_id(con)
browser = logIn(loginPage, GCuser, GCpass)
getActivities(browser, activitiesPage, saved_ids)
