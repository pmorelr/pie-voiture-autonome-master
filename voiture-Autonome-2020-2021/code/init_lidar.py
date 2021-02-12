import sys
import numpy as np
from rplidar import RPLidar

def init_lidar(tour,lidar):
    data=[]
    map=[[i,1000] for i in range(360)]

    i=0
    for scan in lidar.iter_scans(500,10):
        data.append(np.array(scan))
        X=data[-1]
        for j in range(len(X)):
            map[int(X[j][1])-1][1]=X[j][2]
        i+=1
        if i>tour:
            lidar.reset()
            return(map)

    return(map)
