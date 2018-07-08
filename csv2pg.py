from Infos import databaseServer, databaseName, databaseUser, databasePW
import sqlalchemy
import geoalchemy2
import os, glob
import pandas as pd

def connect(databaseUser, databasePW, databaseName, databaseServer, port = 5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://federer:grandestslam@localhost:5432/tennis
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(databaseUser, databasePW, databaseServer, port, databaseName)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta

def createPartialsTable(con, meta):
    """Create partials and summery table"""
    partials = Table('partials', meta,
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


# https://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy
#csv_file_path = '/media/felipe/DATA/Repos/GarminProj/Activities/activity_2747046691.csv'
inFolder = r'/media/felipe/DATA/Repos/GarminProj/Activities'
inFormat = "csv"

# summary.drop(con)
# partials.drop(con)
csv2pg(inFolder, inFormat, databaseUser, databasePW, databaseName, databaseServer)