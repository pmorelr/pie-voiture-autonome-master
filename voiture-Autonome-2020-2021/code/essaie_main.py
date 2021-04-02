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
from evite_murs import *
from traitement import *
import time

import RPi.GPIO as GPIO

servo_pin = 18

#Ajuste estes valores para obter o intervalo completo do movimento do servo
deg_0_pulse   = 0.5 
deg_180_pulse = 2.5
f = 50.0

# Faca alguns calculos dos parametros da largura do pulso
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

#Iniciar o pino gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,f)
pwm.start(0)

duty = deg_0_duty + (90/180.0)* duty_range
pwm.ChangeDutyCycle(duty)

[positioninit, p2, orientationinit, o2, vinit, vi2, deltat,amaxlat,epsilonmax,amax,amin,tsb,l,larg,vmax,N,rv,m,alpha,lanti]=params()
alphainc=360/N

v=0 #vitesse a l instant present

tours_init=50
tours=2
limit_tour=10000

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
        map[min(int(X[j][1])-1,359)][1]=X[j][2]
    i+=1
    map=traitement(map)
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
        
        angle=thetacible*180/pi
        #print(map[int(angle)])
        #print(map[int(angle-10)])
        #print(map[int(angle+10)])
        angle=evite_coins(angle,35,200,map)
        angle=evite_murs(angle,200,map)
        obst=0
        obst=int(evite_obstacle(angle,M))
        
        if obst!=0:
            print("obstacle")
            for j in range(int(abs(angle)),179):
                M[obst*j][1]=100
                Mm1[obst*j][1]=100
            MMMR=zonesafe(M,rv,m)
            MMMRC=adaptevitesserelat (Mm1,M,MMMR,alpha,v,deltat,lanti)
            cible=trouvecible(MMMRC)
            xcible=cible[0]
            ycible=cible[1]
            thetacible=atan((ycible)/(xcible))
            if xcible<0:
                thetacible=pi+atan(ycible/xcible)
            angle=thetacible*180/pi
            if abs(angle)>25:
                angle+=-int(obst)*90
                
        
        #print(angle)
        print(angle)
        if not isnan(angle):
            print(map[int(angle)][1])
        
        angle=angle/abs(angle)*25*(1-exp(-angle*angle/800))
        
        angle_consigne=min(max(angle,-25),25)
        consigne=60*((angle_consigne+25)/50+1)

        duty = deg_0_duty + (consigne/180.0)* duty_range
        pwm.ChangeDutyCycle(duty)
        Mm1=M.copy()
        M=map.copy()
        data=[]
        compteur+=1
        if compteur>limit_tour:
            break

lidar.stop_motor()
lidar.reset()
lidar.disconnect()
