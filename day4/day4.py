# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:35:40 2021

@author: hongb
"""

def get_next_candidate(start):
    me = [i for i in start]
    if me[-1] != 9:
        me[-1] += 1
        return me    
    else:
        tmp = get_next_candidate(me[:-1]) 
        return tmp + [tmp[-1]]
    

f = "input.txt"
lines = open(f)

for l in lines:
    possible_range = list(l.strip().split("-"))    
#we can immediately see that 111111 must be the actual smallest password that can be viable, otherwise the decreasing rule will be broken
    
start = [int(i) for i in possible_range[0]]

end =  [int(i) for i in possible_range[1]] 
prev = start[0]

for i in range(1, len(start)):
    if start[i] < prev:
        for j in range(i, len(start)):
            start[j] = prev
        break
    else:
        prev = start[i]
        
        
start2 = [i for i in start] #part2  

ans = 0
while start < end:
    for i in range(1, len(start)):
        if start[i-1] == start[i]:
            ans += 1

            break
    start = get_next_candidate(start)
    
print(ans)
#2814

ans2 = 0
while start2 < end:
    a,b,c,d,e,f = start2
    if (a == b and a != c) or (b == c and a != b and c != d) or (c == d and b != c and d != e) or (d == e and c != d and e != f) or (e == f and d != e):
        ans2 += 1    
        
    start2 = get_next_candidate(start2)
    
print(ans2)
#1991