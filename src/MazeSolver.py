import sys
import math

#----------------------------------------------------------------------
#fungsi BFS
def BFS():
	global current, visited, queue, maze, jalur
	koor = []
	solution = []
	current = queue[0]
	if((current[0] != 0) and (maze[current[0]-1][current[1]] == 0)) : #mau ke atas
		koor = [current[0]-1,current[1]]
		if (koor not in visited):
			queue.append(koor)
			solution.append(koor)
	if((current[1] != (len(maze[0]) - 1)) and (maze[current[0]][current[1]+1] == 0)) : #mau ke kanan
		koor = [current[0],current[1]+1]
		if (koor not in visited):
			queue.append(koor)
			solution.append(koor)
	if((current[1] != (len(maze)-1)) and (maze[current[0]+1][current[1]] == 0)) : #mau ke bawah
		koor = [current[0]+1,current[1]]
		if (koor not in visited):
			queue.append(koor)
			solution.append(koor)
	if((current[0] != 0) and (maze[current[0]][current[1]-1] == 0)) : #mau ke kiri
		koor = [current[0],current[1]-1]
		if (koor not in visited):	
			queue.append(koor)
			solution.append(koor)
	
	if (len(solution) > 0) :
		for i in range(len(solution)):
			if (current != solution[i] and solution[i] not in visited):
				jalur.append([current,solution[i]])
		
	queue.pop(0)
	visited.append(current)

#----------------------------------------------------------------------
#fungsi bactracking
def backtrack() :
	global jalur
	global goal
	global start
	global maze
	value = goal
	maze[value[0]][value[1]] = '.'
	while (value != start):
		for i in range(len(jalur)):
			if (value == jalur[i][1]):
				value = jalur[i][0]
				break
		
		maze[value[0]][value[1]] = '.'

#----------------------------------------------------------------------
#fungsi untuk membaca File eksternal berupa txt file menjadi list of list of Char
def readFile(FileEx):
	block = '\u2588'
	F = list(open(FileEx,'r').read().split('\n'))
	Maze = []
	for i in range(len(F)):
		Maze.append(list(F[i]))
	return Maze
#----------------------------------------------------------------------
#fungsi untuk menampilkan maze pada layar dengan jalannya 
def printMaze(F):
	for i in range(len(F)):
		for j in range(len(F[i])):
			if (F[i][j] == '.'):
				print (block, end = block)
			else :
				print(F[i][j],end = ' ')
		print()
#----------------------------------------------------------------------
#fungsi untuk menhitung jarak dari suatu titik ke goal, untuk fungsi heuristik A*
def countDistance(inp,out):
	return math.sqrt(pow(out[0], inp[0]) + pow(out[1], inp[1]))
#----------------------------------------------------------------------
#fungsi untuk mencari nilai x pada way, dan akan menghapus nilai x pada way 
#jika pop bernilai True
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

#----------------------------------------------------------------------
#fungsi untuk mencari vertex dalam labirin yang bercabang menjadi 3 (pertigaan)
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
#----------------------------------------------------------------------
#prosedur untuk menjalankan algoritma A* dan menampilkan hasil pada layar
def Astar(inp, out, lifeNode,F,size,passed, way,Vertex):
	lifeNode.pop(0)
	if (inp == out):
	#jalan sudah ditemukan	
		Result = []
		for i in range(len(F)):
			Result.append(F[i])
			for j in range(len(F[i])):
				if (findWay([i+1,j+1],way,True)):
					Result[i].pop(j)
					Result[i].insert(j,'.')
		printMaze(Result)
	else :
		#jalan belum ditemukan
		if (inp[0] > 0) :
			#mengecek apakah ada jalan di sebelah atas dari simpul
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i-1][j] == '0'):
				#ada jalan di sebelah kiri simpul
				i -= 1
				newWay = way.copy()
				while (i > 0) and (not found):
					#iterasi sampai simpul tersebut bertemu tembok
					#atau merupakan pertigaan
					newWay.append([i+1,j+1])
					if (F[i-1][j] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					else :
						i -= 1
				if (not(findWay([i+1,j+1],way,False))):
					#simpul yang ditemukan belum terdapat pada jalan yang 
					#sudah dilalui
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = inp[0] - i  + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		if (inp[0]< size):
			#mengecek apakah ada jalan di sebelah bawah dari simpul
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i+1][j] == '0'):
				i += 1
				newWay = way.copy()
				while (i < size) and (not found):
					#iterasi sampai simpul tersebut bertemu tembok
					#atau merupakan pertigaan
					newWay.append([i+1,j+1])
					if (F[i+1][j] == '1'):
						found = True
					elif (findWay([i,j],Vertex,False)):
						found = True
					else:
						i += 1
				if (not(findWay([i+1,j+1],way,False))):
					#simpul yang ditemukan belum terdapat pada jalan yang 
					#sudah dilalui
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = i - inp[0] + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		if (inp[1]>0):
			#mengecek apakah ada jalan di sebelah kiri dari simpul
			i = inp[0]
			j = inp[1]
			found = False
			if (F[i][j-1] == '0'):
				j -= 1
				newWay= way.copy()
				while (j > 0) and not (found):
					#iterasi sampai simpul tersebut bertemu tembok
					#atau merupakan pertigaan
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
			#mengecek apakah ada jalan di sebelah kanan dari simpul
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
					#iterasi sampai simpul tersebut bertemu tembok
					#atau merupakan pertigaan atau bertemu goal 
					# goal selalu ada di bagian kanan labirin
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
					#simpul yang ditemukan belum terdapat pada jalan yang 
					#sudah dilalui
					if ((found) or (findWay([i,j], Vertex,False))) :
						newPassed = j - inp[1]  + int (passed)
						newDist = newPassed + countDistance([i,j], out)
						x =[[i,j], newPassed, newDist,newWay]
						lifeNode.append(x)
		lifeNode.sort(key = lambda x: x[2])
		#sort simpul hidup berdasrkan newDist (f(n))
		Astar(lifeNode[0][0],out,lifeNode,F,size,lifeNode[0][1],lifeNode[0][3],Vertex)
		#telusuri lagi simpul dengan formula terkecil

