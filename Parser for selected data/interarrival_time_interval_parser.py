'''
This parser computes the interarrival times of all the parser
 in a specific time frame provided as input
'''
from __future__ import division
import datetime
import os
import pandas as pd

interval = input("Time interval in minute: ")

# week folder
weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for week in weeks:

    #The folder of the raw data contains a .
    if '.' in week:

        print 'Current week: ' + week
        pathWeek = os.path.join(os.getcwd(), week)  
        days = [name for name in os.listdir(pathWeek) if os.path.isdir(os.path.join(pathWeek, name))]

        for day in days:
            path = os.path.join(pathWeek, day)
            junctions = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

        for junction in junctions:
            path1 = os.path.join(path, junction)

            for file in os.listdir(path1):

                if "velocity" not in file and "interarrival" not in file :

                    path2 = os.path.join(path1, file)
                    print path2  

                    pathToDel = os.path.join(path1, "interarrival_time_interval-" + path2[-11:])
                    if os.path.exists(pathToDel):
                        os.remove(pathToDel)
                        print 'Deleted file: ' + pathToDel

                    if os.path.exists(path2):
                        df = pd.read_csv(path2, sep='|', header=None)
                        print 'Analyzing file: ' + path2
                        data = df.values
                        # beginning time for the comparison
                        begin_time = datetime.datetime.strptime(data[0, 1], "%d-%b-%Y %H:%M:%S.%f")
                        # casual number to make sure that we bring a data in the correct day
                        begin_time2 = datetime.datetime.strptime(data[50, 1], "%d-%b-%Y %H:%M:%S.%f")
                        if begin_time.day != begin_time2.day:
                            # FIRST TIME --> Midnight
                            round_begin_time = begin_time.replace(hour=00, minute=00, day=begin_time2.day)
                        else:
                            # FIRST TIME --> Midnight
                            round_begin_time = begin_time.replace(hour=00, minute=00)

                        mean_interarrival_time = ((data[0, 3] * 250) / 1000)
                        counter = 1

                        for i in range(1, data.shape[0]):
                            id = data[i, 0]
                            junction = id[:7]
                            junction2 = junction.replace("/", "-")
                            path3 = os.path.join(path1, "interarrival_time_interval-" + junction2 + ".csv")
                            # END TIME OF THE FIRST INTERVAL
                            round_end_time = round_begin_time + datetime.timedelta(minutes=interval)
                            # ACTUAL LOGGED TIME
                            log_time = datetime.datetime.strptime(data[i, 1], "%d-%b-%Y %H:%M:%S.%f")
                            if log_time.day != begin_time2.day:
                                log_time = log_time.replace(hour=00, minute=00, day=begin_time2.day)

                            if log_time >= begin_time and log_time <= round_end_time:
                                mean_interarrival_time += ((data[i, 3] * 250) / 1000)
                                counter += 1
                            else:
                                interarrival_time = mean_interarrival_time / counter
                                toWrite = str(round_begin_time) + "|" + str(round_end_time) + "|" + str(interarrival_time)
                                round_begin_time = round_end_time
                                round_end_time = round_end_time + datetime.timedelta(minutes=interval)
                                f = open(path3, "a")
                                f.write(toWrite + '\n')
                                f.close
                                mean_interarrival_time = ((data[i, 3] * 250) / 1000)
                                counter = 1

                        interarrival_time = mean_interarrival_time / counter
                        toWrite = str(round_begin_time) + "|" + str(round_end_time) + "|" + str(interarrival_time)
                        f = open(path3, "a")
                        f.write(toWrite + '\n')
                        print 'File written: ' + path3 + '\n'