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

#débloquer lidar : sudo chmod 666 /dev/ttyUSB0

#def ConsigneRoues(Mm1,Vm1):

    #Mm1 et Vm1 sont la sortie lidar et la vitesse a l instant d avant


[positioninit, p2, orientationinit, o2, vinit, vi2, deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
alphainc=360/N

v=0 #vitesse a l instant present

lidar = RPLidar('/dev/ttyUSB0')
lidar.start_motor()
lidar.connect()

time.sleep(2)

Mm1=init_lidar(50,lidar)
#M=lecture_lidar(4,Mm1,lidar)
M=Mm1.copy()

k=0
while k<20:
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
    time.sleep(0.7)
    lidar = RPLidar('/dev/ttyUSB0')
    M=lecture_lidar(4,Mm1,lidar)
    k+=1

lidar.stop_motor()
lidar.disconnect()


#return(thetaRoues)
