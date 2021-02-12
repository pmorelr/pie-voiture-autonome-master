import numpy as np
import copy
from zonesafe import *
from adaptevitesserelat import *
from trouvecible import *
from environment import *
from lidar import *
from actualise import *
from actualise2 import *
from params import *
from calculrayoncourbure import *
from math import *
from objectif import *
from lecture_lidar import *
from rplidar import RPLidar
from init_lidar import *
import time

[positioninit, p2, orientationinit, o2, vinit, vi2, deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
alphainc=360/N

v=0 #vitesse a l instant present

tours_init=50
tours=4
limit_tour=100

lidar = RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.connect()

time.sleep(2)

data=[]
map=[[i,1000] for i in range(360)]

compteur=0
i=0
for scan in lidar.iter_scans(500,10):
    data.append(np.array(scan))
    X=data[-1]
    for j in range(len(X)):
        map[int(X[j][1])-1][1]=X[j][2]
    i+=1
    if i>tours_init:
        Mm1=map.copy()
        M=map.copy()
    if i>tours_init+1 and i%tours==0:
        MMMR=zonesafe(M,rv,m)

        MMMRC=adaptevitesserelat (Mm1,M,MMMR,alpha,v,deltat,lanti)
        cible=trouvecible(MMMRC)
    #obj=objectif(cible,v,deltat)
    #R=calculrayoncourbure(obj)
        xcible=cible[0]
        ycible=cible[1]
        thetacible=atan((ycible)/(xcible))
        if xcible<0:
            thetacible=pi+atan(ycible/xcible)

        print(thetacible*180/pi)
        Mm1=M.copy()
        M=map.copy()
        data=[]
        compteur+=1
        if compteur>limit_tour:
            break

lidar.stop_motor()
lidar.reset()
lidar.disconnect()
