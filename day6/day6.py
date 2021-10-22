# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 12:25:39 2021

@author: hongb
"""


f = "input.txt"

lines = open(f)

levels = dict()
orbits = dict()
inverted = dict()
levels["COM"] = 0

for l in lines:
    parent, orbiter = l.strip().split(")")
    if parent not in orbits:
        orbits[parent] = []
    orbits[parent].append(orbiter)
    inverted[orbiter] = parent
to_search = ["COM"]
ans = 0


while len(to_search) != 0:    
    me = to_search.pop(0)  
    
    if me not in orbits:
        continue
    
    level = levels[me]
    
    
    
    orbiters = orbits[me]
    for child in orbiters:
        levels[child] = level + 1
        ans += level +1
        to_search.append(child)
        
print(ans)
#200001

start = "YOU"
end = "SAN"

target1 = inverted[start]
target2 = inverted[end]
my_path = dict()
path = 0
path2 = 0
while target1 != "COM":
    my_path[target1] = path
    path += 1
    target1 = inverted[target1]
    
    
while target2 != "COM":
    if target2 in my_path:
        print(path2+my_path[target2])
        break
    else:
        target2 = inverted[target2]
        path2 += 1
#379