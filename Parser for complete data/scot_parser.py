'''
This parser will extract useful data from scoot_detectors.csv. This file contains information about each separate SCOOT
detector. In particular, we'll extract: longitude, latitude, topographic identifier, easting (cartesian coordinates),
northing (cartesian coordinates) and detector id. With this extracted information we can build a database to retrieve
in a faster way the location of the detectors.
'''

import pandas as pd

var = input("File name: ")
df = pd.read_csv(var + '.csv', sep=',', header=None)
data = df.values
x = 0
s = set([])

for i in range(0, data.shape[0]):
    # Debug Print
    if i == x:
        print(str(x) + ' - Parsing - Please Wait')
        x += 500
    if data[i, 13] not in s:
        s.add(data[i, 13])
        # long, lat, toid, easting, northing, detector_n
        toWrite = str(data[i, 0]) + ',' + str(data[i, 1]) + ',' + str(data[i, 4]) + ',' + str(data[i, 5]) + ',' +\
                  str(data[i, 6]) + ',' + str(data[i, 13])
        f = open("scot_reference_parsed.csv", "a")
        f.write(toWrite + '\n')
        f.close()
print('All Parsed')
