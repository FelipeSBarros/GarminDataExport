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
        """Function to login to Garmin Connect page"""
        self.driver.get(self.urlLogin)
        assert "GARMIN Authentication Application" in self.driver.title
        self.driver.find_element_by_id("username").send_keys(userName)
        self.driver.find_element_by_id("password").send_keys(passWord)
        self.driver.find_element_by_id("login-btn-signin").click()
        print("Logged in!")
        return self.driver

    def getActivities(self, saved_ids):
        """Function to navigate on activities page and download data"""
        self.driver.get(self.urlActivities)
        assert "Garmin Connect" in self.driver.title
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "activity-name-edit")))
        activities = self.driver.find_elements_by_id("activity-name-edit")
        validActivities = [i for i in activities if i.text] # if returning only valid activities
        print("Total Activities: " + str(len(validActivities )))
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

            # wait until load page
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "page-previous")))
            self.driver.implicitly_wait(3)
            # In activitie page, find the gear icon
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "icon-gear"))).click()

            # Find CSV file and download
            print("Getting CSV")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "btn-export-csv"))).click()
            # Find if there is a spatial infomation (map)
            if WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "activityMapViewPlaceholder"))):
                # If there is a map, download GPX file
                print("Getting Map...")
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "icon-gear"))).click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "btn-export-gpx"))).click()
            else:
                print("NO GPX FILE")
                self.driver.implicitly_wait(3)  # seconds

            # Once done, use next icon co go to next activitie
            print("Going to next activitie...")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "page-previous"))).click()
            nxtid = self.driver.current_url.split("/")[-1]
            # test if the current activitie is already saved or not.
            if int(nxtid) in saved_ids:
                # If it is already saved, change keep to False, to stop *while* loop
                keep = False
                print("End of NEW activities download")
                self.driver.close()
