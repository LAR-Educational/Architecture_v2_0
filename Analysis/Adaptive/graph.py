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
            
            if ("vector" in name):# and ([] in name):
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

    plt.xlim(0,4)





    plt.xlabel('Adaptive Window (t)')
    plt.ylabel('Value')
    plt.title('Adaptive Vectors')
    plt.grid(True)
    plt.savefig("test.png")
    plt.show()




def users():
    
    av = [6.3, 3.4, 6.4, 6.7, 5.6, 6.6, 5.7]
    sd = [1.059349905,	1.646545205,	0.9660917831,	0.6749485577,	0.8432740427,	0.6992058988,	1.059349905] 
    
    
    
    x =  range(1,len(av)+1)
    
    plt.bar(x, av, width=0.45, color = 'aqua', align="center", yerr=sd, ecolor="k")
    for i in x:
        plt.text(x[i-1]+0.1, av[i-1]+0.1, "{:.2f}".format(av[i-1]), fontsize=14 ) 

    plt.title("Users average score by question", fontsize=28)
    plt.ylabel("Average users' score", fontsize=16)
    plt.xlabel("Question number", fontsize=16)
    plt.gca().yaxis.grid(True)
    plt.xticks(x)
    plt.savefig("usersAnswers.png")
    plt.show()










    

if __name__=="__main__":
        make()
        #users()
