'''
This parser computes the mean interarrival time for the work and festive week
in a time frame provided as input
'''
from __future__ import division
import pandas as pd
import os
import numpy as np
import datetime
import shutil

festiveJunctionMap = {}
workJunctionMap = {}

#create final work path
globalWorkPath = os.path.join(os.getcwd(), "Global Feb Work Week Interarrival")
if os.path.exists(globalWorkPath):
    print 'The global work path already exist. Please delete it'
    shutil.rmtree(globalWorkPath)

#create final festive path
globalFestivePath = os.path.join(os.getcwd(), "Global Feb Festive Week Interarrival")
if os.path.exists(globalFestivePath):
    print 'The global festive path already exist. Please delete it'
    shutil.rmtree(globalFestivePath)

interval = input("Time Interval in minutes. Same of the single interval intervarrival: ")

#week folder 
weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for dayIndex, week in enumerate(weeks):

    #The folder of the raw data contains a .
    if '.' in week:

        if 'Velocity' not in week:

            pathWeek = os.path.join(os.getcwd(), week)

            print 'Week: ' + pathWeek

            if 'Festive' in pathWeek:
                work = False
            elif 'Work' in pathWeek:
                work = True

            # days folder
            days = [name for name in os.listdir(pathWeek)]

            for day in days:

                print 'Day: ' + day

                path = os.path.join(pathWeek, day)
                # junction folders
                junctions = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

                for junction in junctions:
                   
                    path1 = os.path.join(path, junction)
                    
                    for file in os.listdir(path1):

                        if 'interarrival_time' in file:
                            path2 = os.path.join(path1, file)
                            if os.path.exists(path2):
                                df = pd.read_csv(path2, sep='|', header=None)
                                data = df.values

                                idJunction = file[-11:-4]
                                print 'Junction: ' + idJunction
                                #check if the junction is already in the map
                                if work:
                                    if idJunction not in workJunctionMap:
                                        workJunctionMap[idJunction] = {}
                                else:
                                    if idJunction not in festiveJunctionMap:
                                        festiveJunctionMap[idJunction] = {}
                                

                                for i in range(0, data.shape[0]):
                                    interarrival_time = data[i,2]

                                    if work:
                                        innerMap = workJunctionMap[idJunction]
                                        #add the key in the inner map
                                        if day not in innerMap:
                                            innerMap[day] = []

                                        innerMap[day].append(interarrival_time)

                                    else:
                                        innerMap = festiveJunctionMap[idJunction]
                                        if day not in innerMap:
                                            innerMap[day] = []

                                        innerMap[day].append(interarrival_time)

#create directory
os.mkdir(globalWorkPath)
os.mkdir(globalFestivePath)

#Work Week
for junction in workJunctionMap:

    innerMap = workJunctionMap[junction]

    for dayIndex, days in enumerate(innerMap):

        #we need to create an empty set for the global week
        if dayIndex == 0:
            globalWeek = [0 for x in range(len(innerMap[days]))] 
            
        dayVelocityList = innerMap[days]

        i = 0;

        for arrivalIndex, interarrival_time in enumerate(dayVelocityList):
            globalWeek[arrivalIndex] = globalWeek[arrivalIndex] + interarrival_time
            i += 1
        
    for j, vel in enumerate(globalWeek):
        globalWeek[j] = globalWeek[j]/(dayIndex+1)

    #write the result to disk
    path = os.path.join(globalWorkPath, 'work_week_interarrival_time_' + junction + '.csv')
    begin_time = datetime.datetime.strptime('00:00', "%H:%M")
    end_time = begin_time + datetime.timedelta(minutes=interval)
    for interarrival_time in globalWeek:
        toWrite = begin_time.strftime("%H:%M") + '|' + end_time.strftime("%H:%M") + '|' + str(round(interarrival_time,2))
        begin_time = end_time
        end_time = end_time + datetime.timedelta(minutes=interval)
        f = open(path, "a")
        f.write(toWrite + '\n')
        f.close

#Festive Week
for junction in festiveJunctionMap:

    innerMap = festiveJunctionMap[junction]

    for dayIndex, days in enumerate(innerMap):

        #we need to create an empty set for the global week
        if dayIndex == 0:
            globalWeek = [0 for x in range(len(innerMap[days]))] 
            
        dayVelocityList = innerMap[days]

        i = 0;

        for arrivalIndex, interarrival_time in enumerate(dayVelocityList):
            globalWeek[arrivalIndex] = globalWeek[arrivalIndex] + interarrival_time
            i += 1
        
    for j, vel in enumerate(globalWeek):
        globalWeek[j] = globalWeek[j]/(dayIndex+1)

    #write the result to disk
    path = os.path.join(globalFestivePath, 'festive_week_interarrival_time_' + junction + '.csv')
    begin_time = datetime.datetime.strptime('00:00', "%H:%M")
    end_time = begin_time + datetime.timedelta(minutes=interval)
    for interarrival_time in globalWeek:
        toWrite = begin_time.strftime("%H:%M") + '|' + end_time.strftime("%H:%M") + '|' + str(round(interarrival_time,2))
        begin_time = end_time
        end_time = end_time + datetime.timedelta(minutes=interval)
        f = open(path, "a")
        f.write(toWrite + '\n')
        f.close
