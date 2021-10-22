# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:33:00 2021

@author: hongb
"""
import math
def get_defining_angle(loc1, loc2):
    x1,y1 = loc1
    x2,y2 = loc2
    
    if x1 == x2:
        if y1 > y2:
            return (float('inf'), 1)
        else:
            return (float('inf'), -1)
    
    gradient = (y2 - y1) / (x2 - x1)
    
    if y1 > y2:
        return (gradient, 1)
    elif y2 > y1:
        return (gradient, -1)
    else:
        if x1> x2:
            return (gradient, 1)
        else:
            return (gradient, -1)
        
def get_characteristic_angle(me, them):
    y1,x1 = me
    y2,x2 = them
    
    if x1 == x2:
        if y2 < y1:
            return 0
        else:
            return math.pi
    elif y1 == y2:
        if x2 - x1 < 0:
             return math.pi/2
        else:
             return 3*math.pi/2
    else:
        deltay = y2 - y1
        deltax = x2 - x1
        angle = math.atan(abs(deltay/deltax))
        
        if deltax > 0 and deltay > 0:

            return math.pi/2 - angle
        if deltax > 0 and deltay < 0:
            return math.pi/2 + angle
        if deltax < 0 and deltay > 0:
            return 3 * math.pi / 2 - angle
        return 3 * math.pi / 2 + angle
    

f = "input.txt"
lines = open(f)

image = []

for l in lines:
    l = l.strip()
    tmp = [i for i in l]
    image.append(tmp)
    
locations = dict()

for r in range(len(image)):
    for c in range(len(image[0])):
        if image[r][c] == "#":
            locations[(r,c)] = dict()
            
ans = 0
loc = (0,0)

for me in locations:
    for them in locations:
        if me != them:
            signature = get_defining_angle(me, them)
            locations[me][signature] = 1
    if len(locations[me]) > ans:
        ans = len(locations[me])
        loc = me

            
print(ans)
#256
      
del locations[loc]

keys = []
angles = dict()

for them in locations:
    angle = get_characteristic_angle(loc, them)
    if angle not in angles:
        angles[angle] = []
        keys.append(angle)
    distance = abs(loc[0]  - them[0]) + abs(loc[1]- them[1])
    angles[angle].append((distance, them))
    
for angle in angles:
    angles[angle].sort()
    
keys.sort()

ptr = 0

for _ in range(200):    
    while len(angles[keys[ptr]]) == 0:
        ptr = (ptr + 1) % len(keys)

    me = angles[keys[ptr]].pop(0)
    ptr = (ptr + 1) % len(keys)
rows = len(image)  
cols = len(image[0])  

print(me[1][1]*100 +me[1][0])
#1707