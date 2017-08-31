'''
This parser print the mean velocity in certain window of time.
Before of this parser we must run the velocity_parser
'''
from __future__ import division
import pandas as pd
import os
import numpy as np
import datetime
import time

interval = input("Time interval in minute: ")

#week folder 
weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for week in weeks:
    
    if '.' in week:

        pathWeek = os.path.join(os.getcwd(), week)

        # days folder
        days = [name for name in os.listdir(pathWeek)]

        for day in days:
            path = os.path.join(pathWeek, day)
            # junction folders
            junctions = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

            for junction in junctions:
                # es: /feb/27/01-227 --> month/day/junction
                path1 = os.path.join(path, junction)
                
                files = []
                for file in os.listdir(path1):
               
                    if "every_velocity" in file:

                        path2 = os.path.join(path1,file)
                        print 'path2: ' + path2

                        pathToDel = os.path.join(path1, "interval_velocity-" + path2[-11:])
                        if os.path.exists(pathToDel):
                            os.remove(pathToDel)
                            print 'Deleted file: ' + pathToDel
                        
                        if os.path.exists(path2):
                            df = pd.read_csv(path2, sep='|', header=None)
                            print 'Analyzing file: ' + path2
                            data = df.values
                            # 27-Feb-2015 19:58:04.750
                            # beginning time for the comparison
                            begin_time = datetime.datetime.strptime(data[0, 1], "%d-%b-%Y %H:%M:%S.%f")
                            #casual number to make sure that we bring a data in the correct day
                            begin_time2 = datetime.datetime.strptime(data[50, 1], "%d-%b-%Y %H:%M:%S.%f")
                            if begin_time.day != begin_time2.day:
                                #FIRST TIME --> Midnight
                                round_begin_time = begin_time.replace(hour=00,minute=00,day=begin_time2.day)
                            else:
                                #FIRST TIME --> Midnight
                                round_begin_time = begin_time.replace(hour=00,minute=00)
                            mean_velocity = data[0, 2]
                            counter = 1 

                            for i in range(1, data.shape[0]):
                                id = data[i, 0]
                                junction = id[:7]
                                junction2 = junction.replace("/", "-")
                                path3 = os.path.join(path1, "interval_velocity-" + junction2 + ".csv")
                                #END TIME OF THE FIRST INTERVAL
                                round_end_time = round_begin_time + datetime.timedelta(minutes = interval)
                                #ACTUAL LOGGED TIME                          
                                log_time = datetime.datetime.strptime(data[i, 1], "%d-%b-%Y %H:%M:%S.%f")
                                if log_time.day != begin_time2.day:
                                    log_time = log_time.replace(hour=00,minute=00,day=begin_time2.day)

                                if log_time >= begin_time and log_time <= round_end_time :
                                    mean_velocity += data[i, 2]
                                    counter += 1
                                else:
                                    velocity = mean_velocity / counter
                                    toWrite = str(round_begin_time) + "|" + str(round_end_time) + "|" + str(velocity)
                                    round_begin_time = round_end_time
                                    round_end_time = round_end_time + datetime.timedelta(minutes = interval)
                                    f = open(path3, "a")
                                    f.write(toWrite + '\n')
                                    f.close
                                    mean_velocity = data[i, 2]
                                    counter = 1

                            #write the remaining data
                            velocity = mean_velocity / counter
                            toWrite = str(round_begin_time) + "|" + str(round_end_time) + "|" + str(velocity)
                            f = open(path3, "a")
                            f.write(toWrite + '\n')