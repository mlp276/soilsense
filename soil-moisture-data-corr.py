import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="darkgrid")

df = pd.read_csv('sensorData01.csv')

df.columns = ['Time in Millisecond Since UTC Epoch', 'Temperature in Celsius', 'Capacitive Reading']

df2 = pd.read_csv('plantDatabase.csv')

df2.columns = ['#', 'Name', 'Common Name', 'Type', 'New Jersey Native?', 'Soil Type', 'Soil Moisture', 'Soil pH', 'Drought Tolerance', 'Optimal Light', 'Light Range', 'Hardiness Zone']

df3 = df2.drop(df2.index[0])

df4 = df3.drop(columns=['#'])

dbfinal = df4

s1 = df

conditions = [
    (s1['Capacitive Reading'] <= 650),
    (s1['Capacitive Reading'] > 650) & (s1['Capacitive Reading'] <= 1100),
    (s1['Capacitive Reading'] > 1100) & (s1['Capacitive Reading'] <= 1550),
    (s1['Capacitive Reading'] > 1550)
]

values = ['Dry', 'Dry_Moist', 'Moist', 'Moist_Wet']

s1['Soil Moisture'] = np.select(conditions, values, default=pd.NaT)

s1.head()

#extract an array of plants that have the specified soil moisture from the plant database, 
#and store the array into the respective lists

dryplants = dbfinal.loc[dbfinal['Soil Moisture'] == 'Dry', 'Common Name']
print(dryplants)

drymoist = dbfinal.loc[dbfinal['Soil Moisture'] == 'Dry_Moist', 'Common Name']
print(drymoist)

moistplants = dbfinal.loc[dbfinal['Soil Moisture'] == 'Moist', 'Common Name']
print(moistplants)

moistwet = dbfinal.loc[dbfinal['Soil Moisture'] == 'Moist_Wet', 'Common Name']
print(moistwet)

con2 = [
    (s1['Soil Moisture'] == 'Dry'),
    (s1['Soil Moisture'] == 'Dry_Moist'),
    (s1['Soil Moisture'] == 'Moist'),
    (s1['Soil Moisture'] == 'Moist_Wet')
]

#convert the lists of plants with a specified soil moisture into strings so they  
#can be returned as recommendations in a new column of the soil moisture dataframe

dpst = " ".join(str(x) for x in dryplants)
dmst = " ".join(str(x) for x in drymoist)
mpst = " ".join(str(x) for x in moistplants)
mwst = " ".join(str(x) for x in moistwet)

val2 = [dpst, dmst, mpst, mwst]

s1['Plant Recommendations'] = np.select(con2, val2, default=pd.NaT)

s1.to_html('sensor01rec.html')