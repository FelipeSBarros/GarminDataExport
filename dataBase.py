from sqlalchemy import Table, Column, Integer, String, Float, Time, create_engine, MetaData, Date, BigInteger # To work with PostgreSQL
from sqlalchemy_views import CreateView, DropView
from sqlalchemy.sql import select
from geoalchemy2 import Geometry, WKTElement# To work with PostgIS
import geopandas as gpd
import os, glob
import pandas as pd
import fiona
from Infos import databaseServer, databaseName, databaseUser, databasePW

class DataBaseHelper:
    def __init__(self):
        asas = asas
        return asasa


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


    def createPartialsTable(con, meta):
        """Create partial and summary tables and garmin_ids view"""
        partials = Table('partials', meta,
                         Column('idGarmin', String),
                         Column('Divisão', Integer),
                         Column('Hora', Time()),
                         Column('Moving Time', String),
                         Column('Distância', Float(2)),
                         Column('Elevation Gain', Integer),
                         Column('Perda da elevação', Integer),
                         Column('Ritmo médio', Time()),
                         Column('Ritmo médio de movimento', String),
                         Column('Melhor ritmo', Time()),
                         Column('Cadência de corrida média', Float(4)),
                         Column('Cadência de corrida máxima', Float(2)),
                         Column('Comprimento médio da passada', String),
                         Column('Frequência cardíaca média', String),
                         Column('FC máxima', String),
                         Column('Temperatura média', String),
                         Column('Calorias', String)
                         )

        summary = Table('summary', meta,
                        Column('idGarmin', String),
                        Column('Divisão', String),
                        Column('Hora', Time()),
                        Column('Moving Time', String),
                        Column('Distância', Float(2)),
                        Column('Elevation Gain', Integer),
                        Column('Perda da elevação', Integer),
                        Column('Ritmo médio', Time()),
                        Column('Ritmo médio de movimento', String),
                        Column('Melhor ritmo', Time()),
                        Column('Cadência de corrida média', Float(4)),
                        Column('Cadência de corrida máxima', Float(2)),
                        Column('Comprimento médio da passada', String),
                        Column('Frequência cardíaca média', String),
                        Column('FC máxima', String),
                        Column('Temperatura média', String),
                        Column('Calorias', String)
                        )
        # Creating partial table
        meta.create_all(con)

        print("Creating VIEW garmin_ids...")
        summary = meta.tables['summary']
        view = Table('garmin_ids', meta)
        definition = select([summary.c.idGarmin]).distinct()
        createview = CreateView(view, definition, or_replace=True)
        con.execute(createview)
        print("Done")


    def get_garmin_id(con):
        """Get from database the activities ids already saved"""
        result = con.execute("select * from garmin_ids")
        return [x[0] for x in result] #TODO convert values to int if necessary


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


    def csv2pg(inFolder, inFormat, databaseUser, databasePW, databaseName, databaseServer):
        '''Import csv from folder to PGSQL'''
        print("connecting with {} database...".format(databaseName))
        con, meta = connect(databaseUser, databasePW, databaseName, databaseServer)

        # Testing if tables already exists
        if not ('partials' in meta.tables and 'summary' in meta.tables):
            print('Tables: {0}, {1} does not exists... creating them!'.format('summary', 'partials'))
            createPartialsTable(con, meta)
        else:
            print('No need to create table...')
            summary = meta.tables["summary"]
            partials = meta.tables["partials"]

        # Creating file list
        fileList = glob.glob(os.path.join(inFolder, "*.{0}".format(inFormat)))
        print("processing {} CSV files".format(len(fileList)))
        for f in fileList:
            # f = fileList[0]
            print(f)
            data = pd.read_csv(f)
            id = f.split('_')[-1]
            id = id.split(".")[0]
            data["idGarmin"] = id
            summaryData = data[-1:]
            data = data.drop(data[-1:].index)

            # Converting to dictionary
            data = data.to_dict(orient='records')
            summaryData = summaryData.to_dict(orient='records')

            # Inserting data!
            con.execute(partials.insert(), data)
            con.execute(summary.insert(), summaryData)

        print("All done!")