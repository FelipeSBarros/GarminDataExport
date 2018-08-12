from selenium import webdriver
from pyvirtualdisplay import Display
from GCExtract import GarminConnect as GC
from dbSetup import con, meta
from gpxImport import gpx2pg
from csv2pg import csv2pg

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

# importing files

inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities2'
inFormat = "gpx"

gpx2pg(con, meta, inFolder, inFormat)

inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities2'
inFormat = "csv"

csv2pg(con, meta, inFolder, inFormat)
