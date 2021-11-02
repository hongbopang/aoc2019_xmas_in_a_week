# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 16:13:02 2021

@author: hongb
"""


class opcode_machine:
    def __init__(self, opcode):
        self.ptr = 0
        self.seq = [i for i in opcode]
        self.halt = False
        self.pause = False
        self.input = []
        self.output = None
        self.base = 0
        self.oxygen = None
        
        self.r_c = (0,0)

        self.frontier = [((0,0), None, [], 0)] # [location, parent, pathfromorigin, distance]
        self.distances = dict() # -1 for walls
        self.directions = [(1,0), (-1,0), (0,-1), (0,1)] #NE positive
        self.paths = dict()
        self.paths[(0,0)] = []
        
    def add_input(self, input_val):
        self.input.append(input_val)

    def modify(self, pos, val):
        self.seq[pos] = val
        
    def operate(self):
        ans = 0
        while not ans:
            ans = self.bfs()
        print(ans)
        
        while len(self.frontier) != 0:
            self.bfs()
        
    def attempt_move(self, instruction):
        self.add_input(instruction)
        self.pause = False
        self.run_machine()
        
        result = self.output
        
        if instruction == 1 or instruction == 3:
            opp = instruction + 1
        else:
            opp = instruction - 1

        if result == 0:
            return -1
        elif result == 1:
            self.add_input(opp)
            self.run_machine() 
            self.output = None
            return 0
        else:
            self.add_input(opp)
            self.run_machine() 
            self.output = None

            return 1
            
            
    def goto(self, target):

        path_home = self.paths[self.r_c]
        path_home = path_home[::-1]
        back_path = []

        for i in path_home:
            if i == 0 or i == 2:
                opp = i + 1
            else:
                opp = i - 1
            back_path.append(opp)

    
        fwd_path =  self.paths[target]       
        united_path =  back_path + fwd_path
        
        for i in united_path:
            instruction = i + 1
            self.pause = False
            self.add_input(instruction)
            self.run_machine()
        
        self.r_c = target
        
    def bfs(self):

        me, parent,pathfromorigin, distance = self.frontier.pop(0)        
        ans = 0
        if me != self.r_c:
            self.goto(me)

        for i in range(len(self.directions)):
            
            tmpr, tmpc = me[0] + self.directions[i][0], me[1] + self.directions[i][1]

            if (tmpr, tmpc) not in self.paths:
                result = self.attempt_move(i+1)

                if result != -1:     
                    self.frontier.append(((tmpr,tmpc), me, pathfromorigin + [i], distance + 1))
                    self.paths[(tmpr,tmpc)] = pathfromorigin + [i]     
                    if distance + 1 not in self.distances:
                        self.distances[distance+1] = []
                    self.distances[distance+1].append((tmpr,tmpc))
                    if result == 1:
                        ans = distance + 1
                        self.oxygen = (tmpr,tmpc)
        return ans
    
    def run_machine(self):
        while 1:
            self.read_once()
            if self.pause:
                return False
            elif self.halt:
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

        self.output =  num1
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
    
maze_robot = opcode_machine(opcode)
part2_robot = opcode_machine(opcode)
ans = maze_robot.operate()

#224

locations = [(0,0)]

for i in maze_robot.distances:
    locations += maze_robot.distances[i]
    


frontier = [maze_robot.oxygen]

distances = dict()
distances[maze_robot.oxygen] = 0

while len(frontier) != 0:
    r,c = frontier.pop(0)
    curr_dist = distances[(r,c)]
    
    next_steps = [(r+1,c), (r-1,c), (r,c-1), (r, c+1)]
    
    for tmp in next_steps:
        if tmp in locations and tmp not in distances:
            frontier.append(tmp)
            distances[tmp] = curr_dist + 1
            
print(curr_dist)
#284
