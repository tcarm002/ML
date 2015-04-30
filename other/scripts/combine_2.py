import csv
import re
import time
import datetime as dt


data_file = "nodes_with_time.csv"

NUM_REGIONS = 5
NUM_NODES = 6

data = [] #Used to store data parsed from all files


try:
	t = []
	with open(data_file,"r") as file:
		lines = file.read().split("\n") #Used to strip trailing \n from rows
	for line in lines :
		fields = line.split(',')  #Grabs fields from csv
		t.append(fields) #Used to temporarily store all rows
	data.append(t)	#Stores file data as one element 
	file.close

	
except IOError as (errno, strerror):
	print "I/O error({0}): {1}".format(errno, strerror)

#Traverse list backwards to find closest node
def gen_tdelta():
	final =[] #The list of tdelta values for the entire dataset
	tdelta = 0 #The amount of seconds since this node was activated
	time_set = False
	for i in range(1, len(data[0])-1):
		for j in range(i-1,-1,-1):
			if data[0][i][1] == data[0][j][1]: #Finds the closest node to the current node
				start=data[0][j][0] #The time on the current node
				end=data[0][i][0] #time on the closest, previous node
				start_dt = dt.datetime.strptime(start, '%H:%M:%S')
				end_dt = dt.datetime.strptime(end, '%H:%M:%S')
				diff = (end_dt - start_dt) #subtracts times
				tdelta = diff.seconds 	#converts to seconds		
				time_set = True #The ti
			if time_set:
				break
		time_set = False
		final.append(tdelta)
		tdelta = 0
	return final

#prints tdelta column
'''
print gen_tdelta()
'''

#Used to find correlation between occupancy and temperature
def temp_corr(occ,temp):
	threshold = 22.0
	if occ>0:
		if temp < threshold:#Average HVAC usage
			return .5
		if temp >= threshold:#Efficient HVAC usage
			return 1
	if occ<1:
		if temp<threshold: #Wasteful HVAC usage
			return 0
		if temp>=threshold: #Efficient HVAC usage
			return 1


data_file = "part2.csv"

try:
	t = []
	with open(data_file,"r") as file:
		lines = file.read().split("\n") #Used to strip trailing \n from rows
	for line in lines :
		fields = line.split(',')  #Grabs fields from csv
		t.append(fields) #Used to temporarily store all rows
	data.append(t)	#Stores file data as one element 
	file.close

	
except IOError as (errno, strerror):
	print "I/O error({0}): {1}".format(errno, strerror)

line = []
final = []
for d in data[1]:
	if len(d)>1:	
		for i in range(1,6):	
			occ = d[2*i]
			temp = d[2*i+1]
			score = temp_corr(int(occ),float(temp))
			line.append(score)
		final.append(line)
		line = []
for f in final:
	print f

