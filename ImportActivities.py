import os, glob
from geoalchemy2 import WKTElement # To conver geom to WKT
import pandas as pd
import geopandas as gpd
import fiona
from dbSetup import get_garmin_id, summary, partials, con, meta


def gpx2pg(con, meta, inFolder, inFormat):

    def create_wkt_element(geom):
        """"function Use GeoAlchemy's WKTElement to create a geom with SRID"""
        return WKTElement(geom.wkt, srid=4326)

    # Identify file with pattern (format) in path (folder)
    fileList = glob.glob(os.path.join(inFolder, "*.{0}".format(inFormat)))
    for i in fileList:
        # i = fileList [0]
        idGarmin = i.split("_")[-1]
        idGarmin = idGarmin.split(".")[0]
        # Test if activity already saved (idGarmin)
        if int(idGarmin) in get_garmin_id(con):
            print("Activity {} already saved!".format(idGarmin))
        else:
            # Identify Layers in file
            layers = fiona.listlayers(i)
            for l in layers:
                # l = layers[2]
                table = meta.tables[l] # getting spatial table related to layer
                try:
                    data = gpd.read_file(i, layer=l)
                    # Use GeoAlchemy's WKTElement to create a geom with SRID
                    data['geometry'] = data['geometry'].apply(create_wkt_element) # TODO insert WKTElement(geom.wkt, srid=4326) direct here instead of creating function?
                    data["idGarmin"] = idGarmin
                    # Converting to Dictionary to import several feature at once
                    dataDict = data.to_dict(orient='records')
                    # Executing insert statement
                    con.execute(table.insert(), dataDict)
                    print("Layer {} from {} SAVED!".format(l, idGarmin))
                except KeyError:
                    print("Layer {} from {} without feature...".format(l, idGarmin))
                #except:
                #    print("Other error ocurred")
            print("GPX import done!")

def csv2pg(con, meta, inFolder, inFormat):
    '''Import csv from folder to PGSQL'''

    # Creating file list
    fileList = glob.glob(os.path.join(inFolder, "*.{0}".format(inFormat)))
    print("processing {} CSV files".format(len(fileList)))
    for f in fileList:
        # f = fileList[0]
        data = pd.read_csv(f)
        data = data.replace(['--'], [None])
        id = f.split('_')[-1]
        id = id.split(".")[0]
        data["idGarmin"] = id
        # Test if activity already saved (idGarmin)
        if int(id) in get_garmin_id(con):
            print("Activity {} already saved!".format(id))
        else:
            summaryData = data[-1:]
            data = data.drop(data[-1:].index)

            # Converting to dictionary
            data = data.to_dict(orient='records')
            summaryData = summaryData.to_dict(orient='records')

            # Inserting data!
            con.execute(partials.insert(), data)
            con.execute(summary.insert(), summaryData)
            print("Activity {} SAVED!".format(id))

    print("CSV import done!")
