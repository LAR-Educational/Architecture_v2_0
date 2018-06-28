import numpy as np

def read_hist():
	arq = open("Activities/Historias/indices.txt" , "r")
	historiasfile = arq.read().split("\n")
	historiasfile = historiasfile[0:10]
	historias= []
	for x in xrange(0,3):
		r = np.random.randint(0,10)
		arq = open("Activities/Historias/" + historiasfile[r]+".txt" , "r")
		historias.append(arq.read().split("\n"))
		historias[x] = historias[x][0:len(historias[x])-1]
	return historias


teste = (read_hist())
print teste[2]
print teste[0]
print teste[1]