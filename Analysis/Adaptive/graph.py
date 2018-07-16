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


class Window:
    
    def __init__(self, f, a, b, c):
        self.f = f
        self.a = a
        self.b = b
        self.c = c





def make(path = "../BKS/Log/AdaptiveLogs"):

    

    namelist = os.listdir(path)

    #print nameflist

    data_list = []

    for name in namelist:
            
            if "vector" in name:
                    #data_list.append(name)
                    data_list.append( genfromtxt(path+'/'+name, delimiter=',', skip_header=0))
                    


    final = np.zeros((3,5))

    for mat in data_list:
                
        
        final+=mat
        #print "Mat"
        #print mat
        #print "Final"
        #print final
        
          
        
    final = final/len(data_list)    
        
        
    my_data = np.transpose(final)
        
    print final   
        
          
        
    #print my_data
    #my_data = np.transpose(my_data)
    #print my_data

    alpha = my_data[2]
    #rint alpha

    beta = my_data[3]
    # print beta

    gama = my_data[4]
    #print gama

    f = my_data[1]#0.5*alpha + 0.3*beta + 0.2*gama

    #print f

    x = range(1, len(f)+1)

    #print x


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




def users():
    
    av = [6.571428571, 3.285714286, 6.714285714, 6.857142857, 5.714285714, 6.857142857, 5.714285714]
    sd = [0.7867957925, 1.799470822, 0.4879500365, 0.377964473, 0.9511897312, 0.377964473, 0.9511897312]

    
    
    
    x =  range(1,len(av)+1)
    
    plt.bar(x, av, width=0.35, align="center", yerr=sd, ecolor="red")
    plt.title("Users average score by question")
    plt.ylabel("Average users' score")
    plt.xlabel("Question number")
    plt.grid(True)
    plt.xticks(x)

    plt.show()










    

if __name__=="__main__":
        #make()
        users()
