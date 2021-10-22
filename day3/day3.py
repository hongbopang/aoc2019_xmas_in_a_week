# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:10:45 2021

@author: hongb
"""

def wire1_reader( pos, wire_dict,steps, wire1_steps, instrc):
    direction = instrc[0]
    moves = int(instrc[1:])
    
    if direction == "U":
        idx = 1
        multiplier = 1
        
    if direction == "D":
        idx = 1
        multiplier = -1
        
    if direction == "L":
        idx = 0
        multiplier = -1
        
    if direction == "R":
        idx = 0
        multiplier = 1
    
    new_locations = list(pos)    

    for i in range(moves):
        new_locations[idx] += multiplier
        tmp = tuple(new_locations)
        wire_dict[tmp] = abs(new_locations[0]) + abs(new_locations[1])
        steps += 1 #part2
        if tmp not in wire1_steps: #part2
            wire1_steps[tmp] = steps
    return tuple(new_locations), wire_dict, steps, wire1_steps

def wire2_reader(pos, wire_dict, steps, wire1_steps, instrc):
    direction = instrc[0]
    moves = int(instrc[1:])
    
    if direction == "U":
        idx = 1
        multiplier = 1
        
    if direction == "D":
        idx = 1
        multiplier = -1
        
    if direction == "L":
        idx = 0
        multiplier = -1
        
    if direction == "R":
        idx = 0
        multiplier = 1
    
    new_locations = list(pos)
    
    
    ans1 = -1
    ans2 = -1
    for i in range(moves):
        new_locations[idx] += multiplier
        tmp = tuple(new_locations)
        steps += 1 #part2
        if tmp in wire_dict:
            if ans1 == -1:
                ans1 = wire_dict[tmp]
                ans2 = wire1_steps[tmp] + steps #part2
            else:
                ans1 = min(wire_dict[tmp], ans1)
                ans2 = min(ans2, wire1_steps[tmp] + steps) #part2
    return tmp, ans1, steps, ans2
    
f = "input.txt"
lines = open(f)

wires = []

for l in lines:
    wires.append(l.strip().split(","))
    
wire1_dict = dict()
pos = (0,0)

#part2
wire1_steps = dict()
steps = 0


for instrc in wires[0]:
    pos, wire1_dict, steps, wire1_steps = wire1_reader(pos, wire1_dict, steps, wire1_steps, instrc)
    
ans1 = float('inf')
pos = (0,0)

#part2
steps = 0
ans2 = float('inf')


for instrc in wires[1]:
    pos, meeting, steps, distance = wire2_reader(pos, wire1_dict,  steps, wire1_steps,instrc)

    if meeting != -1:
        ans1 = min(meeting, ans1)
        ans2 = min(distance, ans2) #part2
print(ans1)
#308
print(ans2)
#12934
