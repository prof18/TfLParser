'''
This parser computes the throughput of every access point and generates a plot
The detectors are matched with the access point using some map
'''

import pandas as pd
import os
import numpy as np
import datetime
import shutil
import matplotlib.pyplot as plt

#Variables
interval = input("Time interval in minute: ")
sizeInterval = (24*60)/interval
print sizeInterval

#detector in ap
threeOclock = ['01-233a','01-233x','01-233d','01-276c','01-276c','01-140s','01-140s','01-142w','01-142w','01-276h','01-276h','01-143c',
'01-143c','01-143r','01-142u','01-142u','01-143a','01-143a','01-159w','01-159w','01-232s','01-232t','01-157g','01-556a','01-237c']
sixOclock = ['01-222a','01-307e','01-160a','01-307g','01-307g','01-204k','01-204k','01-139h','01-139h','01-204l','01-204l','01-140t','01-140t'
,'01-160d','01-233d','01-161e','01-160c','01-160c','01-353j','01-161g','01-162a','01-353m','01-160d','01-161e','01-160c','01-160c','01-353j',
'01-161g','01-162a','01-353m','01-162c']
elevenOclock = ['01-229d','01-229c','01-223d','01-585a','01-223c','01-294h','01-229b','01-228d','01-229c','01-223d','01-223b1','01-235h1',
'01-585a','01-223c','01-233b','01-585b','01-235e','01-235a','01-237a']

#ap map
threeOclockMap = {'1' : ['01-556a','01-237c','01-157g','01-158k','01-232s','01-232t','01-159w','01-159w','01-143a','01-143a','01-142u',
'01-142u','01-143r','01-143c','01-143c','01-276h','01-276h','01-142w','01-142w','01-140s','01-140s','01-276c','01-276c']}
sixOclockMap = {'1' : ['01-222a','01-307e','01-160a','01-307g','01-307g','01-204k','01-204k','01-139h','01-139h','01-204l',
'01-204l','01-140t','01-140t'],
'2' : ['01-162c','01-353m','01-162a','01-161g','01-353j','01-160c','01-160c','01-161e','01-204k','01-204k','01-139h','01-139h',
'01-204l','01-204l','01-140t','01-140t'],
'3' : ['01-162c','01-353m','01-162a','01-161g','01-353j','01-160c','01-160c','01-161e','01-307g','01-307g','01-160a','01-307e','01-222a']}
elevenOclockMap = {'1' : ['01-229d', '01-229q', '01-229s', '01-229c', '01-223d', '01-223b', '01-235h', '01-235e'],
'2' : ['01-229d', '01-229q', '01-229s', '01-229c', '01-223d', '01-223b', '01-235h', '01-235a', '01-237a'],
'3' : ['01-228d', '01-229b', '01-294h', '01-229s', '01-229c', '01-223d', '01-223b', '01-235h', '01-235a', '01-237a'],
'4' : ['01-228d', '01-229b', '01-294h', '01-229s', '01-229c', '01-223d', '01-223b', '01-235h', '01-235e'],
'5' : ['01-228d', '01-229b', '01-294h', '01-229s', '01-229c', '01-223d', '01-585b','01-233b','01-223c','01-585a'],
'6' : ['01-229d', '01-229q', '01-229s', '01-229c', '01-223d', '01-585b','01-233b','01-223c','01-585a'],
'7' : ['01-585b','01-233b','01-223c','01-585a', '01-223b', '01-235h'],
'8' : ['01-585b','01-233b','01-223c','01-585a' , '01-223b', '01-235h',  '01-235a', '01-237a']}

