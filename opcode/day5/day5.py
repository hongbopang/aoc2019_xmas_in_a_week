# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:00:55 2021

@author: hongb
"""


class opcode_machine:
    def __init__(self, opcode, input_val=0):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.halt = False
        self.input = input_val
        self.output = None

    def modify(self, pos, val):
        self.seq[pos] = val
        
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
            
        #2 parameters    
        elif ins[-1] == "5" or ins[-1] == "6":
            major_code = int(ins[-1])
            
            if len(ins) < 4:
                ins = "0" * (4-len(ins)) + ins
            parameters = []
            for i in ins[:2]:
                parameters.append(int(i))
            parameters = parameters[::-1]
            
        #1 parameters       
        elif ins[-1] == "3" or ins[-1] == "4":
            major_code = int(ins[-1])
            
            if len(ins) <= 2:
                parameters = [0]
            else:
                parameters = [int(ins[0])]
                

                
        
        return major_code, parameters
        
    def read_once(self):
        instruction = str(self.seq[self.ptr])

        major_code, parameters = self.decode(instruction)


        if major_code == 99:
            self.opcode_terminate()
            return

        if major_code == 1:
            self.opcode_1(parameters)
        elif major_code == 2:
            self.opcode_2(parameters)
        elif major_code == 3:
            self.opcode_3(parameters)
        elif major_code == 4:
            self.opcode_4(parameters)      
        elif major_code == 5:
            self.opcode_5(parameters)     
        elif major_code == 6:
            self.opcode_6(parameters)     
        elif major_code == 7:
            self.opcode_7(parameters)                 
        elif major_code == 8:
            self.opcode_8(parameters)     
            
    def opcode_1(self,parameters):
        mode1, mode2, mode3 = parameters
        if mode1 == 0:            
            pos1 = self.seq[self.ptr+1]
            num1 = self.seq[pos1]
        elif mode1 == 1:
            num1 = self.seq[self.ptr+1]        
                
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]
            

        pos3 = self.seq[self.ptr+3]
        
        self.seq[pos3] = num1 + num2              
        self.ptr += 4
        
    def opcode_2(self,parameters):
        mode1, mode2, mode3 = parameters
        if mode1 == 0:            
            pos1 = self.seq[self.ptr+1]
            num1 = self.seq[pos1]
        elif mode1 == 1:
            num1 = self.seq[self.ptr+1]
        
                
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]            

        pos3 = self.seq[self.ptr+3]
        
        self.seq[pos3] = num1 * num2             
        self.ptr += 4
        
        
        
    def opcode_3(self, parameters):
        pos1 = self.seq[self.ptr+1]
 
        self.seq[pos1] = self.input        
        
        self.ptr += 2
        
    def opcode_4(self, parameters):
        mode1 = parameters[0]
        if mode1 == 0:
            pos1 = self.seq[self.ptr+1] 
            num1 = self.seq[pos1]  
        else:
            num1 = self.seq[self.ptr+1] 
            
        self.output =  num1
        print(self.output)
        self.ptr += 2
        
    def opcode_5(self, parameters):
        mode1, mode2 = parameters
        if mode1 == 0:
            pos1 = self.seq[self.ptr+1] 
            num1 = self.seq[pos1]  
        else:
            num1 = self.seq[self.ptr+1]             
            
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]
            
        if num1 != 0:
            self.ptr = num2
        else:
            self.ptr += 3
            
    def opcode_6(self, parameters):
        mode1, mode2 = parameters
        if mode1 == 0:
            pos1 = self.seq[self.ptr+1] 
            num1 = self.seq[pos1]  
        else:
            num1 = self.seq[self.ptr+1]             
            
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]
            
        if num1 == 0:
            self.ptr = num2
        else:
            self.ptr += 3
            
    def opcode_7(self,parameters):
        mode1, mode2, mode3 = parameters
        if mode1 == 0:            
            pos1 = self.seq[self.ptr+1]
            num1 = self.seq[pos1]
        elif mode1 == 1:
            num1 = self.seq[self.ptr+1]        
                
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]
            

        pos3 = self.seq[self.ptr+3]
        if num1 < num2:            
            self.seq[pos3] = 1
        else:
            self.seq[pos3] = 0
        self.ptr += 4
        
    def opcode_8(self,parameters):
        mode1, mode2, mode3 = parameters
        if mode1 == 0:            
            pos1 = self.seq[self.ptr+1]
            num1 = self.seq[pos1]
        elif mode1 == 1:
            num1 = self.seq[self.ptr+1]        
                
        if mode2 == 0:            
            pos2 = self.seq[self.ptr+2]
            num2 = self.seq[pos2]
        elif mode2 == 1:
            num2 = self.seq[self.ptr+2]
            

        pos3 = self.seq[self.ptr+3]
        if num1 == num2:            
            self.seq[pos3] = 1
        else:
            self.seq[pos3] = 0
        self.ptr += 4
    def opcode_terminate(self):
        self.halt = True
        
        
f = "input.txt"

lines = open(f)

for l in lines:
    opcode = list(map(int,l.strip().split(",")))
    
    
machine = opcode_machine(opcode, 1)

while not machine.halt:
    machine.read_once()
print("machine1")
#5074395
    

machine2 = opcode_machine(opcode, 5)

while not machine2.halt:
    machine2.read_once()
print("machine2")
#8346937