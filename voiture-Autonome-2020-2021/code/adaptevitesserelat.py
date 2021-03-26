from math import *
import copy


def adaptevitesserelat (Mm1,M,MMMR,alpha,v,deltat,rmax):
    

    mmmr=[]
    mmmrc=[]
    MMMRC=copy.deepcopy(MMMR)
    NNN=len(MMMR)
    i=0
    N=len(M)
    while i<NNN:
        if (MMMR[i][0]*360/N)<alpha:
            mmmr.append(MMMR[i])
        i+=1
    i=0
    while i<NNN:
        if (MMMR[i][0]*360/N)>(360-alpha):
            mmmr.append(MMMR[i])
        i+=1
    i=0
    nnn=len(mmmr)
    while i<nnn:
        theta=mmmr[i][0]
        theta=int(theta)
        vrel=(M[theta][1]-Mm1[int((acos(v*deltat/M[theta][1]/(1-cos(theta*2*pi/360)/max(sin(theta*2*pi/360),0.01))))*360/(2*pi))][1])/deltat #approx de la derivee de la distance a l'objet par rapport au temps"   ATTENTION REMPLACER (orientation-orientationm1) par les donnees de l'accelerometre dorientation/dt*deltat
        
        thetap=atan(mmmr[i][5]/mmmr[i][4]) #angle de coordonnees polaires du pt p attention c'est bien en angle cette fois"
        rp=sqrt(mmmr[i][5]**2+mmmr[i][4]**2) #rayon de coordonnees polaires du pt p"
        if vrel<0:
            rpprim=min(rp*v*cos(thetap)/(-vrel),rmax) #adaptation du rayon en fonction de la vitesse relative a la voituredu point qu'il designe"
            #on pourrait modifier le ryon en prenant aussi compte de l'acceleration relative!
        if vrel>=0:
            rp=sqrt(mmmr[i][5]**2+mmmr[i][4]**2)
            rpprim=rmax+rp
        xpprim=rpprim*cos(thetap)
        ypprim=rpprim*sin(thetap)
            
        
            
        mmmrc.append((mmmr[i]+[xpprim,ypprim]))
        i+=1
    i=0
    
    while i<len(mmmrc):
        j=0
        while j<NNN:
            if mmmrc[i][0]==MMMRC[j][0]:
                MMMRC[j][4]=mmmrc[i][6]
                MMMRC[j][5]=mmmrc[i][7]
            j+=1
        i+=1
    
    return(MMMRC)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
        