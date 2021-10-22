# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:41:36 2021

@author: hongb
"""
def calc_fuel(weight):
    return weight // 3 - 2


def recur_fuel(weight):
    ans = 0
    tmp = max(0,weight // 3 - 2)
    ans += tmp
    
    if tmp > 2:
        ans += recur_fuel(tmp)
    return ans
    
f = "input.txt"

lines = open(f)
ans = 0
ans2 = 0

for l in lines:
    ans += calc_fuel(int(l))
    ans2 += recur_fuel(int(l))
    
print(ans)
#3210097

print(ans2)
#4812287


print(recur_fuel(1969))