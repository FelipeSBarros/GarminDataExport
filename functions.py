import psycopg2

class DBManagement:
    def __init__(self, dbname="gastos.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def get_garmin_id():
        stmt = "SELECT garmin_id FROM activitiesid"
        cur.execute(stmt)
        return [x[0] for x in cur.fetchall()]

    def gpxImport(Activitywd = None):
        from osgeo import ogr
        from glob import glob

        # Establish a connection to a PostGIS database
        pg = ogr.GetDriverByName('PostgreSQL')
        if pg is None:
            raise RuntimeError('PostgreSQL driver not available')
        conn = pg.Open("PG:dbname='GarminTest' user='postgres' host='localhost' password='postgres'", True)
        if conn is None:
            raise RuntimeError('Cannot open dataset connection')

        # Loop through each GPX file
        for gpx_file in glob(Activitywd + '/*.gpx'):
            print(gpx_file)
            ds = ogr.Open(gpx_file)
            if ds is None:
                print('Skipping ' + gpx_file)
            print('Opened ' + gpx_file)
            prefix = os.path.splitext(os.path.basename(gpx_file))[0]
            # Get each layer
            for iLayer in range(ds.GetLayerCount()):
                layer = ds.GetLayer(iLayer)
                layer_name = prefix + '_' + layer.GetName()
                print(layer_name)
                if layer.GetFeatureCount() == 0:
                    print(' -> Skipping ' + layer_name + ' since it is empty')
                else:
                    print(' -> Copying ' + layer_name)
                    pg_layer = conn.CopyLayer(layer, layer_name)
                    if pg_layer is None:
                        print(' |-> Failed to copy')