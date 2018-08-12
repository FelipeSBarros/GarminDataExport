from sqlalchemy import Table, Column, Integer, String, Float, Time, create_engine, MetaData, Date, BigInteger # To work with PostgreSQL
from sqlalchemy_views import CreateView, DropView
from sqlalchemy.sql import select
from geoalchemy2 import Geometry
from Infos import databaseServer, databaseName, databaseUser, databasePW

def connect(databaseUser, databasePW, databaseName, databaseServer, port = 5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(databaseUser, databasePW, databaseServer, port, databaseName)

    # The return value of create_engine() is our connection object
    con = create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = MetaData(bind=con)

    return con, meta


con, meta = connect(databaseUser, databasePW, databaseName, databaseServer, port = 5432)

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

"""Create partials and summery table"""
partials = Table('partials', meta,
                 Column('idGarmin', BigInteger),
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
                Column('idGarmin', BigInteger),
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

view = Table('garmin_ids', meta)
definition = select([summary.c.idGarmin]).distinct()
createview = CreateView(view, definition, or_replace=True)
con.execute(createview)


def get_garmin_id(con):
        """Get from database the activities ids already saved"""
        result = con.execute("select * from garmin_ids")
        return [x[0] for x in result] #TODO convert values to set instad of list ?