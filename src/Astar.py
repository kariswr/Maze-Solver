import math

def readFile(FileEx):
	block = '\u2588'
	F = list(open(FileEx,'r').read().split('\n'))
	Maze = []
	for i in range(len(F)):
		Maze.append(list(F[i]))
	return Maze

def printMaze(F):
	for i in range(len(F)):
		for j in range(len(F[i])):
			if (F[i][j] == '.'):
				print (block, end = block)
			else :
				print(F[i][j],end = ' ')
		print()

def countDistance(inp,out):
	return math.sqrt(pow(out[0], inp[0]) + pow(out[1], inp[1]))

def findWay(x,way,pop):
	found = False
	i = 0
	while (i < (len(way))) and (not found):
		if (x == way[i]):
			found = True
			if (pop):
				way.pop(i)
		else: 
			i += 1
	return found

def searchVertex(F,Vertex):
	for i in range(len(F)):
		for j in range(len(F[i])):
			count = 0
			if (F[i][j] == '0'):
				if (j<size and F[i][j+1] == '0'):
					count += 1
				if (i < size and F[i+1][j] == '0'):
					count += 1
				if (j>0 and F[i][j -1] == '0'):
					count += 1
				if (i > 0 and F[i-1][j] == '0'):
					count += 1
			if (count > 2):
				Vertex.append([i,j])

def Astar(inp, out, lifeNode,F,size,passed, way,Vertex):
	print("way : ",way)
	lifeNode.pop(0)
	print(inp)
	print(out)
	if (inp == out) :
		Result = []
		for i in range(len(F)):
			Result.append(F[i])
			for j in range(len(F[i])):
				if (findWay([i+1,j+1],way,True)):
					Result[i].pop(j)
					Result[i].insert(j,'.')
		printMaze(Result)
	else :
		if (inp[0] > 0) :
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i-1][j] == '0'):
				i -= 1
				newWay = way.copy()
				while (i > 0) and (not found):
					newWay.append([i+1,j+1])
					if (F[i-1][j] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					else :
						i -= 1
				if (not(findWay([i+1,j+1],way,False))):
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = inp[0] - i  + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		if (inp[0]< size):
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i+1][j] == '0'):
				i += 1
				newWay = way.copy()
				while (i < size) and (not found):
					newWay.append([i+1,j+1])
					print(i,j)
					if (F[i+1][j] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					else:
						i += 1
				print (found)
				if (not(findWay([i+1,j+1],way,False))):
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = i - inp[0] + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		if (inp[1]>0):
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i][j-1] == '0'):
				j -= 1
				newWay= way.copy()
				while (j > 0) and not (found):
					newWay.append([i+1,j+1])
					if (F[i][j-1] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					else:
						j -= 1
				if (not(findWay([i+1,j+1],way,False))):
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = inp[1] - j  + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		if (inp[1] < size):
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i][j+1] == '0'):
				j += 1
				newWay = way.copy()
				if (j == size):
					found = True
					newWay.append([i+1,j+1])
				while (j < size) and (not found):
					newWay.append([i+1,j+1])
					if (F[i][j+1] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					elif (j+1 == size):
						found = True
						newWay.append([i+1,j+1])
					else :
						j += 1
				if (not(findWay([i+1,j+1],way,False))):
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = j - inp[1]  + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		lifeNode.sort(key = lambda x: x[2])
		Astar(lifeNode[0][0],out,lifeNode,F,size,lifeNode[0][1],lifeNode[0][3],Vertex)

Vertex = []
FileEx = input("Input external file name for the map (text file) : ")
F = readFile(FileEx)
size = len(F[0]) -1
inp = input("Input the coordinate of the entrance (x,y) : ").split(',')
out = input("Input the coordinate of the exit (x,y) : ").split(',')
inp= [int(inp[0]), int(inp[1])]
out = [int(out[0]), int(out[1])]
way = [inp.copy()]
inp[0] = inp[0] -1
inp[1] = inp[1] -1
out[0] = out[0] -1
out[1] = out[1] -1
lifeNode = ['z']
searchVertex(F,Vertex)
block = '\u2588'
Astar(inp,out, lifeNode,F,size,'0',way,Vertex)
