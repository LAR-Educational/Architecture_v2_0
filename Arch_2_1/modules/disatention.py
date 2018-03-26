import cv2
import numpy as np
import time
from threading import Thread
import vision as vs
import os
import sys
import vars
from naoqi import ALProxy


# subscribe top camera
AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13


string = 'rodando'
flag = True


class Th(Thread):

	def __init__ (self, num):
		Thread.__init__(self)
		self.num = num

	def run(self):
		if self.num == 1:
			desv_counter(0)
			
		elif self.num == 2:
			desv_end()

def desv_end():

	global string

	string = 'sair'


        #global flag
        
        #flag = False
        
        
        
        

#funcao que conta os desvios, retorna o numero de desvios, o tempo perdido em desatencao e o tempo em atencao
def desv_counter(camId):

	global string
        
        global flag
        
        nameId = vars.camera.subscribeCamera("Disatention_Counter", camId, AL_kQVGA, AL_kBGRColorSpace, 10)
        print "Subscribed in ", nameId
    


	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')     #xml necessario para a classificacao 
	
	#print "Path: ", os.getcwd() + "/modules/haarcascade_frontalface_alt.xml"
	
	#cap = cv2.VideoCapture(webcam_code)                                                 
	counter_face = time_face_disatention = 0
	t0 = t1 = time_atention = time.time()

	arq = open('all_statistics.dat', 'a');
	


	while True:#(flag):
	      
	        result = vars.camera.getImageRemote(nameId)
                #create image
                width = result[0]
                height = result[1]
                image = np.zeros((height, width, 3), np.uint8)

                # get image
                result = vars.camera.getImageRemote(nameId)

                '''if result == None:
                print 'cannot capture.'
                elif result[6] == None:
                print 'no image data string.'
                else:
                '''
                
                # translate value to mat
                values = map(ord, list(result[6]))
                i = 0
                for y in range(0, height):
                    for x in range(0, width):
                        image.itemset((y, x, 0), values[i + 0])
                        image.itemset((y, x, 1), values[i + 1])
                        image.itemset((y, x, 2), values[i + 2])
                        i += 3
                        
                # show image
                #cv2.imshow("NAO's Vision top-camera-320x240", image)
                    
                # exit by [ESC]
                        
                #key=cv2.waitKey(1)        
                #        if cv2.waitKey(1) == 27:
                #            break
                #        

	        cv2.imshow('Original',image)
	
		img = image                       #capturando os frames da imagem
		
		#cv2.imshow("", img)
		#cv2.waitKey(0)
										
		face_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    
		faces = face_cascade.detectMultiScale(face_gray, 1.3, 3) #ultimo parametro -> min neighbors
	
		if len(faces) == 0:     				#caso nao tenha faces atualizo o tempo                    
			t1 = time.time()
	
		else:

			for(x, y, w, h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

			if t1-t0 > 0.7:								#se o tempo for maior que um valor conto desvio
				counter_face = counter_face + 1				
				str1 = "Tempo do desvio: "+ "%.2f" %(t1-t0) + "\n"
				arq.write(str1)
				time_face_disatention += t1-t0
			t0 = t1 = time.time()
	
		cv2.imshow('img',img)
                #cv2.waitKey(1)
                
		if cv2.waitKey(1) and string == 'sair':
	                break;

	#cap.release()
	cv2.destroyAllWindows()
	
	vars.camera.unsubscribe(nameId)

	time_atention = time.time() - time_atention - time_face_disatention
	str1 = "Total de desvios: " + "%d" %counter_face + ", tempo total de desvios: " + "%.2f" %time_face_disatention + ", tempo em atencao: " + "%.2f" %time_atention + "\n"
	arq.write(str1)			#escrita em arquivos dos dados
	arq.close()
        
        if counter_face >= 2:
                vars.attention = False
        
        
	arq_ret = open('statistics.dat', 'w');			#escrita no segundo arquivo de dados
	str2 = "%d" %counter_face + "\n" + "%.2f" %time_face_disatention + "\n" + "%.2f" %time_atention + "\n"
	arq_ret.write(str2)
	arq_ret.close()
	string = 'rodando'

