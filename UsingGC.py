from Infos import GCuser, GCpass, databaseServer, databaseName, databaseUser, databasePW
from GCExtract import GarminConnect as GC
from selenium import webdriver
from pyvirtualdisplay import Display
GC.login()
GarminConnect.login()
# creating display

display = Display(visible = 0, size = (1080, 1920))
display.start()
chrome = webdriver.Chrome()
GC = GC(chrome)
GC.login(userName = GCuser, passWord = GCpass)
saved_ids = [2888120512]
GC.getActivities(saved_ids)