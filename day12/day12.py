# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 16:39:32 2021

@author: hongb
"""

import math
import numpy as np
from itertools import combinations
f = "input.txt"

lines = open(f)

luna = []

for l in lines:
    l = l.strip()
    moon = ""
    for char in l:
        if char in "-,0123456789":
            moon += char
            
    moon = list(map(int,moon.split(",")))
    luna.append(moon)

velo = [[0 for _ in range(len(luna[0]))] for __ in range(len(luna))]

moons = np.array(luna)


velocity = np.array(velo)



for _ in range(1000):    
    combos = combinations(range(4),2)
    for combo in combos:
        idx1, idx2 = combo
        moon1,moon2 = moons[idx1],moons[idx2]
        
        for dimension in range(3):
            if moon1[dimension] > moon2[dimension]:
                velocity[idx1][dimension] -= 1
                velocity[idx2][dimension] += 1
            elif moon1[dimension] < moon2[dimension]:
                velocity[idx1][dimension] += 1
                velocity[idx2][dimension] -= 1
                
    moons = moons + velocity
    
ans_moons = np.absolute(moons)
ans_velocity = np.absolute(velocity)
ans_moons = np.sum(ans_moons, axis=1)
ans_velocity = np.sum(ans_velocity, axis=1)

ans = ans_moons * ans_velocity
print(np.sum(ans))
#7098
moons2 = np.array(luna)
velocity2 = np.array(velo)

init_x = moons2[:,0]
init_y = moons2[:,1]
init_z = moons2[:,2]

velocity_checker = np.zeros(len(moons2))

found = [0,0,0]
cycle_len = [0,0,0]
counter = 0
while sum(found) != 3:    
    combos = combinations(range(4),2)
    for combo in combos:
        idx1, idx2 = combo
        moon1,moon2 = moons2[idx1],moons2[idx2]
        
        for dimension in range(3):
            if moon1[dimension] > moon2[dimension]:
                velocity2[idx1][dimension] -= 1
                velocity2[idx2][dimension] += 1
            elif moon1[dimension] < moon2[dimension]:
                velocity2[idx1][dimension] += 1
                velocity2[idx2][dimension] -= 1
                
    moons2 = moons2 + velocity2
    counter += 1
    if found[0] == 0:
        x_slice = moons2[:,0]
        vx_slice = velocity2[:,0]
        
        if np.array_equal(x_slice, init_x) and np.array_equal(vx_slice, velocity_checker):
            found[0] = 1
            cycle_len[0] = counter
        
    if found[1] == 0:
        y_slice = moons2[:,1]
        vy_slice = velocity2[:,1]
        
        if np.array_equal(y_slice, init_y) and np.array_equal(vy_slice, velocity_checker):
            found[1] = 1
            cycle_len[1] = counter
            
    if found[2] == 0:
        z_slice = moons2[:,2]
        vz_slice = velocity2[:,2]
        
        if np.array_equal(z_slice, init_z) and np.array_equal(vz_slice, velocity_checker):
            found[2] = 1
            cycle_len[2] = counter
            
a,b,c = cycle_len


tmp = a * b // math.gcd(a,b)
print(tmp * c // math.gcd(tmp,c))