# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:13:18 2021

@author: hongb
"""
import copy
def make_stuff(storage, equations, target, quantity):

    if target == 'ORE':
        storage[target] += quantity
        return storage
    
    
    
    if quantity > storage[target]:

        n_needed = quantity - storage[target]
        n_equations = (n_needed - 1)// equations[target][0] + 1
        
        for ingredient in equations[target][1]:
            storage = make_stuff(storage, equations, ingredient,n_equations * equations[target][1][ingredient])

        storage[target] += n_equations * equations[target][0]
    storage[target] -= quantity
    return(storage)



def parse_equation(line):
    return line.split(", ")

def parse_element(line):
    value, ingredient = line.split(" ")
    return int(value), ingredient

f = "input.txt"

lines = open(f)

equations = dict()
storage = dict()
storage['ORE'] = 0

for l in lines:
    ingredients, product = l.strip().split(" => ")
    
    
    
    val, name = parse_element(product)
    storage[name] = 0
    equations[name] = [val, dict()]
    
    left_ele = parse_equation(ingredients)
    
    for ele in left_ele:
        
        val, i_name = parse_element(ele)
        equations[name][1][i_name] = val
        
make_stuff(storage, equations,'FUEL',1)
print(storage['ORE'])
#337075
ans = 1

approx = 1000000000000//storage['ORE']
step_size = approx // 2


while step_size > 1:
    tmp = copy.deepcopy(storage)
    tmp = make_stuff(tmp, equations,'FUEL',step_size)
    
    if tmp['ORE'] < 1000000000000:
        storage = tmp
        ans += step_size
    else:
        step_size //= 2
        
print(ans)

        

