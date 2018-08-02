# TODO insert classes to select, import data....

class dbHelper:
    def __init__(self, databaseUser, databasePW, databaseName, databaseServer, port = 5432):
        self.url = 'postgresql://{}:{}@{}:{}/{}'
        self.url = self.url.format(databaseUser, databasePW, databaseServer, port, databaseName)
        # The return value of create_engine() is our connection object
        self.con = create_engine(self.url, client_encoding='utf8')
        # We then bind the connection to MetaData()
        self.meta = MetaData(bind=self.con, reflect=True)


"""Tstes"""
db = dbHelper(databaseUser, databasePW, databaseName, databaseServer)
db.meta.tables["summary"]
db.con