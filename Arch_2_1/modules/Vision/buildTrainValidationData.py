
import os


def erase_database(path):
	
	#save old path
	#cwd = os.getcwd()
	
	#set to data dir
	#os.chdir(path)
	
	#remove files
	for root, dirs, files in os.walk(path):
		for file in files:
		    print "Erasing file:", os.path.join(root,file)
		    os.remove(os.path.join(root,file))
	
	#back to the old dir
	#os.chdir(cwd)
	
	print "\nErase successfull\n"
	return True
	


def buildTrainValidationData(dir):	

	#dir="./data/collected" #Original Directory

	shapes = ['cub','pir','esf']

	'''
	datagen = ImageDataGenerator(
		    rotation_range=40,
		    width_shift_range=0.2,
		    height_shift_range=0.2,
		    rescale=1./255,
		    shear_range=0.2,
		    zoom_range=0.2,
		    horizontal_flip=True,
		    fill_mode='nearest')
	'''


	#Do data aug with all shapes
	
	for sh in shapes:
	
		#Chance shape
		print 'Building train/validation data in', sh	
		
		filelist = os.listdir(dir)
		
		#destiny_path = sp

		#print len(filelist)

		i=1

		#'''
		for filename in filelist:
	
			if sh in filename:
				
				#print "Found a", sh
				if i%10==0:
					os.rename(os.path.join(dir,filename), os.path.join('./data/validation/' + sh, filename))
					#print "yes"
				else:
					os.rename(os.path.join(dir,filename), os.path.join('./data/train/' + sh, filename))
					#print 'no'
				i+=1


		print 'Done!\n'	
		#'''
		
		
def main():


	erase_database("./data/validation")
	erase_database("./data/train")
	#buildTrainValidationData("./data/collected")		
		
		
		
		
		
		
		
		
		
		
    
if __name__ == "__main__":
    main()  	
		