threeOclocRoadMap = {'1' : ['01-556a','01-237c','01-157g','01-158k','01-232s','01-232t','01-159w','01-159w','01-143a','01-143a'],
'2' : ['01-142u','01-142u','01-143r','01-143c','01-143c','01-276h','01-276h','01-142w','01-142w','01-140s','01-140s','01-276c','01-276c']}
sixOclockRoadMap = {'1' : ['01-162c','01-353m','01-162a','01-161g','01-353j','01-160c','01-160c','01-161e','01-307g','01-307g','01-160a','01-307e','01-222a'],
'2' : ['01-204k','01-204k','01-139h','01-139h','01-204l','01-204l','01-140t','01-140t','01-160d']}
elevenOclockRoadMap = {'1' : ['01-229c','01-223d','01-223b1','01-235h1'],
'2' : ['01-585a','01-223c','01-233b','01-585b'],
'3' : ['01-235e','01-235a','01-237a'],
'4' : ['01-228d','01-229b','01-294h','01-229s','01-229q','01-229d']}

#Map for time
threeOclockTimeMap = {'1' : [0 for x in range(sizeInterval)]}
sixOclockTimeMap = {'1' : [0 for x in range(sizeInterval)],
'2' : [0 for x in range(sizeInterval)],
'3' : [0 for x in range(sizeInterval)]}
elevenOclockTimeMap = {'1' : [0 for x in range(sizeInterval)],
'2' : [0 for x in range(sizeInterval)],
'3' : [0 for x in range(sizeInterval)],
'4' : [0 for x in range(sizeInterval)],
'5' : [0 for x in range(sizeInterval)],
'6' : [0 for x in range(sizeInterval)],
'7' : [0 for x in range(sizeInterval)],
'8' : [0 for x in range(sizeInterval)]}

#map for vehicle number
threeOclockVehicleNumMap = {'1' : [0 for x in range(sizeInterval)],
'2' : [0 for x in range(sizeInterval)]}
sixOclockVehicleNumMap = {'1' : [0 for x in range(sizeInterval)],
'2' : [0 for x in range(sizeInterval)]}
elevenOclockVehicleNumMap = {'1' : [0 for x in range(sizeInterval)],
'2' : [0 for x in range(sizeInterval)],
'3' : [0 for x in range(sizeInterval)],
'4' : [0 for x in range(sizeInterval)]}

#1 pkt throughput --> bps
onePckThroughput = (800/0.1)*8
#kps converting factor
toKbps = 1024
#Mbps converting factor
toMbps = 1048576

#Helper Functions
def worstTimeRoad(APmap,timePath,timeMap):

	for road in APmap:

		detectorSet = APmap[road]

		print 'Road: ' + road

		for i in range(0, len(detectorSet)):
			if i != len(detectorSet)-1:
				pair1 = detectorSet[i] + '_' + detectorSet[i+1]
				pair2 = detectorSet[i+1] + '_' + detectorSet[i]

				for file in os.listdir(timePath):
					if pair1 in file or pair2 in file:
						if pair1 in file:
							print 'Analyzing: ' + pair1
						else:
							print 'Analyzing: ' + pair2
							
						pairPath = os.path.join(timePath,file)

						if os.path.exists(pairPath):
							df = pd.read_csv(pairPath, sep='|', header=None)
							data = df.values

							for j in range(0, data.shape[0]):
								timeGlobal = data[j,2]
								timeMap[road][j] = round(timeMap[road][j] + timeGlobal,2)

	#select the worst time case
	maxRoad12 = 0
	roadIndex = -1
	for road in timeMap:
		innerSet = timeMap[road]
		for i in range(0, len(innerSet)):
			if i == 0:
				summa = 0
			summa += innerSet[i]
		if summa > maxRoad12:
			maxRoad12 = summa
			roadIndex = road

	print timeMap[roadIndex]
	print roadIndex

	return timeMap[roadIndex]


