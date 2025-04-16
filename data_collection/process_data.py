import pandas as pd
import json
import numpy as np

def processData(df):
    df.columns = ['Time Collected', 'Temperature in Celsius', 'Capacitive Reading']

    df2 = pd.read_csv('./data_collection/plantDatabase.csv')
    df2.columns = ['#', 'Name', 'Common Name', 'Type', 'New Jersey Native?', 'Soil Type', 'Soil Moisture', 'Soil pH', 'Drought Tolerance', 'Optimal Light', 'Light Range', 'Hardiness Zone']

    df3 = df2.drop(df2.index[0])
    df4 = df3.drop(columns=['#'])

    dbfinal = df4
    sensordata = df

    conditions = [
        (sensordata['Capacitive Reading'] <= 650),
        (sensordata['Capacitive Reading'] > 650) & (sensordata['Capacitive Reading'] <= 1100),
        (sensordata['Capacitive Reading'] > 1100) & (sensordata['Capacitive Reading'] <= 1550),
        (sensordata['Capacitive Reading'] > 1550)
    ]

    values = ['Dry', 'Dry_Moist', 'Moist', 'Moist_Wet']

    sensordata['Soil Moisture'] = np.select(conditions, values, default=pd.NaT)
    sensordata.head()

    #extract an array of plants that have the specified soil moisture from the plant database, 
    #and store the array into the respective lists

    dryplants = dbfinal.loc[dbfinal['Soil Moisture'] == 'Dry', 'Common Name']
    drymoist = dbfinal.loc[dbfinal['Soil Moisture'] == 'Dry_Moist', 'Common Name']
    moistplants = dbfinal.loc[dbfinal['Soil Moisture'] == 'Moist', 'Common Name']
    moistwet = dbfinal.loc[dbfinal['Soil Moisture'] == 'Moist_Wet', 'Common Name']

    con2 = [
        (sensordata['Soil Moisture'] == 'Dry'),
        (sensordata['Soil Moisture'] == 'Dry_Moist'),
        (sensordata['Soil Moisture'] == 'Moist'),
        (sensordata['Soil Moisture'] == 'Moist_Wet')
    ]

    #convert the lists of plants with a specified soil moisture into strings so they  
    #can be returned as recommendations in a new column of the soil moisture dataframe

    dpst = ",".join(str(x) for x in dryplants)
    dmst = ",".join(str(x) for x in drymoist)
    mpst = ",".join(str(x) for x in moistplants)
    mwst = ",".join(str(x) for x in moistwet)

    val2 = [dpst, dmst, mpst, mwst]

    sensordata['Plant Recommendations'] = np.select(con2, val2, default=pd.NaT)
    return sensordata

