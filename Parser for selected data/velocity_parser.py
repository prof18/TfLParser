'''
This parser computes the velocity of the single vehicle.
We must provide as input the lenght of the vehicle
'''
from __future__ import division
import os
import pandas as pd

lenght = input("Average Vehicle Lenght - meters: ")

# week folder
weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]
print weeks

for week in weeks:
    print 'Current week: ' + week
    pathWeek = os.path.join(os.getcwd(), week)

    # days folder
    days = [name for name in os.listdir(pathWeek) if os.path.isdir(os.path.join(pathWeek,name))]
    print days

    for day in days:
        path = os.path.join(pathWeek, day)
        print path
        # junction folders
        junctions = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

        print 'Junction: ' + str(junctions)

        for junction in junctions:
            # es: /feb/27/01-227 --> month/day/junction
            path1 = os.path.join(path, junction)

            #used to keep track of file already parsed
            files = []  # single group of detector files
            for file in os.listdir(path1):

                if 'velocity' not in file and 'interarrival' not in file:

                    print 'Analyzing file: ' + file

                    if os.path.join(path1, file) not in files:
                        # es: /feb/27/01-227/01-227g --> month/day/junction/group-of-detectors
                        path2 = os.path.join(path1, file)
                        if os.path.exists(path2):
                            df = pd.read_csv(path2, sep='|', header=None)
                            data = df.values

                            for i in range(0, data.shape[0]):
                                id = data[i, 0]

                                junction = id[:7]
                                junction2 = junction.replace("/", "-")
                                dir = os.path.join(path1, "every_velocity_" + junction2 + ".csv")

                                files.append(dir)

                                id = str(data[i, 0])
                                timestamp = str(data[i, 1])
                                # vehicle_lenght is the number of 250ms measurements during the passage of a single vehicle
                                # seconds that a vehicle is on the detector
                                vehicle_lenght = ((data[i, 2] * 250) / 1000)
                                # velocity of the vehicle
                                velocity_ms = lenght / vehicle_lenght
                                velocity = str(velocity_ms * 3.6)

                                toWrite = id + '|' + timestamp + '|' + velocity

                                f = open(dir, "a")
                                f.write(toWrite + '\n')
                                f.close
