import os, glob
from sqlalchemy import Table, Column, Integer, String, Float, Time, create_engine, MetaData, Date, BigInteger # To work with PostgreSQL
from geoalchemy2 import Geometry, WKTElement# To work with PostgIS
import geopandas as gpd
from Infos import databaseServer, databaseName, databaseUser, databasePW
import fiona

def connect(databaseUser, databasePW, databaseName, databaseServer, port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(databaseUser, databasePW, databaseServer, port, databaseName)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = MetaData(bind=con, reflect=True)

    return con, meta
# con, meta = connect(databaseUser, databasePW, databaseName, databaseServer)

def get_garmin_id(con):
    """Get from database the activities ids already saved"""
    result = con.execute("select * from garmin_ids")
    return [x[0] for x in result]


def gpx2pg(inFolder, inFormat, con, meta):

    # Testing if Spatial tables already exists
    if not all(x in meta.tables for x in gpxLayers):
        print('Creating spatial tables...')
        # TODO create only those tables not created yet?!
        createSpatialTable(con, meta) # will create all tables
    else:
        print('No need to create table...')
        #waypoints = meta.tables["waypoints"]
        #routes = meta.tables["routes"]
        #tracks = meta.tables["tracks"]
        #route_points = meta.tables["route_points"]
        #track_points = meta.tables["track_points"]

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
                    data['geometry'] = data['geometry'].apply(create_wkt_element)
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


def createSpatialTable(con, meta):
    """Create partials and summery table"""
    # defining table columns and data type
    waypoints = Table('waypoints', meta,
                      Column('idGarmin', BigInteger),
                      Column('ele', Float),
                      Column('time', Time),
                      Column('magvar', Float),
                      Column('geoidheight', Float),
                      Column('name', String),
                      Column('cmt', String),
                      Column('desc', String),
                      Column('src', String),
                      Column('link1_href', String),
                      Column('link1_text', String),
                      Column('link1_type', String),
                      Column('link2_href', String),
                      Column('link2_text', String),
                      Column('link2_type', String),
                      Column('sym', String),
                      Column('type', String),
                      Column('fix', String),
                      Column('sat', Integer),
                      Column('hdop', Float),
                      Column('vdop', Float),
                      Column('pdop', Float),
                      Column('ageofdgpsdata', Float),
                      Column('dgpsid', Integer),
                      Column('geometry',
                               Geometry('POINT', srid=4326))
                      )

    routes = Table('routes', meta,
                   Column('idGarmin', BigInteger),
                   Column('name', String),
                   Column('cmt', String),
                   Column('desc', String),
                   Column('src', String),
                   Column('link1_href', String),
                   Column('link1_text', String),
                   Column('link1_type', String),
                   Column('link2_href', String),
                   Column('link2_text', String),
                   Column('link2_type', String),
                   Column('number', Integer),
                   Column('type', String),
                   Column('geometry',
                            Geometry('LINESTRING', srid=4326))
                   )

    tracks = Table('tracks', meta,
                   Column('idGarmin', BigInteger),
                   Column('name', String),
                   Column('name', String),
                   Column('cmt', String),
                   Column('desc', String),
                   Column('src', String),
                   Column('link1_href', String),
                   Column('link1_text', String),
                   Column('link1_type', String),
                   Column('link2_href', String),
                   Column('link2_text', String),
                   Column('link2_type', String),
                   Column('number', Integer),
                   Column('type', String),
                   Column('geometry',
                          Geometry('MULTILINESTRING', srid=4326))
                   )

    route_points = Table('route_points', meta,
                         Column('idGarmin', BigInteger),
                         Column('ele', Float),
                         Column('time', Time),
                         Column('magvar', Float),
                         Column('geoidheight', Float),
                         Column('name', String),
                         Column('cmt', String),
                         Column('desc', String),
                         Column('src', String),
                         Column('link1_href', String),
                         Column('link1_text', String),
                         Column('link1_type', String),
                         Column('link2_href', String),
                         Column('link2_text', String),
                         Column('link2_type', String),
                         Column('sym', String),
                         Column('geometry',
                                Geometry('POINT', srid=4326))
                   )

    track_points = Table('track_points', meta,
                         Column('idGarmin', BigInteger),
                         Column('track_fid', String),
                         Column('track_seg_id', String),
                         Column('track_seg_point_id', String),
                         Column('ele', String),
                         Column('time', Date),
                         Column('magvar', String),
                         Column('geoidheight', String),
                         Column('name', String),
                         Column('cmt', String),
                         Column('desc', Integer),
                         Column('src', String),
                         Column('link1_href', String),
                         Column('link1_text', String),
                         Column('link1_type', String),
                         Column('link2_href', String),
                         Column('link2_text', Integer),
                         Column('link2_type', String),
                         Column('sym', String),
                         Column('type', String),
                         Column('fix', String),
                         Column('sat', Integer),
                         Column('hdop', Float),
                         Column('pdop', Float),
                         Column('ageofdgpsdata', Float),
                         Column('dgpsid', Integer),
                         Column('ns3_TrackPointExtension', String),
                         Column('geometry',
                                  Geometry('POINT', srid=4326))
                                 )
    meta.create_all(con)

"""TESTE"""
inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities'
inFormat = "gpx"
gpxLayers = ['waypoints', 'routes', 'tracks', 'route_points', 'track_points']
# createSpatialTable(con, meta)
# gpx2pg(inFolder, inFormat, con, meta)

#spatialTest.drop(con)
# reading file with geopandas... the data will be a dataframe with simple feature geometry
#gdf = gpd.read_file(fileList, layer='tracks')
gdf = gpd.read_file(fileList, layer=layers[2])
gdf.head()
gdf.crs
#gdf.set_crs(epsg=4326)
#gdf.length
#gdf.geom_type
#gdf["geometry"]
#gdf.plot()


# Use 'dtype' to specify column's type
# For the geom column, we will use GeoAlchemy's type 'Geometry'
# geodataframe.to_sql(table_name, engine, if_exists='append', index=False, dtype={'geom': Geometry('POINT', srid= <your_srid>)})

test.schema["properties"]
test["properties"]
#layer.schema["geometry"] # identifying columns and respectives data type
#layer.crs['init'] # identifying SRC

# Creating spatial table
con, meta = connect(databaseUser, databasePW, databaseName, databaseServer)

# Identifying few parameters from data
#layer.schema["properties"]
#layer.schema["geometry"] # identifying columns and respectives data type
#layer.crs['init'] # identifying SRC





layer[0]
layer.crs
type(layer[0]['properties']['name'])
type(layer[0]['properties']['name'])

layer[0].keys()
layer[0]['properties']
layer[0]['geometry']
for i in layer[0]['properties'].keys():
    print(type(layer[0]['properties'][i]))

for i in layer[0]['geometry'].keys():
    print(type(layer[0]['geometry'][i]))

layer[0]['type']
layer.crs
fiona.FIELD_TYPES_MAP
layer.schema
layer.bounds
rec = next(layer)
rec.keys()
layer.schema.keys()
set(rec.keys()) - set(layer.schema.keys())
set(rec['properties'].keys()) == set(layer.schema['properties'].keys())
type(rec['properties']['name'])
#http://toblerity.org/fiona/manual.html#appending-data-to-existing-files
layer[0]
con, meta = connect(databaseUser, databasePW, databaseName, databaseServer)

track = meta.tables["track_points"]
track.to_dict(orient='records')
