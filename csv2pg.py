import os, glob
import pandas as pd
from dbSetup import summary, partials

def csv2pg(con, meta, inFolder, inFormat):
    '''Import csv from folder to PGSQL'''
    # TODO convert '--' to NULL before import

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

