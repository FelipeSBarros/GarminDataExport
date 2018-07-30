from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Infos import GCuser, GCpass, databaseServer, databaseName, databaseUser, databasePW

class GarminConnect:
    def __init__(self, driver):
        self.driver = driver
        self.urlLogin = 'https://sso.garmin.com/sso/login?service=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&webhost=olaxpw-connect04&source=https%3A%2F%2Fconnect.garmin.com%2Fen-US%2Fsignin&redirectAfterAccountLoginUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&redirectAfterAccountCreationUrl=https%3A%2F%2Fconnect.garmin.com%2Fpost-auth%2Flogin&gauthHost=https%3A%2F%2Fsso.garmin.com%2Fsso&locale=en_US&id=gauth-widget&cssUrl=https%3A%2F%2Fstatic.garmincdn.com%2Fcom.garmin.connect%2Fui%2Fcss%2Fgauth-custom-v1.1-min.css&clientId=GarminConnect&rememberMeShown=true&rememberMeChecked=false&createAccountShown=true&openCreateAccount=false&usernameShown=false&displayNameShown=false&consumeServiceTicket=false&initialFocus=true&embedWidget=false&generateExtraServiceTicket=false'
        self.urlActivities = 'https://connect.garmin.com/modern/activities'

    def login(self, userName, passWord):
        self.driver.get(self.urlLogin)
        assert "GARMIN Authentication Application" in self.driver.title
        self.driver.find_element_by_id("username").send_keys(userName)
        self.driver.find_element_by_id("password").send_keys(passWord)
        self.driver.find_element_by_id("login-btn-signin").click()
        print("Logged in!")
        return self.driver

    def getActivities(self):
        self.driver.get(self.urlActivities)
        assert "Garmin Connect" in self.driver.title
        print("OK")
        #activities = self.driver.find_elements_by_class_name("inline-edit-target ")
        activities = self.driver.find_elements_by_id("activity-name-edit")
        validActivities = [i for i in activities if i.text] # if returning only valid activities
        print("Total Activities: " + str(len(validActivities )))
        return validActivities

    def getData(self, activities):
        keep = True
        a = 0
        while keep:
            if self.driver.current_url.split("/")[-1] == 'activities':
                print("In activities general page...")
                if not activities[a].text:
                    print("pass")
                    # pass
                else:
                    # Going to activitie page
                    print("Going to {} activitie page".format(activities[a].text))
                    activities[a].click()

            # In activitie page, find the gear icon
            gear = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "icon-gear"))).click()
            # TODO seguir o script.
            keep = False

            """gear = browser.find_element_by_class_name("icon-gear")
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
            if nxtid in saved_ids:  # test if the current activitie is already saved or not.
                # If it is already saved, change keep to False, to stop *while* loop
                keep = False
                sleep(1)
                print("End of NEW activities download")
""""

#ff = webdriver.Firefox()
chrome = webdriver.Chrome()
GC = GarminConnect(chrome)
f = GC.login(userName = GCuser, passWord = GCpass)
acti = GC.getActivities()
GC.getData(acti)