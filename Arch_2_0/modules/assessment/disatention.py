import cv2
import numpy as np
import time
from threading import Thread

string = 'rodando'

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

#funcao que conta os desvios, retorna o numero de desvios, o tempo perdido em desatencao e o tempo em atencao
def desv_counter(webcam_code):

	global string

	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')     #xml necessario para a classificacao 
	
	cap = cv2.VideoCapture(webcam_code)                                                 
	counter_face = time_face_disatention = i = 0
	t0 = t1 = counter = time_atention = time.time()

	arq = open('all_statistics.dat', 'a');
	
	while (True):
	
		ret, img = cap.read()                       #capturando os frames da imagem
		
		if time.time() - counter > 1:
			#cv2.imwrite(str(i)+'.jpg', img)			#salvando frames para a funcao classificacao de imagem
			i = i+1
			counter = time.time()
										
		face_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                                    
		faces = face_cascade.detectMultiScale(face_gray, 1.3, 5)
	
		if len(faces) == 0:     				#caso nao tenha faces atualizo o tempo                    
			t1 = time.time()
	
		else:

			for(x, y, w, h) in faces:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

			if t1-t0 > 0.3:								#se o tempo for maior que 0.3 conto desvio
				counter_face = counter_face + 1				
				str1 = "Tempo do desvio: "+ "%.2f" %(t1-t0) + "\n"
				arq.write(str1)
				time_face_disatention += t1-t0
			t0 = t1 = time.time()
	
		cv2.imshow('img',img)

		if cv2.waitKey(1) and string == 'sair':
			break;

	cap.release()
	cv2.destroyAllWindows()

	time_atention = time.time() - time_atention - time_face_disatention
	str1 = "Total de desvios: " + "%d" %counter_face + ", tempo total de desvios: " + "%.2f" %time_face_disatention + ", tempo em atencao: " + "%.2f" %time_atention + "\n"
	arq.write(str1)			#escrita em arquivos dos dados
	arq.close()

	arq_ret = open('statistics.dat', 'w');			#escrita no segundo arquivo de dados
	str2 = "%d" %counter_face + "\n" + "%.2f" %time_face_disatention + "\n" + "%.2f" %time_atention + "\n"
	arq_ret.write(str2)
	arq_ret.close()