#-----------------------------------
#-----------------------------------
#---------- MAIN PROGRAM ----------- 
#-----------------------------------
#-----------------------------------

#----------------------------------------------------------------------
#input nama file eksternal dan dibaca 
FileEx = input("Input external file name for the map (text file) : ")

with open(FileEx,'r') as f:
	input_t = f.readlines()

maze = []
for raw_line in input_t:
	split_line = raw_line.strip()
	nums_ls = [int(x) for x in split_line]
	maze.append(nums_ls)

#----------------------------------------------------------------------
#inisialisasi semua list yang akan dipakai
block = '\u2588'
queue = []		
visited = []	
jalur = []	
start = []	
goal = []		
current = []
solution = []

Vertex = []
lifeNode = ['z']

#----------------------------------------------------------------------
#meminta masukan koordinat start dan goal (dalam bentuk indeks matriks (i,j))
in_start = str(input("Input the coordinate of the maze entrance (x,y) : "))
start = [int(x) for x in in_start.split(',')]
while (maze[start[0]][start[1]] == 1):		#start harus benar pada grid 0
	in_start = str(input("Input the coordinate of maze the entrance (x,y) : "))
	start = [int(x) for x in in_start.split(',')]
start = [int(x) for x in in_start.split(',')]

in_goal = str(input("Input the coordinate of the maze exit (x,y) : "))
goal = [int(x) for x in in_goal.split(',')]
while (maze[goal[0]][goal[1]] == 1):		#goal harus benar pada grid 0
	in_goal = str(input("Input the coordinate of the maze exit (x,y) : "))
	goal = [int(x) for x in in_goal.split(',')]
goal = [int(x) for x in in_goal.split(',')]

#----------------------------------------------------------------------
#menjalankan algoritma BFS
print()
print ("With BFS : ")

#----------------------------------------------------------------------
#koordinat start di-push ke queue
queue.append(start)

#----------------------------------------------------------------------
#algoritma BFS dimulai
while (len(queue) > 0 and (goal not in visited)) :
	BFS()

#----------------------------------------------------------------------
#menemukan path yang dilalui dari start menuju goal
backtrack()
#print solusi path
printMaze(maze)

#----------------------------------------------------------------------
#menjalankan algoritma A*
print()
print("With A* :")
F = readFile(FileEx)

#----------------------------------------------------------------------
#mencatat indeks maksimal dalam matriks peta
size = len(F[0]) -1

#----------------------------------------------------------------------
#memasukan koordinat start ke dalam list jalan yang dilewati
inp = []
inp.append(start[0]+1)
inp.append(start[1]+1)
way = [inp.copy()]

#----------------------------------------------------------------------
#mencari semua vertex bercabang 3
searchVertex(F,Vertex)

#----------------------------------------------------------------------
#Algoritma A* dimulai
Astar(start,goal, lifeNode,F,size,'0',way,Vertex)