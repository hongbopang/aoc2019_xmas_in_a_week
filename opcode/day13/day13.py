# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 17:24:26 2021

@author: hongb
"""
import copy
class opcode_machine:
    def __init__(self, opcode):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.seq += [0 for _ in range(1000)]
        self.halt = False
        self.input = []
        self.output = []
        self.base = 0
        self.pause = False        
        
        self.score = 0
        self.screen = dict()
        for i in range(5):
            self.screen[i] = []
            
        self.ball_col = None
        self.paddle_col = None
        
        self.image = None
            
    def parse_screen(self):
        ptr = 0
        for i in range(5):
            self.screen[i] = []
        while ptr < len(self.output):
            x = self.output[ptr]
            y = self.output[ptr+1]
            tile = self.output[ptr+2]
            if tile == 3:
                self.ball_col = x
            elif tile == 4:
                self.paddle_col = x
            if x == -1 and y == 0:
                self.score = tile
            else:
                self.screen[tile].append((x,y))
            ptr += 3  
            
        if not self.image:
            minx, maxx, miny, maxy = 0,0,0,0
            walls = self.screen[1]

            for wall in walls:
                x,y = wall
                minx = min(minx, x)    
                miny = min(miny, y)    
                maxx = max(maxx, x)    
                maxy = max(maxy, y)

            x_len, y_len = maxx - minx + 1, maxy - miny + 1
            
            self.image = [[0 for _ in range(x_len)] for __ in range(y_len)]                  
            
            
        for key in self.screen:
            for x,y in self.screen[key]:
                self.image[y][x] = key       
            

        self.pause = False
        self.output = []
            
    def add_input(self, input_val):
        self.input.append(input_val)

    def modify(self, pos, val):
        self.seq[pos] = val
        
    def run_machine(self):
        while 1:
            self.read_once()
            if self.pause:
                
                self.parse_screen()         
                
                return False
            if self.halt:                
                self.parse_screen()
                return True
        
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
    
arcade = opcode_machine(opcode)
player = opcode_machine(opcode)


arcade.run_machine()
print(len(arcade.screen[2]))
#213


player.modify(0,2)
player.run_machine()

inputs = [-1,0,1]
decisions = [0,0,0]
scores = [0,0,0]

while not player.halt:


    players = [copy.deepcopy(player),copy.deepcopy(player),copy.deepcopy(player)]
    for i in range(3):
        players[i].add_input(inputs[i])
        players[i].run_machine()
        decisions[i] = abs(players[i].ball_col - players[i].paddle_col)
        scores[i] = players[i].score
    idx = decisions.index(min(decisions))  
    player = players[idx]
print(player.score)
#11441