import math as ma

def cone_obs(map):
    
    LARGEUR_VOITURE = 200
    new_map = []

    for i in range(len(map)):

        angle = 2*ma.arctan(LARGEUR_VOITURE/map[i][1])
        
        # Recherche distance minimum (du point le plus proche du lidar) dans le cône d'angle 'angle'
        min = 1000000000
        for j in range(i-angle//2, i+angle//2):
            j = j%360
            if (map[j][1]<min):
                min = map[j][1]

        new_map[i][0], new_map[i][1] = map[i][0], min

    return new_map