def vehicleNumber(roadMap, vehiclePath, vehicleNumMap):

	for road in roadMap:

		detectorSet = roadMap[road]
		print 'Road VN: ' + road

		for i in range(0, len(detectorSet)):
			detector = detectorSet[i]

			for file in os.listdir(vehiclePath):
				if detector in file and '.png' not in file:

					detectorPath = os.path.join(vehiclePath, file)
					print 'Analyzing: ' + detectorPath

					if os.path.exists(detectorPath):
						df = pd.read_csv(detectorPath, sep="|", header=None)
						data = df.values

						for j in range(0, data.shape[0]):
							vehicleGlobal = data[j,2]
							vehicleNumMap[road][j] = round(vehicleNumMap[road][j] + vehicleGlobal,2)

		for k in range(0, len(vehicleNumMap[road])):
			vehicleNumMap[road][k] = round(vehicleNumMap[road][k] / len(detectorSet),0)


	#sum the road vehicle number
	vehicleNumPerS = [0 for x in range(sizeInterval)]
	for road in vehicleNumMap:
		for i in range(0, sizeInterval):
			vehicleNumPerS[i] += vehicleNumMap[road][i]

	for j in range(0, sizeInterval):
		vehicleNumPerS[j] = round(vehicleNumPerS[j]/(interval*60),4)

	return vehicleNumPerS

def throughputWrite(worstRoadMap, vehicleNumMapS, path):
	print 'Writing: ' + path
	for i in range(0, sizeInterval):
		if i == 0:
			begin_time = datetime.datetime.strptime('00:00', "%H:%M")
			end_time = begin_time + datetime.timedelta(minutes=interval)
		throughput = round(((worstRoadMap[i]*vehicleNumMapS[i])*onePckThroughput)/toMbps,2)
		toWrite = begin_time.strftime("%H:%M") + '|' + end_time.strftime("%H:%M") + '|' + str(throughput)
		begin_time = end_time
		end_time = begin_time + datetime.timedelta(minutes=interval)
		f = open(path, 'a')
		f.write(toWrite + '\n')
		f.close

def throughputPlot(path):

	finalMap = {}

	for file in os.listdir(path):
		
		if 'png' not in file:
			filePath = os.path.join(path, file)

			if os.path.exists(filePath):
				df = pd.read_csv(filePath, sep='|', header=None)
				data = df.values
				time = list(range(data.shape[0]))
				throughput = []
				for i in range(0, data.shape[0]):
					throughput.append(data[i,2])

			if '11' in file:
				finalMap['11'] = throughput
			elif '3' in file:
				finalMap['3'] = throughput
			elif '6' in file:
				finalMap['6'] = throughput

	return finalMap, time

		
#Main Program
globalWorkPath = os.path.join(os.getcwd(), "Global Feb Work Week Throughput Conf 2")
if os.path.exists(globalWorkPath):
    print 'The global work path already exist. Deleting..'
    shutil.rmtree(globalWorkPath)

#create final festive path
globalFestivePath = os.path.join(os.getcwd(), "Global Feb Festive Detector Throughput Conf 2")
if os.path.exists(globalFestivePath):
    print 'The global festive path already exist. Deleting..'
    shutil.rmtree(globalFestivePath)

os.mkdir(globalWorkPath)
os.mkdir(globalFestivePath)



#velocity folder
folders = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for folder in folders:

	if 'Work Week Detector Time' in folder:

		timePath = os.path.join(os.getcwd(), folder)

		workTreeOclockWorstRoad = worstTimeRoad(threeOclockMap, timePath, threeOclockTimeMap)
		workSixOclockWorstRoad = worstTimeRoad(sixOclockMap, timePath, sixOclockTimeMap)
		workElevenOclockWorstRoad = worstTimeRoad(elevenOclockMap, timePath, elevenOclockTimeMap)

	elif 'Festive Week Detector Time' in folder:

		timePath = os.path.join(os.getcwd(), folder)

		festiveTreeOclockWorstRoad = worstTimeRoad(threeOclockMap, timePath, threeOclockTimeMap)
		festiveSixOclockWorstRoad = worstTimeRoad(sixOclockMap, timePath, sixOclockTimeMap)
		festiveElevenOclockWorstRoad = worstTimeRoad(elevenOclockMap, timePath, elevenOclockTimeMap)

