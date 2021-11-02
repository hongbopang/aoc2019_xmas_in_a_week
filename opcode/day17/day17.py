# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 12:21:09 2021

@author: hongb
"""

turns = [(-1,0),(0,1),(1,0),(0,-1)]

def find_turn(scaffold_loc, pos, facing):
    r,c = pos
    dir_L = (facing - 1) % 4
    dir_R = (facing + 1) % 4
    
    delrow, delcol = turns[dir_L]
    
    tmp = (r+delrow, c+delcol)
    if tmp in scaffold_loc:
        return "L", dir_L
    
    delrow, delcol = turns[dir_R]
    tmp = (r+delrow, c+delcol)
    if tmp in scaffold_loc:
        return "R", dir_R
    
    return "END", -1

def find_end(scaffold_loc, pos, facing):
    me = pos
    delrow, delcol = turns[facing]
    counter = 0
    while 1:
        r,c = me
        tmp = (r+delrow, c+delcol)
        if tmp in scaffold_loc:
            counter += 1
            me = tmp
        else:
            return counter, me
    

class opcode_machine:
    def __init__(self, opcode):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.halt = False
        self.pause = False
        self.input = []
        self.output = []
        self.base = 0
        
    def add_input(self, input_val):
        self.input.append(input_val)

    def modify(self, pos, val):
        self.seq[pos] = val
        
    def run_machine(self):
        while 1:
            self.read_once()
            if self.pause:
                return False
            elif self.halt:
                return True
        return self.output
        
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
    
scaffolder = opcode_machine(opcode + [0] * 10000)
mover = opcode_machine(opcode + [0] * 10000)
scaffolder.run_machine()

scaffold = scaffolder.output

image = []
tmp = []
for instruction in scaffold:
    if instruction == 10:
        image.append(tmp)
        tmp = []
    else:
        tmp.append(chr(instruction))

image = image[:-1]
scaffold_loc = dict()
n_rows = len(image)
n_col = len(image[0])
ans = 0
for r in range(n_rows):
    for c in range(n_col):
        if image[r][c] == "#":
            scaffold_loc[(r,c)] = 1
            if r != 0 and r != n_rows - 1 and c != 0 and c != n_col -1:
                if image[r+1][c] == "#" and image[r-1][c] == "#" and image[r][c-1] == "#" and image[r][c+1] == "#":
                    ans += r*c
        elif image[r][c] != "." and image[r][c] != "#":
            start = (r,c)
            direction = image[r][c]

print(ans)
#10632

directions = dict()
directions["^"] = 0
directions[">"] = 1
directions["v"] = 2
directions["<"] = 3

facing = directions[direction]

instructions = []
pos = start
while 1:
    turn, facing = find_turn(scaffold_loc,pos,facing)
    if turn == "END":
        break
    
    steps,pos = find_end(scaffold_loc, pos, facing)
    instructions.append(turn+str(steps))
    
print(instructions)

main_routine = "A,B,A,C,A,A,C,B,C,B"
main_ins = []
for char in main_routine:
    main_ins.append(ord(char))
main_ins.append(10)  

rout_A = "L,12,L,8,R,12"
A_ins = []
for char in rout_A:
    A_ins.append(ord(char))
A_ins.append(10) 
    
rout_B = "L,10,L,8,L,12,R,12"
B_ins = []
for char in rout_B:
    B_ins.append(ord(char))    
B_ins.append(10)   


rout_C = "R,12,L,8,L,10"
C_ins = []
for char in rout_C:
    C_ins.append(ord(char))    
C_ins.append(10) 

mover.modify(0,2)
mover.run_machine()


for instruction in main_ins:
    mover.add_input(instruction)
    
mover.output = []
mover.pause = False
mover.run_machine()

print(A_ins, B_ins,C_ins)

for instruction in A_ins:
    mover.add_input(instruction)    
mover.output = []
mover.pause = False
mover.run_machine()

for instruction in B_ins:
    mover.add_input(instruction)  
mover.output = []
mover.pause = False
mover.run_machine()

for instruction in C_ins:
    mover.add_input(instruction)
mover.output = []
mover.pause = False
mover.run_machine()   

mover.add_input(ord("n"))
mover.add_input(10)
mover.output = []

mover.pause = False
mover.run_machine()   
print(mover.output)


