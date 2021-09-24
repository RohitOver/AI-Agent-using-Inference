'''This .py file coded by Rohit Mitra'''

#!/usr/bin/env python3
from Agent import * # See the Agent.py file
import numpy as np
from pysat.solvers import Glucose3
#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.

knowledge_base = []
#---safe rooms
safe = np.zeros([5,5],dtype = int)
#---visited already rooms
visited = np.zeros([5,5],dtype = int)
#---only for BFS use
bfs_vis = np.zeros([5,5],dtype = int)

#---checking if room valid
def IsValid(x,y):
	if((x >= 1 and x <= 4) and (y >= 1 and y <= 4)):
		return True
	else:
		return False

#---map room no.[x,y] to integer (1-16)
def MapToInt(x,y):
	res = np.zeros([5,5],dtype = int);
	counter = 1
	for j in range(1,5):
		for i in range(1,5):
			res[i,j] = counter
			counter += 1
	return int(res[x,y])

#---map int to room no.
def IntToLoc(val):
	#---a is room index
	a = []
	res = np.zeros([5,5],dtype = int);
	counter = 1
	for j in range(1,5):
		for i in range(1,5):
			res[i,j] = counter
			counter += 1
	for j in range(1,5):
		for i in range(1,5):
			if(res[i,j] == val):
				a.append(i)
				a.append(j)
	return a

def MakeInference(clause_x):
	checker = Glucose3()
	temp_kb = knowledge_base.copy()
	temp_kb.append([-1*int(clause_x)])
	#---check if KB^(!clause_x) is contradiction
	for i in range(len(temp_kb)):
		checker.add_clause(temp_kb[i])
	inference = checker.solve()
	checker.delete()
	return (not(inference))

#---inference using PL
def UpdateKnowledgeBase():
	for i in range(1,17):
		index = IntToLoc(i)
		if(MakeInference(i) == True and safe[index[0],index[1]] == 0):
			knowledge_base.append([i]);
			safe[index[0],index[1]] = 1

def ZeroPercept(x,y):
	#---add other rooms around it are safe clauses
	#--- U,R,D,L
	dx = [0,1,0,-1]
	dy = [1,0,-1,0]
	for i in range(4):
		if(IsValid(x+dx[i],y+dy[i])):
			clause_te = []
			clause_te.append(MapToInt(x+dx[i],y+dy[i]))
			knowledge_base.append(clause_te)

def OnePercept(x,y):
	#--- only 1 of neigbouring rooms is unsafe clauses
	#--- U,R,D,L
	dx = [0,1,0,-1]
	dy = [1,0,-1,0]
	valid = []
	clause_main = []
	for i in range(4):
		if(IsValid(x+dx[i],y+dy[i])):
			valid.append(MapToInt(x+dx[i],y+dy[i]))
	for i in range(len(valid)):
		clause_main.append(-1*valid[i])
		for j in range(i+1,len(valid)):
			knowledge_base.append([valid[i],valid[j]])
	knowledge_base.append(clause_main)

def MoreThanOnePercept(x,y):
	#--- > 1 of neigbouring rooms is unsafe clauses
	#--- U,R,D,L
	dx = [0,1,0,-1]
	dy = [1,0,-1,0]
	valid = []
	clause_main = []
	for i in range(4):
		if(IsValid(x+dx[i],y+dy[i])):
			valid.append(MapToInt(x+dx[i],y+dy[i]))
	for i in range(len(valid)):
		clause_main.append(-1*valid[i])
		clause_te = []
		for j in range(len(valid)):
			if(i != j):
				clause_te.append(-1*valid[j])
			else:
				clause_te.append(valid[j])
		knowledge_base.append(clause_te)
	knowledge_base.append(clause_main)

#---find nearest safe unvisited room
def FindClosestPoint():
	dist = 6
	si = 0
	sj = 0
	for i in range(1,5):
		for j in range(1,5):
			if(safe[i,j] == 1 and visited[i,j] == 0):
				val = 4-i+4-j
				if(val < dist):
					dist = val
					si = i
					sj = j
	res = []
	res.append(si)
	res.append(sj)
	return res

#---is [a,b] & [c,d] neighbours
def IsNeigbour(a,b,c,d):
	if((abs(a-c) == 1 and b == d) or (abs(b-d) == 1 and a == c)):
		return True
	else:
		return False

#---print safe array
def PrintSafe():
	for i in range(1,5):
		for j in range(1,5):
			print(safe[j,5-i],end = ' ')
		print()

#---move to go from source s to dest. d
def DecideDirection(sx,sy,dx,dy):
	if(dx == sx+1):
		dir = 'Right'
	elif(dx == sx-1):
		dir = 'Left'
	elif(dy == sy+1):
		dir = 'Up'
	else:
		dir = 'Down'
	return dir

#---bfs utility
def Clear_bfs_vis():
	for i in range(1,5):
		for j in range(1,5):
			bfs_vis[i,j] = 0

#---printing path clearly
def PrintFormat(path):
	print('--------SEQUENCE OF ROOMS IN AGENT\'S PATH : \n')
	print(path[0],end = '')
	for i in range(1,len(path)):
		print(' => ',path[i],end = '')
	print()


def main():
	knowledge_base.append([1])
	safe[1,1] = 1
	#---path_final is required path
	path_final = []
	ag = Agent()
	curr_position = ag.FindCurrentLocation()
	print('Starting Point ,Current Location ',curr_position)
	print()
	path_final.append([1,1])
	#---while loop till agent reaches [4,4]
	while(not(curr_position[0] == 4 and curr_position[1] == 4)):
		x = curr_position[0]
		y = curr_position[1]
		# print(curr_position)
		visited[x,y] = 1
		percept = ag.PerceiveCurrentLocation()
		if(percept == '=0'):
			ZeroPercept(x,y)
		elif(percept == '=1'):
			OnePercept(x,y)
		else:
			MoreThanOnePercept(x,y)
		UpdateKnowledgeBase()
		# PrintSafe()
		next_position = FindClosestPoint()
		# print('Next pos:',next_position)
		#---BFS follows;1 node has room no. & path taken as info
		queue = []
		te_path = []
		queue.append([curr_position,te_path])
		Clear_bfs_vis()
		bfs_vis[curr_position[0],curr_position[1]] = 1
		bfs_path = []
		while queue:
			#---p is node, q is path
			ele = queue.pop(0)
			p = ele[0].copy()
			q = ele[1].copy()
			# print(p)
			if(p == next_position):
				bfs_path = q.copy()
				# print('pop',bfs_path)
				break
			#---  U,R,D,L
			dx = [0,1,0,-1]
			dy = [1,0,-1,0]
			for i in range(4):
				ch = [p[0]+dx[i],p[1]+dy[i]]
				if(IsValid(ch[0],ch[1]) and bfs_vis[ch[0],ch[1]] == 0 and safe[ch[0],ch[1]] == 1):
					# print('child',ch)
					ch_path = q.copy()
					ch_path.append(ch)
					queue.append([ch,ch_path])
					bfs_vis[ch[0],ch[1]] = 1
		#---traversing from current node to next node via safe rooms
		for i in range(len(bfs_path)):
			move = DecideDirection(curr_position[0],curr_position[1],bfs_path[i][0],bfs_path[i][1])
			ag.TakeAction(move)
			print()
			curr_position = ag.FindCurrentLocation()
			path_final.append(curr_position)
	#---printing final path taken
	PrintFormat(path_final)



if __name__=='__main__':
    main()
