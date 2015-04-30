import sys
myfile = sys.argv[1]
Tfile = "T_"+myfile
Lfile = "L_"+myfile
Cfile = "C_"+myfile

print "Parsed File: " + myfile
print "Temp Readings in: " + Tfile
print "Light Readings in:  " + Lfile
print "Crossings Readings in: " + Cfile

try:
	fo = open(myfile, "r")
	foT = open(Tfile, "w")
	foL = open(Lfile, "w")
	foC = open(Cfile, "w")

	for line in fo :
		if line != '\n':
			fields = line.split(' ')
			if 'Transmission' and 'error:' not in line:
				if 'Temperature(C)' in line:
					if len(fields) == 6:
						foT.write(line)
				if 'Light' in line:
					if len(fields) == 6:
						foL.write(line)

				if 'count:' in line: 			
					foC.write(line)
				

except IOError as (errno, strerror):
	print "I/O error({0}): {1}".format(errno, strerror)

fo.close
foT.close
foL.close
foC.close

