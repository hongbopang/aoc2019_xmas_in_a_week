# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 09:54:29 2021

@author: hongb
"""


class opcode_machine:
    def __init__(self, opcode):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.halt = False
    def modify(self, pos, val):
        self.seq[pos] = val
        
    def read_once(self):
        instruction = self.seq[self.ptr]
        
        if instruction == 1:
            self.opcode_1()
        elif instruction == 2:
            self.opcode_2()
        elif instruction == 99:
            self.opcode_terminate()
            
    def opcode_1(self):
        pos1 = self.seq[self.ptr+1]
        pos2 = self.seq[self.ptr+2]
        pos3 = self.seq[self.ptr+3]
        
        
        num1 = self.seq[pos1]
        num2 = self.seq[pos2]
        self.seq[pos3] = num1 + num2
        
        
        self.ptr += 4
        
    def opcode_2(self):
        pos1 = self.seq[self.ptr+1]
        pos2 = self.seq[self.ptr+2]
        pos3 = self.seq[self.ptr+3]
        
        
        num1 = self.seq[pos1]
        num2 = self.seq[pos2]
        self.seq[pos3] = num1 * num2
        
        
        self.ptr += 4
    def opcode_terminate(self):
        self.halt = True
        
        
f = "input.txt"

lines = open(f)

for l in lines:
    opcode = list(map(int,l.strip().split(",")))

machine = opcode_machine(opcode)
machine.modify(1,12)
machine.modify(2,2)

while not machine.halt:
    machine.read_once()

#3562624
print(machine.seq[0])

for noun in range(100):    
    for verb in range(100):
        tmp_machine = opcode_machine(opcode)
        tmp_machine.modify(1,noun)
        tmp_machine.modify(2,verb)
        while not tmp_machine.halt:
            tmp_machine.read_once()
        if tmp_machine.seq[0] == 19690720:
            print(100*noun + verb)
            #8298
            break




