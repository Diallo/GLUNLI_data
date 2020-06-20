import ast
import csv
import pandas as pd
fileName = "./finaloutput.csv"
#
df = pd.read_csv(fileName, skiprows=0)


data = []
i = 0
for index, row in df.iterrows():
    tempResult = []
    tempResult.append(row[0])
    tempResult.append(row[1])
    tempResult.append(row[2])
    tempResult.append(row[3])


    try:
        x = ast.literal_eval(row[4])
        lon = x[0]
        lat = x[1]
        city = x[2].replace(","," ")
        photoRef = x[3].replace(","," ")
        photoAttrib = x[4].replace(","," ")

        tempResult.append(lon)
        tempResult.append(lat)
        tempResult.append(city)
        tempResult.append(photoRef)
        tempResult.append(photoAttrib)

    except:
        i += 1
    data.append(tempResult)



df = pd.DataFrame.from_records(data)
df = df.iloc[::2]
df = df.iloc[::2]
df = df.iloc[::2]

df.to_csv("DEMOFORMATTED.csv", index=False)