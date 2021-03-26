from math import *
import copy

def zonesafe (M,rv,m):
    
    N=len(M)
    A=copy.deepcopy(M[0:int(N/4)])
    B=copy.deepcopy(M[int(3*N/4):N])
    A.reverse()
    B.reverse()
    MR=copy.deepcopy(A+B) #deepcopy
    MMR=[]
    i=0
    alphainc=360/N #valeur d'un increment d'angle
    while i<len(MR):
        theta=MR[i][0]
        r=MR[i][1]
        xi=r*cos(theta*alphainc*2*pi/360)
        yi=r*sin(theta*alphainc*2*pi/360)
        MMR.append([theta,r,xi,yi])
        i=i+1
        
    
    MMMR=[] 
    i=1
    while i<(len(MMR)-1):
        xim1=MMR[i-1][2] #abscisse du pt (i moins 1)
        yim1=MMR[i-1][3]
        xi=MMR[i][2]
        yi=MMR[i][3]
        xip1=MMR[i+1][2]
        yip1=MMR[i+1][3]
        
        if abs(yip1-yim1)>0.00001:
            K=-(xip1-xim1)/(yip1-yim1) #coeff dir de la droite orthogonale au bord du circuit au pt i d'equation y=Kx+C
            C=yi-K*xi 
        
            xp1=xi+(rv+m)/sqrt(1+K**2) 
            yp1=yi+K*(rv+m)/sqrt(1+K**2)
        #abscisse et ordonnee du pt sur la droite ortho au bord du circuit au pt i distant de rv+m du pt i du cote 1
        
            xp2=xi-(rv+m)/sqrt(1+K**2)
            yp2=yi-K*(rv+m)/sqrt(1+K**2)
        #abscisse et ordonnee du pt sur la droite ortho au bord du circuit au pt i distant de rv+m du pt i du cote 2
        if abs(yip1-yim1)<0.00001:
            yp1=yi+rv+m
            yp2=yi-(rv+m)
            xp1=xi
            xp2=xi
            
        d1=(xp1)**2+(yp1)**2
        d2=(xp2)**2+(yp2)**2
        liste1=MMR[i]+[xp1,yp1]
        liste2=MMR[i]+[xp2,yp2]
        
        
            
        if d1<=d2:
            MMMR.append(liste1)
        if d1>d2:
            MMMR.append(liste2)
        
        i=i+1
    
    return(MMMR)
    
    
    
    
