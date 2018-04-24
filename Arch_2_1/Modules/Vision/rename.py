

import os
import csv

print "Starting"


shapes =[]

with open('shapes.csv', 'rb') as csvfile:
	csv_readed = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for sh in csv_readed:
		shapes+=sh

#return 1


print shapes



dir = "./data/collected"
#pattern = "*.jpg"
#titlePattern

#shapes = ['cub','pir','esf']

class_number = len(shapes)

print "Number of Classes: ", class_number

filenames = os.listdir(dir)

#print filenames


print shapes[0]



i=0

for c in range(0,class_number):
	
	
	cdir = os.path.join(dir, shapes[c]) 
	print "working with cdir = ", cdir

	for fn in filenames:
		
		
		if fn[0]==str(c):
			newname = shapes[c] + str(i) +".jpg"
			os.rename(os.path.join(dir,fn),os.path.join(dir,newname))
		#print "Converting ", os.path.join(dir,fn), ' to ', os.path.join(dir,newname)
		i+=1


#rename(r'/Vision/alldb/0',r'*.jpg',r'cube')


print "Done"













