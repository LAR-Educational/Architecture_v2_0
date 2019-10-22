# -*- coding: utf-8 -*-
import os
import csv
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import time
from shutil import copyfile
#import pickle
import cPickle

#keras imports
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.callbacks import ModelCheckpoint
from keras import models

from cv2 import imread,imshow,resize, INTER_AREA, waitKey
import numpy as np



'''
Proccess sequence:

1 - collect data
2 - data aug in one path
3 - build directory tree for train/validation
4 - build batchs


'''
#from tensorflow.python.client import device_lib
#print(device_lib.list_local_devices())

input_shape = (320,240,3)

class CNN:
	
	def __init__(self, steps_per_epoch=1000, batch_size=16,	epochs=30, validation_percent = 10):
		self.steps_per_epoch=steps_per_epoch
		self.batch_size=batch_size
		self.epochs=epochs
		self.validation_percent = validation_percent 
		self.data_aug_check = False 
		self.tree_check = False

		
		
class Data_process:

	def __init__(self, activity_path):
		
		self.work_path = os.path.join(activity_path,"Vision")
		self.file_name = os.path.join(self.work_path ,".info")
		
		
		if os.path.exists(self.file_name):
			self.load()
			#print "SIM"
		else:
			self.classes = None
			self.min_dim = (0,0,0)
			self.im_width = -1
			self.im_heigh = -1
			self.im_dim= -1
			#print "NAO"
			self.save()

		# print self.work_path
		#print self.min_dim
		#print self.classes
		#self.cnn=cnn
		try:
			self.classes.sort()
		except:
			print "Problems in sorting list"
			print "Clasees: ", self.classes
			print "Work path: ", self.work_path
			classes = os.listdir(os.path.join(self.work_path,"Images"))
			self.classes = classes
			self.save()
			raise 
		
		self.save()


	def load(self):
		f = open(self.file_name, 'rb')
		tmp_dict = cPickle.load(f)
		f.close()

		#print tmp_dict          

		self.__dict__.update(tmp_dict) 


	def save(self):
		f = open(self.file_name, 'wb')
		cPickle.dump(self.__dict__, f, 2)
		f.close()


	def load_classes(self, file_name):

		with open(file_name, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in spamreader:
				return row
	


	def erase_database(self, path):
			
			if not os.path.exists(path):
				print "Path already deleted. Doing nothing in this function."
			#path = self.work_path
			#save old path
			#cwd = os.getcwd()
			
			#set to data dir
			#os.chdir(path)
			
			#remove files
			for root, dirs, files in os.walk(path):
				print "Erasing files in:", root
				for file in files:
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
		

		

		path = self.work_path
		
		classes = os.listdir(os.path.join(self.work_path,"Images"))
		self.classes = classes
		total_files = []
		
		self.data_aug_check=True
		
		# UNCOMENT HERE
		#return
		
		
		
		
		if os.path.exists(os.path.join(path,".Aug")):
			print " Data augmentation already performed .Aug exists"
			return
		
		else:
			os.mkdir(os.path.join(path,".Aug"))

		for cl in classes:
		
			print "\n-- Operatin in class ->", cl ,"<- --"
			#continue
			# aug_path = os.path.join(path, "train", cl)
			aug_path = os.path.join(path,"Images", cl)
			new_path = os.path.join(path,".Aug", cl)

			if not os.path.exists(new_path):
				os.mkdir(new_path)
		
		
			print '\nStarting data augmentation from', aug_path ,' to ', new_path
		
			# continue

			filelist = os.listdir(aug_path)
			#print "Working with", len(filelist), "original files."
		
			#return 1

			# w = -1
			# h = -1
			# d = -1
		
			#'''
			for filename in filelist:
		
				img = load_img(os.path.join(aug_path,filename))
				
				#print img 


				w= img.size[0]
				h= img.size[1]
				d= (3)

				#print w,h,d 

				#;return

				if self.im_width < w or	self.im_heigh < h :
					self.im_width = w
					self.im_heigh = h
					self.im_dim = d

				x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
				#img = load_img('data/train/cats/cat.0.jpg')  # this is a PIL image
				x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

				# the .flow() command below generates batches of randomly transformed images
				# and saves the results to the `preview/` directory
				i = 0
				#for batch in datagen.flow(x, batch_size=1, save_to_dir=aug_path, save_format='jpg'):
				for batch in datagen.flow(x, batch_size=1, save_to_dir=new_path, save_prefix=filename[0] , save_format='jpg'):
					i += 1
					if i > 20:
						break  # otherwise the generator would loop indefinitely
			#'''
			total_files.append(len( os.listdir(aug_path) ))
		
		print "FILE:", self.im_dim, self.im_heigh, self.im_width
		end = time.time()
		

		print '\nAug done!\n'	
		print "Done ", sum(total_files)," images in ", end-begin ," seconds\n"

		self.save()





	def buildTrainValidationData(self, validation_percent=10):	
		'''
		path_name= path to run the building
		validation_percent = percentage of samples in validation. Default 10%.
	
		'''
		path_name = self.work_path #"./data/collected" #Original Directory

		classes = os.listdir(os.path.join(path_name,"Images"))
		#self.classes = os.listdir(path_name)
		
		#return
		if not (set(classes) == set(self.classes)): #load_classes('shapes.csv') #['cub','pir','esf']
			print "Classes and Paths dont match!"
			return 0
		
		if self.im_width < 1 or self.im_heigh <1 :
			print "ERROR: Image width or heing is less than 1"
			return -1
		
		coll_path = os.path.join(path_name,".Aug")
		
		#print coll_path
		
		tr_path = os.path.join(path_name,".train")
		val_path = os.path.join(path_name,".validation")

		
		print "----- Starting Path Verification -----"

		# ---- Verifying Collected path	
		#if not os.path.exists(coll_path):
		#print self.data_aug_check

		if not self.data_aug_check:
			print "Path aug dosent exist. Please run data augmentation first."        
			#os.makedirs(aug_path)
			return False
		else:
			print "Data aug done"


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

		#return 0
		#print val_path


		print "\n----- Starting classes transfering -----\n"
	
		cl_index = 0
	

		for cl in classes:
		
		
			print "\n-- Operatin in class ->", cl ,"<- --"

			#continue 
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

	
			class_path = os.path.join(coll_path,cl)

			filelist = os.listdir(class_path)
		
		
			i=1

			for filename in filelist:
			
				#if filename[0] == str(cl_index):

				if i% (validation_percent) ==0:
					# -- Build class sample in validation path according to percentage
					#os.rename(os.path.join(aug_path, filename), os.path.join(val_path, cl , filename))
					copyfile(os.path.join(class_path, filename), os.path.join(val_path, cl , filename))
					#print (os.path.join(aug_path, filename), os.path.join(val_path, cl , filename))
					#print "yes"
				else:
					#os.rename(os.path.join(aug_path,filename), os.path.join(tr_path, cl , filename))
					copyfile(os.path.join(class_path,filename), os.path.join(tr_path, cl , filename))
					#print 'no'
				i+=1
				#'''
	
			cl_index += 1
			print "\nDone class ->", cl, "<- with:"
			print len(os.listdir(os.path.join(tr_path, cl))) , " samples in training path"	
			print len(os.listdir(os.path.join(val_path, cl))) , " samples in validation path\n"		

			print "Deleting .Aug folder"
			#self.erase_database(coll_path)

		return 1
	
	
# -----
	
	
	
	

	def generate_model(self,model_name='my_model', steps_per_epoch=1000, batch_size=16,	epochs=30, validation_percent = 10):
	
		path = self.work_path

		print "\n Train path:", os.path.join(path, '.train') , "\n"
		print "\n Validation path:", os.path.join(path, '.validation') , "\n"

		print os.listdir(os.path.join(path, '.train'))
		return 

		print "\n--- Initializing Network ---\n"

		model = Sequential()
		#model.add(Conv2D(32, (3, 3), input_shape=(150, 150,3)))
		model.add(Conv2D(32, (3, 3), input_shape=(self.im_width, self.im_heigh,3)))
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
		#self.classes = os.listdir(path+'/Images')
		#print self.classes
		#return
		model.add(Dense( len( self.classes)))
		model.add(Activation('softmax'))

		model.compile(loss='categorical_crossentropy',
				      optimizer='rmsprop',
				      metrics=['accuracy'])



		### ------------------ DATA

		print "\n--- Processing Data ---\n"

		#batch_size = cnn.batch_size

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
				os.path.join(path, '.train'),  # this is the target directory
				#target_size=(150, 150),  # all images will be resized to 150x150
				target_size=(self.im_width,self.im_heigh),  # all images will be resized to 150x150
				batch_size=batch_size,
				class_mode='categorical')  # since we use binary_crossentropy loss, we need binary labels

		# this is a similar generator, for validation data
		validation_generator = test_datagen.flow_from_directory(
				os.path.join(path, '.validation'),
				#target_size=(150, 150),
				target_size=(self.im_width, self.im_heigh),
				batch_size=batch_size,
				class_mode='categorical')



		#''''
		print "\n--- Starting Training ---\n"

		# checkpoint
		filepath= os.path.join(path, str(model_name)+".weights.best.hdf5")
		checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
		callbacks_list = [checkpoint]

		model.fit_generator(
				train_generator,
				steps_per_epoch= steps_per_epoch // batch_size,
				epochs= epochs,
				callbacks=callbacks_list,
				validation_data=validation_generator,
				#validation_data=train_generator,
				validation_steps=800 // batch_size)
				
				
				
		print "\n--- Saving Model ---\n"
				
		model.save(os.path.join(self.work_path, str(model_name) +'_model.h5'))        
				
		model.save_weights(os.path.join(self.work_path, str(model_name)+'_weights.h5'))  # always save your weights after training or during training
		'''

		wp ="Activities/as/Vision/test"
		#model=models.load_model(wp+"esfmodel.h5")
		
		#wp = wp+'test'
		for item in os.listdir(wp):
			#print item
			#continue


			img = imread(wp+"/"+item)
			#imshow("showw", img)
			#waitKey()
			#img = resize(img,(dp.im_width,dp.im_heigh))
			img = np.reshape(img,[1,self.im_width,self.im_heigh,3])
			
			classes = model.predict(img)
			#print classes  
			print item, (classes), self.classes[np.argmax(classes[0])]

		'''
		# ----------------------------- FINAL TUNING ----------------


	def print_work_path(self):
		print os.path.join(os.getcwd(),self.work_path)		

	def print_classes(self):
		print self.classes



	def save_best(self):
		model = models.load_model(os.path.join(self.work_path, "model.h5" ))
		model.load_weights(os.path.join(self.work_path, "weights.best.hdf5" ))
		model.save(os.path.join(self.work_path,'model.h5'))


	def class_path(self, folder_path, model):
		images = []
		for img in os.listdir(folder_path):
			name = img
			
			img = os.path.join(folder_path, img)
			img = load_img(img, target_size=(self.im_width, self.im_heigh))
			#img.show()
			#imshow("fig",img)
			#waitKey(0)
			img = img_to_array(img)
			img = np.expand_dims(img, axis=0)
			#images.append(img)
			#img = np.vstack(,img)
			#img = np.expand_dims(image, axis=0)
			#classes = model.predict(img, batch_size=1)
			# classes = model.predict(img, batch_size=1)
			# print name, self.classes, classes[0]

			y_prob = model.predict(img) 
			y_classes = y_prob.argmax(axis=-1)
			#print name, y_classes[0]
			# print y_prob[0], y_classes[0]
			print name, self.classes[y_classes[0]]
		# stack up images list to pass for prediction
		# images = np.vstack(images)
		# classes = model.predict_classes(images, batch_size=1)
		# print(classes)

		
def main():

	dp = Data_process("Activities/as")
	#dp.generate_model()
	#erase_database("./data/validation")
	#erase_database("./data/train")
	
	#dp.data_aug()		
	#dp.buildTrainValidationData()		
	
	#dp.generate_model()
	
	#dp.print_classes()
	
	wp ="Activities/as/Vision/"
	model=models.load_model(wp+"caca_model.h5")
	
	#dp.class_path(os.path.join(wp, 'test'), model)

	return 

	# wp = wp+'test'
	# for item in os.listdir(wp):
	# 	#print item
	# 	#continue


	# 	img = imread(wp+"/"+item)
	# 	#imshow("showw", img)
	# 	#waitKey()
	# 	#img = resize(img,(dp.im_width,dp.im_heigh))
	# 	img = np.reshape(img,[1,dp.im_width,dp.im_heigh,3])
	# 	pred = model.predict(img)
		
	# 	# y = img_to_array(img)
	# 	# q = np.expand_dims(y, axis=0)
	# 	# images = np.vstack([q])
	# 	# classes = model.predict(images)

	# 	#print classes  
	# 	print item, (pred), dp.classes[np.argmax(pred[0])]

	# #model.predict(test, batch_size=0, verbose=0)
    		
	# #print "DONE"
    # #raw_input("DONE")
    
    
    
    
if __name__ == "__main__":
    main()  	
		
