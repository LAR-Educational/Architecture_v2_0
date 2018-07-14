import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
import os



from numpy import genfromtxt

"""
vec
with open('fadap.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		vec+ = row


print vec
"""


path = "../BKS/Log/AdaptiveLogs"

namelist = os.listdir(path)

#print nameflist

data_list = []

for name in namelist:
	
	if "vector" in name:
		#data_list.append(name)
		data_list.append( genfromtxt(path+'/'+name, delimiter=',', skip_header=0))
		


fadp= 0
alpha=0
beta= 0
gama= 0


frames = []



for mat in data_list:
	
	for row in mat:
		i=0
		fadp+= row[1]
		alpha+=row[2]
		beta+= row[3]
		gama+= row[4]
		
		#for j in range(1, len(item[i])):
		#	print item[i][j]
		
	
	print "new matrix"	

exit()




#print my_data
my_data = np.transpose(my_data)
#print my_data

alpha = my_data[1]
print alpha

beta = my_data[2]
print beta

gama = my_data[3]
print gama

f = my_data[0]#0.5*alpha + 0.3*beta + 0.2*gama

print f

x = range(1,4)

print x


plt.plot(x,alpha, label='Alpha')
plt.plot(x,beta, label='Beta')
plt.plot(x,gama, label='Gama')
plt.plot(x,f, label='Fadap', linewidth=5)

#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.legend(bbox_to_anchor=(1,1), loc =1)





plt.xlabel('Adaptive Window (t)')
plt.ylabel('Value')
plt.title('Adaptive Vectors')
plt.grid(True)
plt.savefig("test.png")
plt.show()
