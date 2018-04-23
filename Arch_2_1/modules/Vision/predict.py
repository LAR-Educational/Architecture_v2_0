
from keras.models import Sequential
import keras.models
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing import image
import matplotlib.pyplot as mpl
import numpy as np
import time



#model = Sequential()

def load_model(model_name):
	''' function to load CNN model trained model'''
	
	model=keras.models.load_model(model_name)
	print "\n--- Model successfuly loaded ---\n"
	return model

#img_path = '/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/Vision/data/validation/cub/cub_0_300.jpg'


#img_path = '/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/Vision/data/validation/esf/esf_0_101.jpg'


def predict_from_path(model,img_path):

	img = image.load_img(img_path, target_size=(150, 150))

	x = image.img_to_array(img)
	x = x.reshape((1,) + x.shape)


	#print "\n--- Image successfuly loaded ---\n"

	#mpl.imshow(x) 
	#mpl.show()

	#print "\n--- Image successfuly showed ---\n"


	#cv2.waitKey()

	start=time.time()

	label = model.predict(x,batch_size=1,verbose=0)

	end=time.time()

	f=end-start


	#shapes= ['cubo','esfera','piramide']
	
	#predicted = shapes[np.argmax(label[0])]
	
	#print shapes
	
	#print label, "  Tempo: ", f , '\n\n'
	
	return label















