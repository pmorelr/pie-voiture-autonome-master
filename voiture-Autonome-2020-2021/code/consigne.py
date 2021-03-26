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
    
    angle=thetacible*180/pi

    print(angle)
    if angle>15:
        duty = deg_0_duty + (110/180.0)* duty_range
        pwm.ChangeDutyCycle(duty)
    elif angle<-15:
        duty = deg_0_duty + (70/180.0)* duty_range
        pwm.ChangeDutyCycle(duty)
    else:
        duty = deg_0_duty + (90/180.0)* duty_range
        pwm.ChangeDutyCycle(duty)
        
    Mm1=M.copy()
    time.sleep(0.7)
    lidar = RPLidar('/dev/ttyUSB0')
    M=lecture_lidar(4,Mm1,lidar)
    k+=1

lidar.stop_motor()
lidar.disconnect()


#return(thetaRoues)
