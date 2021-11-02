# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:58:43 2021

@author: hongb
"""

import numpy as np
f = "input.txt"

lines = open(f)

for l in lines:
    l=l.strip()
    numbers = list(map(int,list(l)))
    
org_num = [i for i in numbers]
numbers = np.array(numbers)

offset = int(''.join(list(map(str,numbers[:7]))))

n_digits = len(numbers)

pattern = [0,1,0,-1]

patterns = [[0 for _ in range(n_digits)] for __ in range(n_digits)]


for i in range(n_digits):
    base_pattern = []

        
    for k in [0,1,0,-1]:
        for j in range(i+1):
            base_pattern.append(k)


    while len(base_pattern) < n_digits + 1:
        base_pattern = base_pattern + base_pattern
        
    base_pattern = base_pattern[1:n_digits+1]
    
    patterns[i] = [l for l in base_pattern]
    
A = np.array(patterns)
A = np.transpose(A)

for _ in range(100):
    numbers = abs(np.matmul(numbers,A)) % 10
    
print(''.join(list(map(str,numbers[:8]))))
#11833188

signal = []
digits_to_care = len(numbers) * 10000 - offset
while len(signal) < digits_to_care:
    signal += org_num
    
excess = len(signal) - digits_to_care

signal_to_work_on = signal[excess:]

for _ in range(100):
    tmp = [0 for _ in range(len(signal_to_work_on))]
    tmp[-1] = signal_to_work_on[-1]
    for i in range(len(signal_to_work_on)-2,-1,-1):
        tmp[i] = abs(tmp[i+1] + signal_to_work_on[i]) % 10
    signal_to_work_on = tmp
print(signal_to_work_on[:8])    
#55005000    
