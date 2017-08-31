'''
This parser computes the time needed to reach a detector from another. 
The raw data is road_x.csv and inside it there is the placement of each pair of detectors with its latitude and longitude
'''

from __future__ import division
import pandas as pd
import os
import numpy as np
from haversine import haversine
import shutil

#create final work path
globalWorkPath = os.path.join(os.getcwd(), "Global Feb Work Week Detector Time")
if os.path.exists(globalWorkPath):
    print 'The global work path already exist. Deleting..'
    shutil.rmtree(globalWorkPath)

#create final festive path
globalFestivePath = os.path.join(os.getcwd(), "Global Feb Festive Week Detector Time")
if os.path.exists(globalFestivePath):
    print 'The global festive path already exist. Deleting..'
    shutil.rmtree(globalFestivePath)

os.mkdir(globalWorkPath)
os.mkdir(globalFestivePath)

interval = input("Time interval in minute: ")

folders = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for folder in folders:

	if 'detector_road_distance' in folder:

		distancePath = os.path.join(os.getcwd(), folder)
		
		for file in os.listdir(distancePath):

			pathRoad = os.path.join(distancePath, file)

			print 'Analyzing: ' + pathRoad

			if (os.path.exists(pathRoad)):
				df = pd.read_csv(pathRoad, sep='|')
				data = df.values

				for i in range(0, data.shape[0]):
					latA = data[i,0]
					longA = data[i,1]
					rawIdA = data[i,2]
					detectorIdA = rawIdA[1:-1].replace("/", "-")
			
					latB = data[i,3]
					longB = data[i,4]
					rawIdB = data[i,5]
					detectorIdB = rawIdB[1:-1].replace("/", "-")

					A = (latA, longA)
					B = (latB, longB)
					distanceAB = round(haversine(A, B)*1000,2)

					folders2 = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)] 
					for folder2 in folders2:
						if 'Festive Week Velocity' in folder2:
							velocityFolder = os.path.join(os.getcwd(), folder2)

							for file2 in os.listdir(velocityFolder):
								if '.png' not in file2 and detectorIdA in file2:
									pathVelocity = os.path.join(velocityFolder, file2)
									pathToWrite = os.path.join(globalFestivePath, detectorIdA + '_' + detectorIdB + '_time.csv')
									df2 = pd.read_csv(pathVelocity, sep='|', header=None)
									data2 = df2.values

									for j in range(0, data2.shape[0]):
										velocity = data2[j,2]/3.6
										time = distanceAB/(velocity)
										toWrite = data2[j,0] + '|' + data2[j,1] + '|' + str(round(time,2))
										f = open(pathToWrite, "a")
										f.write(toWrite + '\n')
										f.close

						elif 'Work Week Velocity' in folder2:

							velocityFolder = os.path.join(os.getcwd(), folder2)

							for file2 in os.listdir(velocityFolder):
								if '.png' not in file2 and detectorIdA in file2:
									pathVelocity = os.path.join(velocityFolder, file2)
									pathToWrite = os.path.join(globalWorkPath, detectorIdA + '_' + detectorIdB + '_time.csv')
									df2 = pd.read_csv(pathVelocity, sep='|', header=None)
									data2 = df2.values

									for j in range(0, data2.shape[0]):
										velocity = data2[j,2]/3.6
										time = distanceAB/(velocity)
										toWrite = data2[j,0] + '|' + data2[j,1] + '|' + str(round(time,2))
										f = open(pathToWrite, "a")
										f.write(toWrite + '\n')
										f.close


									









