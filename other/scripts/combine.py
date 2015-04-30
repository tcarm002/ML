import csv
import re
import time
import datetime

r= '\d{2}:\d{2}:\d{2}'

temp_file = "2015-02-20 22_56_23_Temp.csv"
crossing_file = "2015-02-20 22_56_23_Crossings.csv"
light_file = "2015-02-20 22_56_23_Light.csv"

files = [temp_file,crossing_file,light_file] #All files

NUM_REGIONS = 5
NUM_NODES = 6

light_thresholds = [20,20,20,7,5] #light threshold values per node
temp = [] #temperature data
crossings = []	#crossing data
light = [] #lighting data
data = [] #Used to store data parsed from all files
final = [] #The combined data

try:
	for f in files:
		t = []
		with open(f,"r") as file:
			lines = file.read().split("\n") #Used to strip trailing \n from rows
		for line in lines :
			fields = line.split(',')  #Grabs fields from csv
			t.append(fields) #Used to temporarily store all rows
		data.append(t)	#Stores file data as one element 
		file.close
	
	
except IOError as (errno, strerror):
	print "I/O error({0}): {1}".format(errno, strerror)


#Populates the individual data arrays
data_2 = [temp,crossings,light]

for i in range(0,len(data)):
	data_2[i].append( data[i])
	


nodes_sort = [[] for x in xrange(NUM_NODES)] #The temp data, sorted by node number
#Creates a list of lists of temperature data sorted by node
for t in temp[0]:
	#Used to parse out incompletely transmitted lines#Parse out incorrect timestamps#Parse out non-numbers in node list#Parse out nodes not in range of node nums
	if len(t) == 3 and re.match(r,t[0]) and t[1].isdigit() and int(t[1]) in range(0,NUM_NODES+1):	
		nodes_sort[int(t[1])-1].append(t)

#Function to find the temperature for a given node at a given time
def find_temp(timestamp,node):
	hour = int(timestamp[0:2])
	minute = int(timestamp[3:5])
	second = int(timestamp[6:8])
	
	for line in nodes_sort[int(node)-1]: #Checks through the correct list of a given node
		hour_2 = int(line[0][0:2])
		min_2 = int(line[0][3:5])
		sec_2 = int(line[0][6:8])
				
		if hour_2 == hour and min_2 >= minute and sec_2 >= second:
			#print "The time and the line: ", timestamp, line
			return line[2]
		
		


def find_node(node):
	if node == 2:
		region = 2
		return 0
	if node == 3:
		region = 3
		return 1
	if node == 4:
		region = 1
		return 2
	if node == 5:
		region = 4
		return 3
	if node == 6:
		region = 5
		return 4
	else:
		return -1

def find_node_2(region):
	if region == 2:
		return 2
	if region == 3:
		return 3
	if region == 1:
		return 4
	if region == 4:
		return 5
	if region == 5:
		return 6
	else:
		return -1
	


def parse_light():
	lights_sort = [[] for x in xrange(NUM_NODES)] #The temp data, sorted by node number
	#Creates a list of lists of temperature data sorted by node
	for l in light[0]:
		if len(l) == 3:	#Used to parse out incompletely transmitted lines
			node = l[1]
			#Parse out incorrect timestamps #Parse out non-numbers in node list
			if re.match(r,l[0]) and l[1].isdigit(): 
				try:
					node_i = int(node)
					if node_i in range(0,NUM_NODES+1): #Parse out nodes not in range of node nums
						#Checks through the correct list of a given node
						my_node = find_node(node_i)
						if my_node >= 0:
							light_val = l[2]
							time= l[0]
							if int(light_val) >= int(light_thresholds[my_node]):
								lights_sort[node_i-1].append([time,node,1])
							else:
								lights_sort[node_i-1].append([time,node,0])
				except ValueError:
					pass
				 
	return lights_sort

sorted_lights = parse_light() # A list of lists containing light values sorted by node

#Function to find the state of the light for a given region, at a given time
def find_light(timestamp,region):
	hour = int(timestamp[0:2])
	minute = int(timestamp[3:5])
	second = int(timestamp[6:8])
	node = find_node_2(int(region))
	
	if node >= 2:
		for line in sorted_lights[node-1]: #Checks through the correct list of a given node
			hour_2 = int(line[0][0:2])
			min_2 = int(line[0][3:5])
			sec_2 = int(line[0][6:8])
				
			if hour_2 == hour and min_2 >= minute and sec_2 >= second:
				#print "The time and the line: ", timestamp, line
				return int(line[2])
	
	return -1

final_2 = []
for c in crossings[0]:
	if len(c) == 11:#Used to parse out incompletely transmitted lines
		#Parse out incorrect timestamps #Parse out non-numbers in node list#Parse out nodes not in range of node nums
		if re.match(r,c[0]) and c[1].isdigit() and int(c[1]) in range(0,NUM_NODES+1): 
			for i in range(1, 6): #Goes through all columns of crossing data
				time = c[0]
				node = c[2*i-1]
				count = c[2*i]
				

				temp = find_temp(time,node) #Finds the temperature for the node, using the timestamp-->change to R
				
				light = find_light(time, node) #Finds state of light for the region, using the timestamp
								
				final.append([node,count,temp,light])
			if not 'None' in final:		
				final_2.append([time,final])
			final = []

for f in final_2:
	print f
	


