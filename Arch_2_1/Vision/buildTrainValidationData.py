
import os



dir="./Vision/preview/" #Original Directory
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
#for sp in shapes:
	
#Chance shape
print 'Starting data augmentatio in', 'dir.'	

filelist = os.listdir(dir)


#print len(filelist)

i=1

#'''
for filename in filelist:
	
	if i%10==0:
		os.rename(os.path.join(dir,filename), os.path.join('./Vision/validation', filename))
		#print "yes"
	else:
		os.rename(os.path.join(dir,filename), os.path.join('./Vision/train', filename))
		#print 'no'		
	i+=1


print 'Done!\n'	
#'''
