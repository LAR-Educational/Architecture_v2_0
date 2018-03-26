
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img



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
		




def data_aug(path):
    '''
        Data augmentation
        Parameter: Path with train and validation directories
    '''
    aug_path = os.path.join(path,"aug")
    
    print 
    
    print "Working in diractory", os.getcwd()  + aug_path  
    
    if not os.path.exists(aug_path):
        print " exist"        
        os.makedirs(aug_path)
    
    
    #return True    
    
    #path="./Vision/alldb/" #Original Directory
    shapes = ['cub','pir','esf']
    
    
    datagen = ImageDataGenerator(
            rotation_range=40,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest')
    
    
    
    #Do data aug with all shapes
    #for sp in shapes:

    #Chance shape
    print 'Starting data augmentatio in', sp, 'dir.'	
    filelist = os.listdir(path)

    for filename in filelist:
        img = load_img(os.path.join(path,sp,filename))
        #img = load_img('data/train/cats/cat.0.jpg')  # this is a PIL image
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

        # the .flow() command below generates batches of randomly transformed images
        # and saves the results to the `preview/` directory
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir='./Vision/preview', save_prefix=sp, save_format='jpg'):
        i += 1
        if i > 20:
            break  # otherwise the generator would loop indefinitely
        
        print 'Dir', sp, 'done!\n'	
    
    
    
    

def img2batch():
        
    batch_size = 16
    
    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
    
    # this is the augmentation configuration we will use for testing:
    # only rescaling
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # this is a generator that will read pictures found in
    # subfolers of 'data/train', and indefinitely generate
    # batches of augmented image data
    train_generator = train_datagen.flow_from_directory(
            'data/train',  # this is the target directory
            target_size=(150, 150),  # all images will be resized to 150x150
            batch_size=batch_size,
            class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels
    
    # this is a similar generator, for validation data
    validation_generator = test_datagen.flow_from_directory(
            'data/validation',
            target_size=(150, 150),
            batch_size=batch_size,
            class_mode='binary')





















		
def main():

    
    #erase_database("./data/validation")
    #erase_database("./data/train")
    #buildTrainValidationData("./data/collected")		
    
    data_aug("./data")		
    		
    		
    #print "DONE"
    raw_input("DONE")
    
if __name__ == "__main__":
    main()  	
		