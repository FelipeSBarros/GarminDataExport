import os, glob
from geoalchemy2 import WKTElement # To conver geom to WKT
import geopandas as gpd
import fiona
from dbSetup import get_garmin_id


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
        if idGarmin in get_garmin_id(con):
            print("Activity {} already saved!".format(idGarmin))
        else:
            # Identify Layers in file
            layers = fiona.listlayers(i)
            for l in layers:
                # l = layers[0]
                table = meta.tables[l] # getting spatial table related to layer
                try:
                    data = gpd.read_file(i, layer=l)
                    # Use GeoAlchemy's WKTElement to create a geom with SRID
                    data['geometry'] = data['geometry'].apply(create_wkt_element) # TODO insert WKTElement(geom.wkt, srid=4326) direct here instead of creatinf function?
                    data["idGarmin"] = idGarmin
                    # Converting to Dictionary to import several feature at once
                    dataDict = data.to_dict(orient='records')
                    # Executing insert statement
                    con.execute(table.insert(), dataDict)
                    print("Layer {} from {} SAVED!".format(l, i))
                except KeyError:
                    print("Layer {} from {} data without feature...".format(l, i))
                #except:
                #    print("Other error ocurred")

