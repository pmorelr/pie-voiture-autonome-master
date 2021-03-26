import math as m

def evite_coins(angle_cible,eps,larg,map):
	ecart=1000
	if m.isnan(angle_cible):
		return angle_cible
	if min(map[int(angle_cible)-eps][1],map[int(angle_cible)-eps][1])>1000:
		eps=15
	#if abs(map[int(angle_cible)-eps][1]-map[int(angle_cible)+eps][1])<1000:
	#	print("c")
	#	return angle_cible
	if map[int(angle_cible)-eps][1]<map[int(angle_cible)][1]-1000:
		#return angle_cible+m.atan(larg/map[int(angle_cible)-eps][1])
		if map[int(angle_cible)-eps][1]<1000:
			return angle_cible+20
		else:
			return angle_cible+5
	if map[int(angle_cible)+eps][1]<map[int(angle_cible)][1]-1000:
		#return angle_cible-m.atan(larg/map[int(angle_cible)+eps][1])
		if map[int(angle_cible)+eps][1]<1000:
			return angle_cible-20
		else:
			return angle_cible-5
	return angle_cible
	
def evite_murs(angle_cible,delta,map):
	c=0
	for i in range(1,60):
		if map[i][1]<delta:
			c+=1
		if c>5:
			print("mur")
			return -45
		if map[-i][1]<delta:
			c-=1
		if c<-5:
			print("mur")
			return 45
	return angle_cible

def evite_obstacle(angle_cible,map):
	if m.isnan(angle_cible):
		return 0
	if abs(angle_cible)>45:
		signe=int(int(angle_cible)/int(abs(angle_cible)))
		c=0
		for i in range(25,int(abs(angle_cible))):
			if map[signe*i][1]<400:
				c+=1
		if c>10:
			return signe*1
	return 0
			
