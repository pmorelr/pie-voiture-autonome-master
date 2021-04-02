def traitement(map):
	
	n=len(map)
	for i in range(n):
		map[i][1]=(map[i-2][1]+map[i-1][1]+map[i][1]+map[(i+1)%n][1]+map[(i+2)%n][1])/5
	return map
