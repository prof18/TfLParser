'''
This parser generates the plot of the inter-arrival times of all the detectors
'''
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

weeks = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

interval = input("Time Interval in minutes. Same of the single interval interarrival_time: ")

for week in weeks:
	if 'Interarrival' in week:
		path = os.path.join(os.getcwd(), week)
		print 'Analyzing: ' + path
		for file in os.listdir(path):

			if 'png' not in file:
				path2 = os.path.join(path, file)

				if os.path.exists(path2):
					df = pd.read_csv(path2, sep='|', header=None)
					data = df.values
					time = list(range(data.shape[0]))
					interarrival_time = []
					for i in range (0, data.shape[0]):
						start_time = data[i,0]
						end_time = data[i,1]
						interarrival_time.append(data[i,2])

				if 'festive' in file:
					title = 'Festive Week - Detector: ' + file[-11:-4]
				else:
					title = 'Work Week - Detector: ' + file

				figPath = os.path.join(path, title + '.png')

				if os.path.exists(figPath):
					os.remove(figPath)
					
				if max(interarrival_time) > 300:
					yGranular = 30.0
				elif max(interarrival_time) > 200:
					yGranular = 20.0
				elif max(interarrival_time) > 100:
					yGranular = 10.0
				elif max(interarrival_time) > 50:
					yGranular = 5.0
				else:
					yGranular = 3.0

				fig = plt.figure()
				fig.suptitle(title)
				plt.xticks(np.arange(min(time), max(time)+1, 3.0))
				plt.yticks(np.arange(min(interarrival_time), max(interarrival_time)+1, yGranular))
				plt.xlabel('Time intervals of ' + str(interval) + ' minutes from 0:00 to 23.59')
				plt.ylabel('Vehicle interarrival_time')

				ax = fig.add_subplot(111)
				ax.grid(linestyle='--', linewidth=0.5)
				ax.plot(time, interarrival_time)
				fig.savefig(figPath)
				plt.close(fig)