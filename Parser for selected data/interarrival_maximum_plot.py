'''
This parser generates the plot of the maximum inter-arrival time between all the detectors
'''
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

interval = input("Time Interval in minutes. Same of the single interval interarrivalS: ")

sizeInterval = (24*60)/interval

#Function that generates the set of inter-arrival times
def maximumInterArrivalPlot(path):

	interarrivalS = [0 for x in range(sizeInterval)]

	for file in os.listdir(path):

		if 'png' not in file:

			path2 = os.path.join(path, file)

			if os.path.exists(path2):
				df = pd.read_csv(path2, sep='|', header=None)
				data = df.values
				for i in range(0, data.shape[0]):
					if data[i,2] > interarrivalS[i]:
						interarrivalS[i] = data[i,2]

	return interarrivalS

#Main Program
weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

for week in weeks:
	if 'Festive Week Interarrival' in week:
		path = os.path.join(os.getcwd(), week)
		print 'Analyzing: ' + path
		festive = maximumInterArrivalPlot(path)

	elif 'Work Week Interarrival' in week:
		path = os.path.join(os.getcwd(), week)
		print 'Analyzing: ' + path
		work = maximumInterArrivalPlot(path) 
		
title = 'Maximum Inter-arrival Time'

figPath = os.path.join(os.getcwd(), title + '.png')

if os.path.exists(figPath):
	os.remove(figPath)

if max(work) > max(festive):
	interarrivalS = work
else:
	interarrivalS = festive

if min(work) < min(festive):
	interarrivalS = work
else:
	interarrivalS = festive
	
if max(interarrivalS) > 300:
	yGranular = 30.0
elif max(interarrivalS) > 100:
	yGranular = 20.0
elif max(interarrivalS) > 50:
	yGranular = 10.0
elif max(interarrivalS) > 20:
	yGranular = 5.0
else:
	yGranular = 3.0

time = list(range(sizeInterval))

fig = plt.figure()
fig.suptitle(title)
plt.xticks(np.arange(min(time), max(time)+1, 3.0))
plt.yticks(np.arange(min(interarrivalS), max(interarrivalS)+1, yGranular))
plt.xlabel('Time intervals of ' + str(interval) + ' minutes from 0:00 to 23.59')
plt.ylabel('Vehicle interarrival Time - seconds')

ax = fig.add_subplot(111)
ax.grid(linestyle='--', linewidth=0.5)

ax.plot(time, festive, 'r', label="Holidays")
ax.plot(time, work, 'b', label="Weekdays")
plt.legend()

fig.savefig(figPath)

plt.close(fig)