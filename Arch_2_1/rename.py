




import os


print "Starting"


dir = "./data/collected"
#pattern = "*.jpg"
#titlePattern

filenames = os.listdir(dir)

print filenames

i=0

for fn in filenames:
	
	print fn
	
	#newname= "cub"+str(i)+".jpg"
	#os.rename(os.path.join(dir,fn),os.path.join(dir,newname))
	#print "Converting ", os.path.join(dir,fn), ' to ', os.path.join(dir,newname)
	i+=1


#rename(r'/Vision/alldb/0',r'*.jpg',r'cube')


print "Done"
















