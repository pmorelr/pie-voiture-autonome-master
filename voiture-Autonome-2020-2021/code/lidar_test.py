from rplidar import RPLidar
from init_lidar import *
from lecture_lidar import *
import time

k=0

while k<10:
    t=time.time()
    lidar = RPLidar('/dev/ttyUSB0')
    map=[[i,1000] for i in range(360)]
    M=lecture_lidar(4,map,lidar)
    #lidar.clear_input()
    print(time.time()-t)
    time.sleep(0.7)
    k+=1
