from threading import Thread
import time
import server
import emotion
import disatention
import client
import settings

class myThread(Thread):
	def __init__(self, name):
		Thread.__init__(self)
		self.name = name
		self.server = None
		self.emotion = None

	def run(self):
		if(self.name == 'server'):
			self.server = server.Server()
		
		elif(self.name == 'emotion'):
			self.emotion = emotion.EmotionClassifier()
			self.emotion.start()
		
		elif(self.name == 'desv_counter'):
			settings.info('Attention deviation thread being initialized')
			disatention.desv_counter(0)
		
		elif(self.name == 'desv_end'):
			settings.info('Attention deviation killer thread being initialized')
			disatention.desv_end('')


sv = myThread('server')
em = myThread('emotion')
desv_c = myThread('desv_counter')
desv_e = myThread('desv_end')

sv.start()
em.start()
desv_c.start()
desv_e.start()

c=client.Client()
time.sleep(2)
c.sendMessage('end of part')
time.sleep(2)
c.sendMessage('end of part')
time.sleep(2)
c.sendMessage('end of execution')

sv.join()
em.join()
desv_c.join()
desv_e.join()
