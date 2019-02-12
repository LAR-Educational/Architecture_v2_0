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

    x = range(1, 4)# len(f)+1)

    #print x


    plt.plot(x,alpha, label='Alpha')
    plt.plot(x,beta, label='Beta')
    plt.plot(x,gama, label='Gama')
    plt.plot(x,f, label='Fadap', linewidth=5)

    #plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.legend(bbox_to_anchor=(1,1), loc =1)

    plt.xlim(0.5,3.5)





    plt.xticks(x)
    plt.xlabel('Adaptive Window (t)')
    plt.ylabel('Value')
    plt.title('Adaptive Vectors', fontsize=20)
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




def make_from_path():
	
	path = "measures.csv" 
	

	data = genfromtxt(path, delimiter=',', skip_header=1)
	#print data

	#data = np.transpose(data)
	print data[:3]
	
	#for i in range(0,len(data[0])):
	



	x = range(1,4)
	#plt.subplot(121)

   	plt.title("Indicators evolution", fontsize=20)
    	plt.ylabel("Value", fontsize=14)
    	plt.xlabel("Instant t", fontsize=14)
	
	#plt.plot(x, data[:,0]/30, label = "Deviations * 10e-10")
	plt.plot(x, data[:,1]/125, label = "Bad emotions count")
	plt.plot(x, data[:,2]/11, label = "Spoken words")
	plt.plot(x, 1-data[:,3], label = "Success rate")
	plt.plot(x, data[:,4]/40, label = "Time to answer")
	
    	
	
	plt.xlim(0.5,3.5)
	
	
	plt.legend(bbox_to_anchor=(1, 1), loc=1)#, borderaxespad=0.)
	plt.grid(True)
	plt.xticks(x)
	plt.savefig("indicators2.png")
	plt.show()



def emo_prefs():
	
	sport = [0,	1.777777778,	0.6666666667,	31.22222222,	13,	0.4444444444,	0.6666666667]
	food = [0,	1.555555556,	0.1111111111,	14.22222222,	4.777777778,	0.3333333333,	0.1111111111]
	music = [0,	2.555555556,	0,	9.444444444,	5,	0.1111111111,	0]

	ssd = [0,	2.773886163,	1.658312395,	4.002430,	2.00694311,	0.7264831573,	1.414213562]
	fsd = [0,	3.574601765,	0.3333333333,	12.7747581,	7.758507875,	0.7071067812,	0.3333333333]
	msd = [0,	5.570258322,	0,				12.1151879,	8.845903006,	0.3333333333,	0]


	fig, ax = plt.subplots()
	
	index = np.arange(len(sport)) #0,8)
	
	
	
	bar_width = 0.25

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	print len(sport)


	rects1 = ax.bar(index, sport, bar_width,
		            alpha=opacity, color='b',
		            yerr=ssd, error_kw=error_config,
		            label='Sport')

	rects2 = ax.bar(index + bar_width, food, bar_width,
		            alpha=opacity, color='r',
		            yerr=fsd, error_kw=error_config,
		            label='Food')
	#'''
	rects3 = ax.bar(index + 2*bar_width, music, bar_width,
		            alpha=opacity, color='g',
		            yerr=msd, error_kw=error_config,
		            label='Music')
	#'''
	
	ax.set_xlabel('Emotions labels')
	ax.set_ylabel('Emotion count')
	ax.set_title('Emotions detected by preferences')
	ax.set_xticks(index + bar_width / 2)
	ax.set_xticklabels(('Angry', 'Disgusting', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise'))
	ax.legend()
	plt.plot()
	fig.tight_layout()
	plt.savefig("emos_pref.png")
	
	plt.show()


def GUI_teach_test():

    av = [3.555555556,	3.777777778,	3.444444444,	3.777777778,	3.888888889,	3.111111111,	3.555555556,	3.333333333]
    sd = [1.013793755,	0.9718253158,	0.8819171037,	0.8333333333,	0.6009252126,	0.6009252126,	0.7264831573,	0.8660254038] 
    
    
    
    x =  range(1,len(av)+1)
    
    plt.bar(x, av, width=0.45, color = 'aquamarine', align="center", yerr=sd, ecolor="k")
    for i in x:
        plt.text(x[i-1]+0.1, av[i-1]+0.1, "{:.2f}".format(av[i-1]), fontsize=14 ) 

    plt.title("Teachers' Answer", fontsize=28)
    plt.ylabel("Average teachers' score", fontsize=16)
    plt.xlabel("Question number", fontsize=16)
    #plt.gca().yaxis.grid(True)
    plt.xticks(x)
    plt.savefig("teachers.png")
    plt.show()


if __name__=="__main__":
    #emo_prefs()
    #make_from_path()
    #users()
	#make()
    GUI_teach_test()
