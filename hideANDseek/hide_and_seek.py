import random
from random import choice
import sys
import math
#variables = {A(1,1), A(1,2), A(1,3), ... , A(11,11)}
#domain = {friend, tree, empty}

def backtracking_search():
	variables = []
	#friend = 1, tree = -1, empty = 0
	#since trees are preplaced, we are only concerned with 1 and 0
	domain = [1,0]
	#assignments keeps track of everything that has been assigned,
	#as well as the number of friends that have been assigned.
	assignments = [[],0]
	#puts args in a list of coordinates
	#the first coordinate pair is n and k, the rest are coordinates of trees
	args = [(int(line.strip().split()[0]), int(line.strip().split()[1])) for line in open('smplin')]
	num_friends = args[0][0]
	#num_trees = args[0][1]
	num_trees = 0
	#assign all spaces with trees a value of -1
	# for tree in args[1:num_trees+1]:
	# 	# if the coordinate is in the specified game board, num_friends is also the grid length
	# 	if tree[0] <= num_friends and tree[1] <= num_friends:
	# 		assignments[0].append((tree,-1))
	#put each space on the board in the assigned list or variable list
	i = 0
	for x in range(1,num_friends+1):
		for y in range(1,num_friends+1):
			if ((x,y),-1) not in assignments[0]:
			#all spaces without trees are still variables
				variables.append((x,y))
	csp = [variables,domain,num_friends]
	for assignment in backtrack(assignments,csp, 0)[0]:
		if assignment[1] == 1:
			print assignment[0][0], assignment[0][1]
	return

def backtrack(assignments, csp, num_backtracks):
	variables = csp[0]
	domain = csp[1]
	num_friends = csp[2] #this is also the grid length
	#if the quantity of assignments made equals the number of people, everyone has a spot.
	if assignments[1] == num_friends:
		print "NUM BACKTRACKS:", num_backtracks
		return assignments
	if len(variables) == 0:
		return "failure"
	#var = choice(variables)
	var = global_heuristic(assignments, csp)
	#var = local_heuristic(assignments, csp)
	for value in domain:
		assignments[0].append((var, value))
		variables.remove(var)
		if value == 1:
			assignments[1] += 1
		if isValid(var, value, assignments, num_friends):
			num_backtracks += 1
			result = backtrack(assignments, csp, num_backtracks)
			if result != "failure":
				return result
		assignments[0].remove((var, value))
		variables.append(var)
		if value == 1: assignments[1] -= 1
	return "failure"

def isValid(var, value, assignments, grid_length):
	x_coord = var[0]
	y_coord = var[1]
	#if the value is 1, we must not have another 1 visible.
	if value == 1:
		#flag used to check if trees seperate people or not
		#x-axis check
		flag = 0
		for x in range(1,grid_length+1):
			if ((x,y_coord), 1) in assignments[0]:
				#the first person we hit, switch the flag
				#if we get to another person before hitting a tree or
				#reaching the end of the board, return false.
				if flag == 0: flag = 1
				else: return 0
			elif ((x,y_coord), -1) in assignments[0]:
				flag = 0
		#y-axis check
		flag = 0
		for y in range(1,grid_length+1):
			if ((x_coord,y), 1) in assignments[0]:
				if flag == 0: flag = 1
				else:
					return 0
			elif ((x_coord, y), -1) in assignments[0]:
				flag = 0
		#positive slope diagonal check
		if x_coord >= y_coord:
			start_coord = (x_coord - y_coord + 1, 1)
		else: start_coord = (1, y_coord - x_coord + 1)
		flag = 0
		for counter in range(0, grid_length - max(start_coord[0], start_coord[1]) + 1):
			if ((start_coord[0] + counter, start_coord[1] + counter), 1) in assignments[0]:
				if flag == 0: flag = 1
				else: return 0
			elif ((start_coord[0] + counter, start_coord[1] + counter), -1) in assignments[0]:
				flag = 0
		#negative slope diagonal check
		if x_coord + y_coord <= grid_length:
			start_coord = (x_coord + y_coord - 1 , 1)
		else: start_coord = (grid_length , x_coord + y_coord - grid_length)
		flag = 0
		for counter in range(0, min(start_coord[0], grid_length - start_coord[1] + 1)):
			if ((start_coord[0] - counter, start_coord[1] + counter), 1) in assignments[0]:
				if flag == 0: flag = 1
				else: return 0
			elif ((start_coord[0] + counter, start_coord[1] + counter), -1) in assignments[0]:
				flag = 0
	return 1

def local_heuristic(assignments, csp):
	variables = csp[0]
	domain = csp[1]
	num_friends = csp[2] #this is also the grid length
	friend_list = []
	farthest = 0
	farthest_coord = None
	if assignments[1] == 0: #if no one has been assigned yet
		return choice(variables) #return a corner spot

	last_placed_friend = None

	for i in range(1,len(assignments[0])+1):
		if assignments[0][-i][1] == 1:
			last_placed_friend = assignments[0][-i][0]
			break

	for var in variables:
		#if last_placed_friend != None:
			distance = find_distance(var, last_placed_friend) #distance from x to last assigned space
			if distance > farthest:
				farthest = distance
				farthest_coord = var

	return var


def global_heuristic(assignments, csp):
	variables = csp[0]
	domain = csp[1]
	num_friends = csp[2] #this is also the grid length
	friend_list = []
	farthest = 0
	farthest_coord = None
	if assignments[1] == 0: #if no one has been assigned yet
		return choice(variables) #return any unassigned spot.

	for var in variables:
		distance_sum = 0

		for assignment in assignments[0]: #for every assignment made
			if assignment[1] == 1: #if the assignment is a person
				distance_sum += find_distance(var,assignment[0])
		mean_distance = distance_sum/assignments[1] #mean is distance_sum over number of people
		if mean_distance > farthest:
			farthest = mean_distance
			farthest_coord = var

	return var

def find_distance(coord1, coord2):
	return math.sqrt((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)


backtracking_search()
