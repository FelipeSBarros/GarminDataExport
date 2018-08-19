from selenium import webdriver
from pyvirtualdisplay import Display
from GCExtract import GarminConnect as GC
from dbSetup import con, meta, get_garmin_id
from ImportActivities import gpx2pg, csv2pg
from Infos import GCuser, GCpass

# creating display
display = Display(visible = 0, size = (1080, 1920))
display.start()
chrome = webdriver.Chrome()
GC = GC(chrome)
GC.login(userName = GCuser, passWord = GCpass)
saved_ids = get_garmin_id(con)
GC.getActivities(saved_ids)

# importing Activities to Database
inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities2'
inFormat = "gpx"

gpx2pg(con, meta, inFolder, inFormat)

inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities'
inFormat = "csv"

csv2pg(con, meta, inFolder, inFormat)
