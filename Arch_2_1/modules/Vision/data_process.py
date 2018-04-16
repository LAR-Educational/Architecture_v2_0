# -*- coding: utf-8 -*-
import os
import csv
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import time
from shutil import copyfile

#keras imports
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.callbacks import ModelCheckpoint





'''
Proccess sequence:

1 - collect data
2 - data aug in one path
3 - build directory tree for train/validation
4 - build batchs


'''


class Data_process:

	def __init__(self, work_path):
		self.work_path = work_path
		self.classes = self.load_classes(os.path.join(work_path, "file_classes.csv"))
		


	def load_classes(self, file_name):

		with open(file_name, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in spamreader:
				return row
	


	def erase_database(self):
			
			path = self.work_path
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
			









	def data_aug(self):
		'''
		    Data augmentation
		    Parameter: Path with train and validation directories
		'''
		
		path = self.work_path
		classes = self.classes
		total_files = []
		
		   
		datagen = ImageDataGenerator(
		        rotation_range=40,
		        width_shift_range=0.2,
		        height_shift_range=0.2,
		        rescale=1./255,
		        shear_range=0.2,
		        zoom_range=0.2,
		        horizontal_flip=True,
		        fill_mode='nearest')
		
		print '\nTake a book... it could take a while' 
		begin = time.time()
		
		
		for cl in classes:
		
			print "\n-- Operatin in class ->", cl ,"<- --"
			
			aug_path = os.path.join(path, "train", cl)
		
		
		
			print '\nStarting data augmentation in', aug_path 
			
			filelist = os.listdir(aug_path)
			#print "Working with", len(filelist), "original files."
		
			#return 1
		
		
			#'''
			for filename in filelist:
		
				img = load_img(os.path.join(aug_path,filename))
				#img = load_img('data/train/cats/cat.0.jpg')  # this is a PIL image
				x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
				x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

				# the .flow() command below generates batches of randomly transformed images
				# and saves the results to the `preview/` directory
				i = 0
				#for batch in datagen.flow(x, batch_size=1, save_to_dir=aug_path, save_format='jpg'):
				for batch in datagen.flow(x, batch_size=1, save_to_dir=aug_path, save_prefix=filename[0] , save_format='jpg'):
					i += 1
					if i > 20:
						break  # otherwise the generator would loop indefinitely
			#'''
			total_files.append(len( os.listdir(aug_path) ))
		
		
		end = time.time()
		    
		print '\nAug done!\n'	
		print "Done ", sum(total_files)," images in ", end-begin ," seconds\n"

		





	def buildTrainValidationData(self, validation_percent=10):	
		'''
		dir= path to run the building
		validation_percent = percentage of samples in validation. Default 10%.
	
		'''

		dir = self.work_path #"./data/collected" #Original Directory

		classes = self.classes #load_classes('shapes.csv') #['cub','pir','esf']

		coll_path = os.path.join(dir,"collected")
		tr_path = os.path.join(dir,"train")
		val_path = os.path.join(dir,"validation")


		print "----- Starting Path Verification -----"

		# ---- Verifying Collected path	
		if not os.path.exists(coll_path):
			print "Path aug dosent exist"        
			#os.makedirs(aug_path)
			return False
		else:
			print "Collected path found!", coll_path


		# ---- Verifying Train path
		if not os.path.exists(tr_path):
			print "Creating train path!"        
			os.makedirs(tr_path)

		else:
			print "Train path found in ", tr_path


		# ---- Verifying Validation path
		if not os.path.exists(val_path):
			print "Creating validation path!"        
			os.makedirs(val_path)

		else:
			print "Validation path found in ", val_path



		print "\n----- Starting classes transfering -----\n"
	
		cl_index = 0
	
		for cl in classes:
		
		
			print "\n-- Operatin in class ->", cl ,"<- --"
		
			cl_tr_path = os.path.join(tr_path, cl)
			cl_val_path = os.path.join(val_path, cl)

			# --- Train class verification		
			if not os.path.exists(cl_tr_path):
				print "Creating class ->", cl, "<- in training path!"        
				os.makedirs(cl_tr_path)

			else:
				print "Train path for class ->", cl,"<- already exists"


			# --- Validation class verification
			if not os.path.exists(cl_val_path):
				print "Creating class ->", cl, "<- in validation path!"        
				os.makedirs(cl_val_path)

			else:
				print "Validation path for class ->", cl, "<- already exists"

	
	
			filelist = os.listdir(coll_path)
		
		
			i=1

			for filename in filelist:
			
				if filename[0] == str(cl_index):

					if i% (validation_percent) ==0:
						# -- Build class sample in validation path according to percentage
						#os.rename(os.path.join(aug_path, filename), os.path.join(val_path, cl , filename))
						copyfile(os.path.join(coll_path, filename), os.path.join(val_path, cl , filename))
						#print (os.path.join(aug_path, filename), os.path.join(val_path, cl , filename))
						#print "yes"
					else:
						#os.rename(os.path.join(aug_path,filename), os.path.join(tr_path, cl , filename))
						copyfile(os.path.join(coll_path,filename), os.path.join(tr_path, cl , filename))
						#print 'no'
					i+=1
					#'''
		
			cl_index += 1
			print "\nDone class ->", cl, "<- with:"
			print len(os.listdir(os.path.join(tr_path, cl))) , " samples in training path"	
			print len(os.listdir(os.path.join(val_path, cl))) , " samples in validation path\n"		

	

		return 1
	
	
	
	
	
	

	def generate_model(self):
	
		path = self.work_path

		print "\n Train path:", os.path.join(path, 'train') , "\n"
		print "\n Validation path:", os.path.join(path, 'validation') , "\n"

		print "\n--- Initializing Network ---\n"

		model = Sequential()
		model.add(Conv2D(32, (3, 3), input_shape=(150, 150,3)))
		model.add(Activation('relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))

		model.add(Conv2D(32, (3, 3)))
		model.add(Activation('relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))

		model.add(Conv2D(64, (3, 3)))
		model.add(Activation('relu'))
		model.add(MaxPooling2D(pool_size=(2, 2)))


		model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
		model.add(Dense(64))
		model.add(Activation('relu'))
		model.add(Dropout(0.5))
	
		#number of classes
	
		model.add(Dense( len( self.classes)))
		model.add(Activation('sigmoid'))

		model.compile(loss='categorical_crossentropy',
				      optimizer='rmsprop',
				      metrics=['accuracy'])



		### ------------------ DATA

		print "\n--- Processing Data ---\n"

		batch_size = 20

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
				os.path.join(path, 'train'),  # this is the target directory
				target_size=(150, 150),  # all images will be resized to 150x150
				batch_size=batch_size,
				class_mode='categorical')  # since we use binary_crossentropy loss, we need binary labels

		# this is a similar generator, for validation data
		validation_generator = test_datagen.flow_from_directory(
				os.path.join(path, 'validation'),
				target_size=(150, 150),
				batch_size=batch_size,
				class_mode='categorical')



		#''''
		print "\n--- Starting Training ---\n"

		# checkpoint
		filepath= os.path.join(path,"weights.best.hdf5")
		checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
		callbacks_list = [checkpoint]

		model.fit_generator(
				train_generator,
				steps_per_epoch=1000 // batch_size,
				epochs=25,
				callbacks=callbacks_list,
				validation_data=validation_generator,
				validation_steps=800 // batch_size)
				
				
				
		print "\n--- Saving Model ---\n"
				
		model.save(os.path.join(self.work_path,'model.h5'))        
				
		model.save_weights(os.path.join(self.work_path,'weights.h5'))  # always save your weights after training or during training
		#'''



		# ----------------------------- FINAL TUNING ----------------


	def print_work_path(self):
		print os.path.join(os.getcwd(),self.work_path)		

	def print_classes(self):
		print self.classes


		
def main():

	dp = Data_process("data/garrafa_carteira")
    
	#erase_database("./data/validation")
	#erase_database("./data/train")
	#dp.buildTrainValidationData()		
	#dp.data_aug()		
	
	dp.generate_model()
	
	#dp.print_classes()
	
	
    		
    		
	print "DONE"
    #raw_input("DONE")
    
    
    
    
if __name__ == "__main__":
    main()  	
		
