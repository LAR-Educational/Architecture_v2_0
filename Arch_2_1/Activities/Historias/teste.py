import numpy as np

def read_hist():
	arq = open("Activities/Historias/indices.txt" , "r")
	historiasfile = arq.read().split("\n")
	historiasfile = historiasfile[0:10]
	historias= []
	for x in xrange(0,2):
		r = np.random.randint(0,2)
		arq = open("Activities/Historias/" + historiasfile[r] , "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])-1]
	return historias


print(read_hist())