for folder in folders:

	if 'Work Week Vehicle Number' in folder:

		vehiclePath = os.path.join(os.getcwd(), folder)

		workTreeOclockVehicleNumberPerS = vehicleNumber(threeOclocRoadMap, vehiclePath, threeOclockVehicleNumMap)
		workSixOclockVehicleNumberPerS = vehicleNumber(sixOclockRoadMap, vehiclePath, sixOclockVehicleNumMap)
		workElevenOClockVehicleNumberPerS = vehicleNumber(elevenOclockRoadMap, vehiclePath, elevenOclockVehicleNumMap)

	elif 'Festive Week Vehicle Number' in folder:

		vehiclePath = os.path.join(os.getcwd(), folder)

		festiveTreeOclockVehicleNumberPerS = vehicleNumber(threeOclocRoadMap, vehiclePath, threeOclockVehicleNumMap)
		festiveSixOclockVehicleNumberPerS = vehicleNumber(sixOclockRoadMap, vehiclePath, sixOclockVehicleNumMap)
		festiveElevenOClockVehicleNumberPerS = vehicleNumber(elevenOclockRoadMap, vehiclePath, elevenOclockVehicleNumMap)

#Work Week

#Access Point 3 oClock
path = os.path.join(globalWorkPath, "work_week_throughtput_3_oclock.csv")
throughputWrite(workTreeOclockWorstRoad, workTreeOclockVehicleNumberPerS,path)

#Access Point 6 oClock
path = os.path.join(globalWorkPath, "work_week_throughtput_6_oclock.csv")
throughputWrite(workSixOclockWorstRoad, workSixOclockVehicleNumberPerS,path)

#Access Point 11 oClock
path = os.path.join(globalWorkPath, "work_week_throughtput_11_oclock.csv")
throughputWrite(workElevenOclockWorstRoad, workElevenOClockVehicleNumberPerS,path)

#Festive Week

#Access Point 3 oClock
path = os.path.join(globalFestivePath, "festive_week_throughtput_3_oclock.csv")
throughputWrite(festiveTreeOclockWorstRoad, festiveTreeOclockVehicleNumberPerS,path)

#Access Point 6 oClock
path = os.path.join(globalFestivePath, "festive_week_throughtput_6_oclock.csv")
throughputWrite(festiveSixOclockWorstRoad, festiveSixOclockVehicleNumberPerS,path)

#Access Point 11 oClock
path = os.path.join(globalFestivePath, "festive_week_throughtput_11_oclock.csv")
throughputWrite(festiveElevenOclockWorstRoad, festiveElevenOClockVehicleNumberPerS,path)

#Generate Work Week throughput plot
workMap, time = throughputPlot(globalWorkPath)
#Generate Festive Week throughput plot
festiveMap, time = throughputPlot(globalFestivePath)

for position in workMap:

	work = workMap[position]
	festive = festiveMap[position]

	if max(work) > max(festive):
		throughput = work
	else:
		throughput = festive

	if min(work) < min(festive):
		throughput = work
	else:
		throughput = festive

	preTitle = 'Throughput with 3 RSU - '

	if '11' in position:
		title = preTitle + "North West Access Point"
	elif '3' in position:
		title = preTitle + 'East Access Point'
	elif '6' in position:
		title = preTitle + 'South Access Point'


	figPath = os.path.join(os.getcwd(), title + '.png')

	if os.path.exists(figPath):
		os.remove(figPath)

	if max(throughput) > 20:
		yGranular = 2.0
	else:
		yGranular = 1.0

	fig = plt.figure()
	fig.suptitle(title)
	plt.xticks(np.arange(min(time), max(time)+1, 3.0))
	plt.yticks(np.arange(min(throughput), max(throughput)+1, yGranular))
	plt.xlabel('Time intervals of ' + str(interval) + ' minutes from 0:00 to 23.59')
	plt.ylabel('Throughput - Mbps')

	ax = fig.add_subplot(111)
	ax.grid(linestyle='--', linewidth=0.5)

	ax.plot(time, festive, 'r', label="Holidays")
	ax.plot(time, work, 'b', label="Weekdays")
	plt.legend()
	
	fig.savefig(figPath)

	plt.close(fig)