


import os

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img




odir="./Vision/alldb/" #Original Directory
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
for sp in shapes:
	
	#Chance shape
	print 'Starting data augmentatio in', sp, 'dir.'	
	filelist = os.listdir(os.path.join(odir,sp))

	for filename in filelist:
		img = load_img(os.path.join(odir,sp,filename))
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



