# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 16:01:59 2021

@author: hongb
"""


class opcode_machine:
    def __init__(self, opcode):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.seq +=  [0 for _ in range(1000)]
        self.halt = False
        self.pause = False
        self.input = []
        self.output = []
        self.base = 0
        #robot specific
        self.row = 0
        self.col = 0
        self.direction = 0
        self.directions = [[-1,0],[0,1],[1,0],[0,-1]]
        self.color_memory = dict()
        
    def add_input(self, input_val):
        self.input.append(input_val)

    def modify(self, pos, val):
        self.seq[pos] = val
        
    def color(self, paint):
        self.color_memory[(self.row, self.col)] = paint
        
    def move(self, direction):
        if direction == 0:
            adj = -1
        else:
            adj = 1
        self.direction = (self.direction + adj) % 4
        dr,dc = self.directions[self.direction]
        self.row += dr
        self.col += dc
    
    def run_machine(self):
        pos = (self.row, self.col)
        if pos in self.color_memory:
            self.add_input(self.color_memory[pos])
        else:
            self.add_input(0)
        while 1: 
            self.read_once()
            if self.pause:
                return self.output, False
            if self.halt:
                return self.output, True

        
    def decode(self, ins):
        major_code = 0
        parameters = None
        if ins == "99":
            return 99, None
        
        #3 parameters
        
        if ins[-1] == "1" or ins[-1] == "2" or ins[-1] == "7" or ins[-1] == "8":
            major_code = int(ins[-1])
            
            if len(ins) < 5:
                ins = "0" * (5-len(ins)) + ins
            parameters = []
            for i in ins[:3]:
                parameters.append(int(i))
            parameters = parameters[::-1]
            
            locations = [0,0,0]
            for j in range(3):
                adjuster = j + 1
                if parameters[j] == 0:
                    locations[j] = self.seq[self.ptr+adjuster]
                elif parameters[j] == 1:
                    locations[j] = self.ptr+adjuster
                elif parameters[j] == 2:
                    locations[j] = self.seq[self.ptr+adjuster] + self.base
            
            
            
        #2 parameters    
        elif ins[-1] == "5" or ins[-1] == "6":
            major_code = int(ins[-1])
            
            if len(ins) < 4:
                ins = "0" * (4-len(ins)) + ins
            parameters = []
            for i in ins[:2]:
                parameters.append(int(i))
            parameters = parameters[::-1]
            locations = [0,0]
            for j in range(2):
                adjuster = j + 1
                if parameters[j] == 0:
                    locations[j] = self.seq[self.ptr+adjuster]
                elif parameters[j] == 1:
                    locations[j] = self.ptr+adjuster
                elif parameters[j] == 2:
                    locations[j] = self.seq[self.ptr+adjuster] + self.base
            
        #1 parameters       
        elif ins[-1] == "3" or ins[-1] == "4" or ins[-1] == "9":
            major_code = int(ins[-1])
            
            if len(ins) <= 2:
                parameters = 0
            else:
                parameters = int(ins[0])
            if parameters == 0:
                locations = [self.seq[self.ptr+1]]
            elif parameters == 1:
                locations = [self.ptr+1]
            elif parameters == 2:
                locations = [self.seq[self.ptr+1]+self.base]

                
        
        return major_code, locations
        
    def read_once(self):
        instruction = str(self.seq[self.ptr])

        major_code, locations = self.decode(instruction)

        

        if major_code == 99:
            self.opcode_terminate()
            return

        if major_code == 1:
            self.opcode_1(locations)
        elif major_code == 2:
            self.opcode_2(locations)
        elif major_code == 3:
            self.opcode_3(locations)
        elif major_code == 4:
            self.opcode_4(locations)      
        elif major_code == 5:
            self.opcode_5(locations)     
        elif major_code == 6:
            self.opcode_6(locations)     
        elif major_code == 7:
            self.opcode_7(locations)                 
        elif major_code == 8:
            self.opcode_8(locations)     
        elif major_code == 9:
            self.opcode_9(locations)   
            
    def opcode_1(self,parameters):
        loc1, loc2, loc3 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]
        
        self.seq[loc3] = num1 + num2              
        self.ptr += 4
        
    def opcode_2(self,parameters):
        loc1, loc2, loc3 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]
        
        self.seq[loc3] = num1 * num2              
        self.ptr += 4
        
        
        
    def opcode_3(self, parameters):
        loc1 = parameters[0]
        if len(self.input) == 0:
            self.pause = True
            return
        self.seq[loc1] = self.input.pop(0)        
        
        self.ptr += 2
        
    def opcode_4(self, parameters):
        loc1 = parameters[0]
        num1 = self.seq[loc1]
        
        self.output.append(num1)
        self.ptr += 2
        
        
        
    def opcode_5(self, parameters):
        loc1, loc2 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]
            
        if num1 != 0:
            self.ptr = num2
        else:
            self.ptr += 3
            
    def opcode_6(self, parameters):
        loc1, loc2 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]
            
        if num1 == 0:
            self.ptr = num2
        else:
            self.ptr += 3
            
    def opcode_7(self,parameters):
        loc1, loc2, loc3 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]            

        if num1 < num2:            
            self.seq[loc3] = 1
        else:
            self.seq[loc3] = 0
        self.ptr += 4
        
    def opcode_8(self,parameters):
        loc1, loc2, loc3 = parameters
        num1 = self.seq[loc1]
        num2 = self.seq[loc2]   

        if num1 == num2:            
            self.seq[loc3] = 1
        else:
            self.seq[loc3] = 0
        self.ptr += 4
        
    def opcode_9(self, parameters):
        loc1 = parameters[0]
        num1 = self.seq[loc1]      
            
 
        self.base += num1  
        
        self.ptr += 2
        
        
    def opcode_terminate(self):
        self.halt = True

f = "input.txt"

lines = open(f)

for l in lines:
    opcode = list(map(int,l.strip().split(",")))

painter = opcode_machine(opcode) 
painter2 = opcode_machine(opcode) 
while 1:
    color_to_paint, ok = painter.run_machine()
    if ok:
        print(len(painter.color_memory))
        break
    else:
        paint, direction = painter.output
        painter.color(paint)
        painter.move(direction)
        painter.output = []
        painter.pause = False
#2478
        
painter2.color_memory[(0,0)] = 1        
while 1:
    color_to_paint, ok = painter2.run_machine()
    if ok:
        break
    else:
        paint, direction = painter2.output
        painter2.color(paint)
        painter2.move(direction)
        painter2.output = []
        painter2.pause = False

maxc,maxr,minc,minr = 0,0,0,0
for r,c in painter2.color_memory:
    maxc = max(c,maxc)
    maxr = max(r,maxr)
    minc = min(c,minc)
    minr = min(r,minr)

 
rows = maxr - minr + 1
cols = maxc - minc + 1

r_adj = - minr
c_adj = - minc

picture = [[" " for _ in range(cols)] for __ in range(rows)]

for loc in painter2.color_memory:
    r,c = loc
    if painter2.color_memory[loc] == 0:
        picture[r+r_adj][c+c_adj] = " "
    else:
        picture[r+r_adj][c+c_adj] = "#"
for l in picture:
    print(''.join(l))
#HCZRUGAZ     
