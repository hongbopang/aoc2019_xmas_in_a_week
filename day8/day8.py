# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:05:30 2021

@author: hongb
"""


f = "input.txt"

lines = open(f)

for l in lines:
    image = l.strip()
    
layer_size = 25 * 6

startptr = 0
endptr = layer_size    
images = []
sorter = []

while startptr < len(image):
    tmp = [0,0,0]
    layer = image[startptr:endptr]
    images.append(layer)
    for i in layer:
        tmp[int(i)] += 1
    sorter.append(tuple(tmp))
    
    startptr += layer_size
    endptr += layer_size
    

sorter.sort()

print(sorter[0][1] * sorter[0][2])
#1690

final_image = [[-1 for _ in range(25)] for __ in range(6)]

for r in range(6):
    for c in range(25):
        layer_id = 0

        while images[layer_id][r*25+c] == "2":
            layer_id +=1
        if images[layer_id][r*25+c] == "0":
            
            final_image[r][c] = " "
        else:
            final_image[r][c] = "O"
for row in final_image:
    print(row)
    
#ZPZUB