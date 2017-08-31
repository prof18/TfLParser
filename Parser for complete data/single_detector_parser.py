'''
This parser select only certain detectors. This parser can be used the select only certain detector. 
It generates a folder for each main detector (e.g. 01-142) that contains the detailed file for each road detector (e.g. 01-142u and 01-142w)
'''
import pandas as pd
import os
import time

days = [name for name in os.listdir(os.getcwd()) if os.path.isdir(name)]

#This is necessaty to open the detector main file
selected_detectors_base = ['01-157','01-585','01-223','01-233','01-204','01-139','01-276','01-142','01-143','01-140','01-235','01-237', '01-557','01-556','01-158',
'01-232','01-159','01-229','01-437','01-222','01-307','01-160','01-230','01-161','01-353','01-162','01-294','01-228']

selected_detectors = ['01/585a1','01/223c1','01/233b1','01/585b1','01/233a1','01/233x1','01/233d1','01/204k1','01/204k2','01/139h1',
'01/139h2','01/140t1','01/140t2', '01/276c1','01/276c2','01/142w1','01/142w2','01/143c1','01/143c2','01/143r1','01/204l2','01/204l1','01/139f2','01/139f1','01/140s2',
'01/140s1','01/276h2','01/276h1','01/142u1','01/142u2','01/235a1','01/237a1', '01/557b1','01/556a1','01/237c1','01/157g1','01/158k1','01/232s1','01/232t1','01/159w1',
'01/159w2','01/143a1','01/143a2','01/229s1','01/229q1','01/229d1','01/437c1','01/222a1','01/307e1','01/160a1','01/307g2','01/307g1','01/229c1','01/223d1','01/223b1',
'01/235h1', '01/235e1', '01/230c1', '01/160d1', '01/161e1','01/160c1','01/160c2','01/353j1','01/161g1','01/162a1','01/353m1','01/162c1','01/294h1','01/229b1',
'01/228d1']

for day in days :
    path = os.path.join(os.getcwd(), day)
    print path

    for file in os.listdir(path):
        #enter in the detector main file
        if file[:6] in selected_detectors_base:
            path1 = os.path.join(path,file)
            
            if os.path.exists(path1):

                df = pd.read_csv(path1, sep='|', header=None)
                data = df.values
                start_time = time.time()

                #iterate in the file
                for i in range(0, data.shape[0]):
                    if i == 0:
                        fileName = file[:6]
                        newdir = os.path.join(path, fileName)
                        os.mkdir(newdir)
                    status = data[i, 4]
                    #we keep the data only if the data is correctly measured
                    if status == 1:
                        id = data[i, 0]
                        junction = id[:7]
                        junction2 = id[:8]
                    
                        if junction2 in selected_detectors:

                            junction2 = junction.replace("/", "-")
                            dir = os.path.join(newdir, junction2 + ".csv")
                            toWrite = ''
                            for j in range(0, data.shape[1]):
                                if id[:7] == junction:
                                    if j == data.shape[1] - 1:
                                        toWrite += str(data[i, j])
                                    else:
                                        toWrite = toWrite + str(data[i, j]) + '|'

                            f = open(dir, "a")
                            f.write(toWrite + '\n')
                            f.close()

            print('Parsed:' + path1);
           
