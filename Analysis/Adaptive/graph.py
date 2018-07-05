import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv
from numpy import genfromtxt

"""
vec
with open('fadap.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		vec+ = row


print vec
"""


my_data = genfromtxt('fadap.csv', delimiter=',', skip_header=1)
#print my_data
my_data = np.transpose(my_data)
#print my_data

alpha = my_data[0]
print alpha

beta = my_data[1]
print beta

gama = my_data[2]
print gama

f = 0.5*alpha + 0.3*beta + 0.2*gama

print f

x = range(1,10)

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
