#from Infos import databaseServer, databaseName, databaseUser, databasePW
#import psycopg2
import sqlalchemy
databaseUser = 'federer'
databasePW = 'grandestslam'
databaseName = 'tennis'
databaseServer='localhost'
port = 5432
def connect(databaseUser, databasePW, databaseName, databaseServer, port):
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

# using function created above to connect to postgre
con, meta = connect(databaseUser, databasePW, databaseName, databaseServer, port)

#Creating table
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Time, Float


slams = Table('slams', meta,
    Column('name', String, primary_key=True),
    Column('country', String)
)

results = Table('results', meta,
    Column('slam', String, ForeignKey('slams.name')),
    Column('year', Integer),
    Column('result', String)
)

# Create the above tables
meta.create_all(con)

for table in meta.tables:
    print(table)

# Insert data
clause = slams.insert().values(name='Wimbledon', country='United Kingdom')
con.execute(clause)

clause = slams.insert().values(name='Roland Garros', country='France')

result = con.execute(clause)

result.inserted_primary_key


victories = [
    {'slam': 'Wimbledon', 'year': 2003, 'result': 'W'},
    {'slam': 'Wimbledon', 'year': 2004, 'result': 'W'},
    {'slam': 'Wimbledon', 'year': 2005, 'result': 'W'}
]
con.execute(meta.tables['results'].insert(), victories)
#victories[0].keys()

# Selecting
for row in con.execute(results.select()):
    print(row)

clause = results.select().where(results.c.year == 2005)
for row in con.execute(clause):
    print(row)

#Experiments


# using function created above to connect to postgre
con, meta = connect(databaseUser, databasePW, databaseName, databaseServer, port)



# Creating partial table
partials = Table('partials', meta,
                 Column('idGarmin', String),
                 Column('Divisão', String),
                 Column('Hora', Time()),
                 Column('Moving Time', Time()),
                 Column('Distância', Float(2)),
                 Column('Elevation Gain', Integer),
                 Column('Perda da elevação', Integer),
                 Column('Ritmo médio', Time()),
                 Column('Ritmo médio de movimento', Time()),
                 Column('Melhor ritmo', Time()),
                 Column('Cadência de corrida média', Float(4)),
                 Column('Cadência de corrida máxima', Float(2)),
                 Column('Comprimento médio da passada', String),
                 Column('Frequência cardíaca média', String),
                 Column('FC máxima', String),
                 Column('Temperatura média', Float(2)),
                 Column('Calorias', String)
                 )

summary = Table('summary', meta,
                 Column('idGarmin', String),
                 Column('Divisão', String),
                 Column('Hora', Time()),
                 Column('Moving Time', Time()),
                 Column('Distância', Float(2)),
                 Column('Elevation Gain', Integer),
                 Column('Perda da elevação', Integer),
                 Column('Ritmo médio', Time()),
                 Column('Ritmo médio de movimento', Time()),
                 Column('Melhor ritmo', Time()),
                 Column('Cadência de corrida média', Float(4)),
                 Column('Cadência de corrida máxima', Float(2)),
                 Column('Comprimento médio da passada', String),
                 Column('Frequência cardíaca média', String),
                 Column('FC máxima', String),
                 Column('Temperatura média', Float(2)),
                 Column('Calorias', String)
                 )

meta.create_all(con)

for table in meta.tables:
    print(table)

# Inserting

# clause = partials.insert().values(idGarmin='Wimbledon', Hora='00:11:31.00')
#con.execute(clause)

# https://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy
csv_file_path = '/media/felipe/DATA/Repos/GarminProj/Activities/activity_2747046691.csv'
import pandas as pd
data = pd.read_csv(csv_file_path)
id = csv_file_path.split('_')[-1]
id = id.split(".")[0]
data["idGarmin"] = id
summaryData = data[-1:]
#data.drop(data[data.Divisão == "Summary"].index)
data = data.drop(data[-1:].index)
# INSERIR idGARMIN
data = data.to_dict(orient='records')
summaryData = summaryData.to_dict(orient='records')
data[0].keys()
con.execute(partials.insert(), data)
con.execute(summary.insert(), summaryData)

#session.commit()

#session.close()