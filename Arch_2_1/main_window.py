#from PyQt4 import QtGui, QtCore # Import the PyQt4 module we'll need

from PyQt4.QtCore import *
from PyQt4.QtGui import *


#import PyQt4
import sys # We need sys so that we can pass argv to QApplication
import csv
import os
import cv2
import time
import numpy as np
import pandas as pd
from utils import *
	
#import utils
#from PyQt4.QtGui import *
 
import activities_Manager # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


from Modules import vars as core
from Modules import dialog as ds
#from Modules import motion as mt
#from Modules import vision #as vs
from Modules import emotion
from Modules.Vision import predict
from Modules.Vision import data_process #as dp
from Modules import content as ct
from Modules.userhandler import *

class SessionInfo:
	def __init__(self,initi_time,final_time):
		self.initi_time = initi_time
		self.final_time = final_time



# class PandasModel(QAbstractTableModel):
#     def __init__(self, data, parent=None):
#         QAbstractTableModel.__init__(self, parent)
#         self._data = data

#     def rowCount(self, parent=None):
#         return len(self._data.values)

#     def columnCount(self, parent=None):
#         return self._data.columns.size

#     def data(self, index, role=Qt.DisplayRole):
#         if index.isValid():
#             if role == Qt.DisplayRole:
#                 return QVariant(str(
#                     self._data.values[index.row()][index.column()]))
#         return QVariant()



class ExampleApp(QMainWindow, activities_Manager.Ui_MainWindow):
	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()

		self.setupUi(self)  # This is defined in design.py file automatically

		self.sys_vars = core.SystemVariablesControl()
		self.diag_sys = ds.DialogSystem(False, False)

		QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf8"))

		self.loadactButton.clicked.connect(self.load_file)
		self.exitButton.clicked.connect(self.close)
		self.insertQuestion_Button.clicked.connect(self.insertQuestion)
		self.loadQuestions_Button.clicked.connect(self.loadQuestions_fromFile)
		self.saveQuestions_Button.clicked.connect(self.saveQuestions_fromFile)
		self.reportLoadButton.clicked.connect(self.loadReportsCsv)
		self.writeReportButton.clicked.connect(self.writeReportCsv)
		
		self.recog_flag = False

		#--- Content panel
		self.content_path=None
		self.subs_list = []

		self.content_delete_button.clicked.connect(self.content_delet_topic)
		self.contenct_newSubj_button.clicked.connect(self.content_NewSubject)
		self.content_insert_question_button.clicked.connect(self.content_InsertQuestion)
		self.content_delete_question_button.clicked.connect(self.content_DeleteQuestion)
		self.content_saveSub_button.clicked.connect(self.content_save)
		self.content_subject_comboBox.currentIndexChanged.connect(self.content_update_tab)
		self.contenct_clear_questions_button.clicked.connect(self.content_clear_table)
		

		#--- Knowledge panel
		self.knowledge_path="./Data/"
		# DataFrames of General and Personal data
		self.know_gen_df=None
		self.know_gen_button_new.clicked.connect( lambda: insert_item_table(self.knowledge_general_table))
		self.know_gen_button_del.clicked.connect( lambda: delete_item_table(self.knowledge_general_table))
		self.know_gen_button_save.clicked.connect( lambda: save_table(self, self.knowledge_general_table,self.know_gen_df,self.knowledge_path+"general_knowledge.csv"))
		self.know_gen_button_load.clicked.connect( lambda: load_table(self, self.knowledge_general_table,self.know_gen_df,self.knowledge_path+"general_knowledge.csv"))

		self.know_per_df=None
		self.know_per_button_new.clicked.connect( lambda: insert_item_table(self.knowledge_personal_table))
		self.know_per_button_del.clicked.connect( lambda: delete_item_table(self.knowledge_personal_table))
		self.know_per_button_save.clicked.connect( lambda: save_table(self, self.knowledge_personal_table,self.know_per_df,self.knowledge_path+"personal_knowledge.csv"))
		self.know_per_button_load.clicked.connect( lambda: load_table(self, self.knowledge_personal_table,self.know_per_df,self.knowledge_path+"personal_knowledge.csv"))


		#--- Student
		
		self.students_database = UserDatabase()
		dataframe_to_table(self.students_database.index_table, self.st_db_index_table)
		self.user_new_button.clicked.connect( self.insert_user)
		self.user_cancel_button.clicked.connect( self.user_cancel)
		self.user_ok_button.clicked.connect( self.user_confirm_entry)
		self.user_del_button.clicked.connect( self.delete_user)
		self.user_open_table_button.clicked.connect( self.user_open)
		self.user_choose_pic_button.clicked.connect( self.user_choose_pic)


		#--- Plan and Run
		self.pushButton_run_activity.clicked.connect(self.start_display_image)
		self.pushButton_start_robot_view.clicked.connect(self.resume_display_image)
		self.pushButton_stop_robot_view.clicked.connect(self.stop_display_image)
		self.run_facerecog_pushButton.clicked.connect(self.run_facerecog)
		self.run_emotion_pushButton.clicked.connect(self.run_att_emo)
		self.run_load_pushButton.clicked.connect(self.run_load_models)
		self.run_takepic_pushButton.clicked.connect(self.run_takepic)
		#self.run_picname_lineEdit.textChanged.connect( lambda: self.line_edit_text_changed(self.run_picname_lineEdit,self.run_takepic_pushButton	 ))
		#self.run_videoname_lineEdit.textChanged.connect( lambda: self.line_edit_text_changed(self.run_videoname_lineEdit,self.run_recvid_button	 ))
		self.run_recvid_button.clicked.connect(self.run_start_recording_video)
		self.run_stopvid_button.clicked.connect(self.run_stop_recording_video)
		self.deviation_times=[]

		self.run_next_question_pushButton.clicked.connect(self.run_next_question)
		self.run_next_topic_pushButton.clicked.connect(self.run_next_concept)
		self.run_user_say_pushButton.clicked.connect(self.run_user_say)
		#run_next_topic_pushButton



		self.image=None
		
		# Define the codec and create VideoWriter object
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = None# cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
		self.run_record = False
		self.run_emotion_flag = False
		self.act = None #"/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content" #None
		self.qRow = 0
		self.qCol = 0


		self.model = QStandardItemModel(self)
		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)

		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.layoutVertical = QVBoxLayout(self)
		self.layoutVertical.addWidget(self.tableView)
		self.layoutVertical.addWidget(self.reportLoadButton)
		self.layoutVertical.addWidget(self.writeReportButton)
		
		







	def load_file(self):
		
		filename = QFileDialog.getOpenFileName(self, 'Open File', './Activities/NOVA')
		
		self.act=ct.load_Activity(filename)
		
		#self.name_lineEdit.setText(self.act.name)
		#self.desc_lineEdit.setText(self.act.description)		
		#self.path_lineEdit.setText(self.act.path)
		#self._lineEdit.setText(self.act.desc)
		self.editButton.setEnabled(True)
		self.modules_tabWidget.setEnabled(True)
		self.content_path = self.act.path +  "/Content" +"/"
		
		#self.sub_list = load_subjects(os.path.join(self.act.path,"Content","subjects"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.cvs"))
		#print self.sub_list
		#self.content_subject_comboBox.addItems(self.sub_list[1])

		self.content_load_subjects()


	def close(self):
		exit()
		#self.destroy()

	
	
	#------------------ DIALOG -----------------------------
	
	def insertQuestion(self):
		
		self.sysQuestionsTable.insertRow(self.qRow)
		self.sysQuestionsTable.setCurrentCell(self.qRow,0)
		#self.questions_tableWidget.setItem(0,0, QTableWidgetItem("TESTE"))
		self.qRow+=1
	
	
	
	def loadQuestions_fromFile(self):

		
		clearTable(self.sysQuestionsTable)
		
		
		fileName = self.act.path + "/Dialog/sys_questions.csv"
		self.qRow=0
		
		#print fileName

		#''' 
		with open(fileName, "rb") as fileInput:
			for item in csv.reader(fileInput):    
				#print item
				
				self.sysQuestionsTable.insertRow(self.qRow)
				self.sysQuestionsTable.setItem(self.qRow, 0, QTableWidgetItem(item[0]))
				self.sysQuestionsTable.setItem(self.qRow, 1, QTableWidgetItem(item[1]))
				self.qRow+=1
				
				#for field in row:
				#	print field
				
		#'''

	
	def saveQuestions_fromFile(self):						

		
		fileName = self.act.path + "/Dialog/questions.csv"
		
		#print fileName

		#''' 
		with open(fileName, "wb") as fileOutput:
			
			writer = csv.writer(fileOutput)
			for index in range(0,self.qRow):
	
	
				item = [
				self.sysQuestionsTable.item(index,0).text(),
				self.sysQuestionsTable.item(index,1).text()]
		
				print item[0], item [1]

				writer.writerow(item)
	
	

	
	
	
	
	def loadReportsCsv(self):

		with open('report.csv', "rb") as fileInput:
			for row in csv.reader(fileInput):    
				items = [
				    QStandardItem(field)
				    for field in row
				]
				self.model.appendRow(items)




	def writeReportCsv(self):
       
		with open('report.csv', "wb") as fileOutput:
			writer = csv.writer(fileOutput)
			for rowNumber in range(self.model.rowCount()):
				fields = [
				    self.model.data(
				        self.model.index(rowNumber, columnNumber),
				        Qt.DisplayRole
				    )
				    for columnNumber in range(self.model.columnCount())
				]
				writer.writerow(fields)
	
	




#------------------------ CONTENT -------------------------------------

	def content_NewSubject(self):

		
		while True:
			cont_name,  ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter new subject name:')
			if ok:
				# Check if the name already exists
				if (cont_name in self.sub_list['subjects'].tolist()):
					QMessageBox.critical(self, "Error!", "Subject already exists!\nChoose another name!", QMessageBox.Ok )
				else:		
					self.content_subject_comboBox.addItem(cont_name)
					self.sub_list.loc[len(self.sub_list.index)] = [cont_name,""]
					self.content_subject_comboBox.setCurrentIndex(self.content_subject_comboBox.count()-1)
					file_name = self.act.path +  "/Content/subjects.csv"
					self.sub_list.to_csv(file_name, index=False)



					break
			else:
				break		
	
		#self.content_saveSub_button.setEnabled(True)



	def content_save(self):
		#<<<<<<< HEAD
		#		file_name = self.act.path +  "/Content" +"/"+self.content_subject_comboBox.currentText()+".csv"

				#table_to_file(self.content_questions_table, file_name)
		#		sub_name = str(self.content_subject_comboBox.currentText())
		#		sub_conc = str(self.content_concept.toPlainText())
		#		self.sub_list.loc[self.content_subject_comboBox.currentIndex()] = [sub_name,sub_conc]
		#=======
		#>>>>>>> a6cb02fec78079ad08f4744019e0a6d9e90861eb
		
		ret = QMessageBox.question(self, "Saving Content!", "Are you sure you want to overwrite this content?", QMessageBox.Cancel | QMessageBox.Ok )
			
		if ret == QMessageBox.Ok:
			
			
			file_name = self.act.path +  "/Content" +"/"+self.content_subject_comboBox.currentText()+".csv"
			index_file =  self.act.path +  "/Content/subjects.csv"
			#table_to_file(self.content_questions_table, file_name)
			sub_name = str(self.content_subject_comboBox.currentText())
			sub_conc = str(self.content_concept.toPlainText())
			self.sub_list.loc[self.content_subject_comboBox.currentIndex()] = [sub_name,sub_conc]
			self.sub_list.to_csv(index_file, index=False)

			data = table_to_dataframe(self.content_questions_table)
			data.to_csv(file_name, index=False)

		"""
		#self.log("Subject saved at " + QDateTime.currentDateTime())

		return 1 


		#if (os.path.isfile(file_name)):
		if ():
			ret = QMessageBox.warning(self, "Warning!", "File already exist\nChose ther name", QMessageBox.Ok )

		else:
			ret = QMessageBox.warning(self, "Warning!", "File DO NOT exist\nWant to create it?", QMessageBox.Cancel | QMessageBox.Ok )
			
			if ret == QMessageBox.Cancel:
				print "CANCEL"


			if ret == QMessageBox.Ok:
				#print "Ok"
				cf = open(file_name,"w")
				cf.write(self.content_concept.toPlainText())
				cf.close()
		"""	

	def content_load_subjects(self):
		self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		self.content_subject_comboBox.addItems(self.sub_list['subjects'].tolist())
		self.content_update_tab()

	def content_update_tab(self):
		#text= self.sub_list['concepts'][self.sub_list['subjects'][self.sub_list['subjects']==str(self.content_subject_comboBox.currentText())].index[0]]
		text= str(self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()])
		
		self.content_concept.setText(text)
		file_name = str(self.content_path + self.content_subject_comboBox.currentText()+".csv")
		
		if os.path.isfile(file_name):
			data=pd.read_csv(file_name)
			#print "trying data", data

			dataframe_to_table(data,self.content_questions_table)

			self.log("Subject loaded: " + self.content_subject_comboBox.currentText())
			

		else:	
			self.log("WARNING TABLE <<"+file_name +">>  FILE DO NOT EXIST")
			labels = []
			for i in range(0,3):
				labels.append(str(self.content_questions_table.horizontalHeaderItem(i).text()))
			
			data = 	pd.DataFrame(columns=labels, index=range(0))

			#print data

			data.to_csv(self.content_path + self.content_subject_comboBox.currentText()+".csv", index=False)
			data.to_csv(file_name, index=False)



	def content_InsertQuestion(self):
		
		self.content_questions_table.insertRow(self.content_questions_table.rowCount())
		self.content_questions_table.setItem(self.content_questions_table.rowCount()-1,0, QTableWidgetItem(self.content_dif_comboBox.currentText()))
		
	
	def content_DeleteQuestion(self):
		
		index = self.content_questions_table.currentRow()
		#print index
		self.content_questions_table.removeRow(index)
		


	def content_clear_table(self):

		#data = table_to_dataframe(self.content_questions_table)
		data = pd.read_csv("/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content/subject2.csv")
		
		
		#print "RETRIEVED: "
		#print  data

		dataframe_to_table(data,self.content_questions_table)



	def content_delet_topic(self):

		#cont_name,  ok = QInputDialog.getText(self, 'Deleting Topic', 'Are you sure to delete this Topic?')
		ret = QMessageBox.warning(self, 'Deleting Topic', 'Are you sure to delete this Topic?', QMessageBox.Cancel | QMessageBox.Ok )
			
			# if ret == QMessageBox.Cancel:
			# 	print "CANCEL"


		if ret == QMessageBox.Ok:
		#if ok:
			cont_name = self.content_subject_comboBox.currentText()
			
			#print "index", self.content_subject_comboBox.currentIndex()

			#print self.sub_list

			#delete from RAM table
			#self.sub_list.drop(self.content_subject_comboBox.currentIndex())
			
			self.sub_list = self.sub_list[self.sub_list.subjects != cont_name]

			
			# Delete qestions table
			table_name = self.act.path +  "/Content/"+cont_name+".csv"
			os.remove(table_name)

			
			#Organizing index file
			file_name = self.act.path +  "/Content/subjects.csv"
			self.sub_list.to_csv(file_name, index=False)
			
			# Combo box updating
			self.content_subject_comboBox.removeItem(self.content_subject_comboBox.currentIndex())
			#self.content_subject_comboBox.setCurrentIndex(self.content_subject_comboBox.count()-1)
			self.log("Content <<" + cont_name + ">> deleted!")
			




#-------------------------------------------------- USER ----------------------------------------


	def insert_user(self):

		self.frame_18.setEnabled(False)
		self.user_frame.setEnabled(True)
		self.user_name_field.setEnabled(True)
		self.user_id_label.setText(str(self.sys_vars.users_id+1))
		#self.user_name_field.setFocus()
		self.user_creation_date.setDate(QDate.currentDate())
		self.user_bd_field.setDate(QDate.currentDate())
		
		#self.user_id_label.setText(str(user2show.id))
		#self.user_bd_field.setDate()
		self.user_name_field.setText("")
		self.user_last_name_field.setText("")
		self.user_school_year.setValue(0)
		self.user_image.setPixmap(QPixmap("GUI/user2.png"))
		#self.user_last_name_field.setText(str())
		#self.user_last_name_field.setText(str())
		#self.user_last_name_field.setText(str())

		self.user_sport.setText("")
		self.user_team.setText("")
		self.user_toy.setText("")
		self.user_game.setText("")
		self.user_dance.setText("")
		self.user_music.setText("")
		self.user_hobby.setText("")
		self.user_food.setText("")


		

	def delete_user(self):

		#print self.students_database.index_table[self.st_db_index_table.currentRow()]
		#print self.st_db_index_table.currentRow()

		# print self.students_database.users[self.st_db_index_table.currentRow()]
		user2kill = self.students_database.users[self.st_db_index_table.currentRow()]

		self.students_database.delete_user(user2kill)
		dataframe_to_table(self.students_database.index_table, self.st_db_index_table)



	def user_cancel(self):

		self.frame_18.setEnabled(True)
		self.user_frame.setEnabled(False)


		#self.log_text.setText(self.user_name_field.text())	
		
	# def __init__(self, id, first_name, last_name, bday='None',
    #             scholl_year='None', picture='None', preferences={}, img = None, creation_Date=None):
	
	# def setPreferences(self, sport='None', team='None', toy='None', game='None', 
    #                    dance='None', music='None', hobby='None', food='None'):

	def user_confirm_entry(self):
		
		
		#QPixmap qpix = self.user_image.pixmap()
		image = self.user_image.pixmap().toImage()
		
		print type (image)

		#img = cv2.Mat(image.rows(),image.cols(),CV_8UC3,image.scanline())
		img = qImageToMat(image)

		print type (img)

		#cv2.imshow("test",img)
		#cv2.waitKey(0)

		aux = User(int(self.user_id_label.text()),
			str(self.user_name_field.text()),
			str(self.user_last_name_field.text()),
			#str(self.user_bd_field.textFromDateTime("dd:mm:yyyy")),
			(self.user_bd_field.date()),
			str(self.user_school_year.text()),
			creation_date=self.user_creation_date.date())

		aux.setPreferences(
			self.user_sport.text(),
			self.user_team.text(),
			self.user_toy.text(),
			self.user_game.text(),
			self.user_dance.text(),
			self.user_music.text(),
			self.user_hobby.text(),
			self.user_food.text())

		if self.students_database.insert_user(aux)	> 0:
			self.sys_vars.add('user')
		
		dataframe_to_table(self.students_database.index_table, self.st_db_index_table)
		
		self.user_frame.setEnabled(False)
		self.frame_18.setEnabled(True)
		
	


	def user_open(self):

		#self.st_db_index_table.setEnabled(False)
		self.frame_18.setEnabled(False)
		self.user_name_field.setEnabled(True)
		
		self.user_frame.setEnabled(True)
		
		user2show = self.students_database.users[self.st_db_index_table.currentRow()]

		self.user_id_label.setText(str(user2show.id))
		#self.user_bd_field.setDate()
		self.user_name_field.setText(str(user2show.first_name))
		self.user_last_name_field.setText(str(user2show.last_name))
		#print user2show.bday
		#self.user_bd_field.setDate(QDate.fromString(user2show.bday,"dd/MM/yyyy"))
		#self.user_creation_date.setDate(QDate.fromString(user2show.creation_date,"dd/MM/yyyy"))
		self.user_bd_field.setDate(user2show.bday)
		self.user_creation_date.setDate(user2show.creation_date)
		#self.user_last_name_field.setText(str())
		#self.user_last_name_field.setText(str())
		#self.user_last_name_field.setText(str())

		self.user_sport.setText(user2show.preferences['sport'])
		self.user_team.setText(user2show.preferences['team'])
		self.user_toy.setText(user2show.preferences['toy'])
		self.user_game.setText(user2show.preferences['game'])
		self.user_dance.setText(user2show.preferences['dance'])
		self.user_music.setText(user2show.preferences['music'])
		self.user_hobby.setText(user2show.preferences['hobby'])
		self.user_food.setText(user2show.preferences['food'])

		self.log_text.setText(self.user_creation_date.date().toString('dd/MM/yyyy'))


	def user_choose_pic(self):

		filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
		img = QPixmap(filename)
		self.user_image.setPixmap(img)









#-------------------------------------------------- RUN ----------------------------------------

	def start_display_image(self):
		
		self.capture = cv2.VideoCapture(0)
		self.run_options_frame.setEnabled(True)
		self.pushButton_start_robot_view.setEnabled(True)
		self.pushButton_stop_robot_view.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(False)
		self.run_facerecog_pushButton.setEnabled(False)
		self.run_takepic_pushButton.setEnabled(True)
		self.run_recvid_button.setEnabled(True)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(5)

		self.clock_timer = QTimer()
		self.counter_timer = QTime()
		self.clock_timer.timeout.connect(self.showTime)
		self.clock_timer.start(1000)
		time = QTime.currentTime()
		#time = time.toString('hh:mm:ss') 
		self.cur_sess=SessionInfo(time,None)
		self.counter_timer.start()
		self.run_cont_interator = 0
		
		self.run_question_interator = -1

	def run_load_models(self):
		self.students_database.generate_encodings()
		self.run_facerecog_pushButton.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(True)
		self.emotion_classifier = emotion.Classifier()
		self.face_cascade = cv2.CascadeClassifier('Modules/haarcascade_frontalface_alt.xml')
		#self.faces = self.face_cascade.detectMultiScale(image_gray, 1.3, self.minNei_spinBox.value() )#minNeighbors=5)
		self.run_load_pushButton.setEnabled(False)

	def run_facerecog(self):
		self.recog_flag=True
		self.run_emotion_pushButton.setEnabled(False)


	def run_att_emo(self):
		self.run_emotion_flag=True
		self.run_facerecog_pushButton.setEnabled(False)
		self.n_deviations = self.time_disattention = 0
		# static measuring time, dynamic measuring time, time on atention, time for emotion classifier
		self.static_time = self.dynamic_time = self.time_attention = self.time_emotion = time.time()






	def run_takepic(self):
		name = "images/"+str(self.run_picname_lineEdit.text()) +".png"
		cv2.imwrite(name, self.image)
		self.log(name + " write")
		self.run_load_pushButton.setEnabled(True)
		#print name

	def run_start_recording_video(self):
		video_name = "Videos/"+ str(self.run_videoname_lineEdit.text())+".avi"
		self.out =  cv2.VideoWriter(video_name,self.fourcc, 20.0, (640,480))
		self.run_record = True 
		self.run_stopvid_button.setEnabled(True)


	def run_stop_recording_video(self):
		self.out.release()
		self.run_record = False

		
	def resume_display_image(self):
		self.pushButton_start_robot_view.setEnabled(False)
		self.pushButton_stop_robot_view.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(True)
		self.run_facerecog_pushButton.setEnabled(True)
		self.recog_flag = False
		self.run_emotion_flag = False
		self.timer.start(5)



	def update_frame(self):
		ret, self.image=self.capture.read()
		self.image = cv2.flip(self.image,1)
		#cv2.imshow("testwindow",self.image )
		#cv2.waitKey()

		if (self.recog_flag):
			self.image, name = self.students_database.face_recognition(self.image)
			if name:
				self.run_recognized_user_label.setText(name)

		if (self.run_emotion_flag):
			self.image = self.run_attention_emotion_thread(self.image)

		if(self.run_record):
			frame = self.image #cv2.flip(self.image,-1)
			self.out.write(frame)

		self.displayImage(self.image)









	def displayImage(self, img):
		qformat = QImage.Format_Indexed8
		if len(img.shape)==3:
				if img.shape[2]==4:
					qformat = QImage.Format_RGBA8888
				else :
					qformat = QImage.Format_RGB888
		
		outImage= QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
		outImage = outImage.rgbSwapped()

		self.img_from_cam.setPixmap(QPixmap.fromImage(outImage))
		#self.img_from_cam.setScaledContentes(True)


	def stop_display_image(self):
		self.pushButton_start_robot_view.setEnabled(True)
		self.pushButton_stop_robot_view.setEnabled(False)
		self.timer.stop()


	
	def run_attention_emotion_thread(self, image):
	
		
		# start some variables
		# number of deviations, time on disattention
		# n_deviations = time_disattention = 0
		# # static measuring time, dynamic measuring time, time on atention, time for emotion classifier
		# static_time = dynamic_time = time_attention = time_emotion = time.time()

		
		#arq = open('AttentionLogs/{:6.0f}all_statistics.dat'.format(time.time()), 'w');
	
		#info("All set. Obtaining images!")
		#c = open('emotion_imgs/classifications.txt', 'a+')
		face = None
	

		# convert image to grayscale			
		image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                                    

		# detect faces using Haar Cascade, last parameter: min_neighbors
		faces = self.face_cascade.detectMultiScale(image_gray, 1.3, self.minNei_spinBox.value() )#minNeighbors=5)

		# if no faces are detected, updates deviation time
		if len(faces) == 0:           
			#print "Here is a problem"         
			self.dynamic_time = time.time()

		# else, shows on screen the detected face, store the face on
		# a variable to be emotion-classified, and counts deviation time
		else:
			# runs through all faces found (expected only one, but runs on a loop just to be sure)
			for (x, y, w, h) in faces:
				# draws rectangle around the face
				cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
			
				# store the detected face with a few extra pixels, because
				# the cascade classifier cuts a litte too much
				face = image_gray[y-10:y+h+10, x-10:x+w+10]
			
				# if a time difference of 0.3 seconds is met, classify the emotion on a face
				self.time_diff = self.dynamic_time-self.time_emotion

				try:
					#print " 1"
					#if(time_diff >= 0.3 and face is not None):
					if( face is not None):
					
						#print "--2"
						#info("Face detected. Classifying emotion.")
						# reshape image to meet the input dimensions
						face_to_classify = np.stack([face, face, face], axis=2)
						face_to_classify = cv2.resize(face_to_classify, core.input_shape[:2], interpolation=cv2.INTER_AREA) * 1./255
						
						# get inference from classifier
						#classified_emotion = "nothing"
						classified_emotion = self.emotion_classifier.inference(face_to_classify)
						# writes emotion on the image, to be shown on screen
						#cv2.putText(image, classified_emotion, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)			
						# store image on a folder, for future analysis
						#cv2.imwrite("emotion_imgs/{}.png".format(dynamic_time), face)
						#c.write("{} {}\n".format(dynamic_time, classified_emotion))
						# reset time
						self.time_emotion = self.time_diff
						#core.info("Emotion classified: {}".format(classified_emotion))
						self.run_emotion_label.setText(classified_emotion)
						core.emotions[classified_emotion] += 1
				except Exception as e:
					print(e)
			# if the time difference meets a threshold, count it as a deviation
			self.diff = self.dynamic_time - self.static_time
			
			if self.diff > 0.7:
				# increase the number of deviations detected
				self.n_deviations += 1
				self.run_deviation_count.setText(str(self.n_deviations))
				# stores the time of this deviation
				#arq.write("Tempo do desvio: {:.2f}\n".format(diff))
				self.deviation_times.append(self.diff)
				#increases total disattention time
				self.time_disattention += self.diff
				core.info("Deviation detected")
			self.static_time = self.dynamic_time = time.time()

		return image


	def run_next_concept(self):

		if self.run_cont_interator < len(self.sub_list):
		#for i in self.run_cont_interator < len(self.sub_list):
			
			self.robot_say(self.sub_list['concepts'][self.run_cont_interator])

			self.run_current_topic.setText(self.sub_list['subjects'][self.run_cont_interator])

			file_name = str(self.content_path + self.sub_list['subjects'][self.run_cont_interator] +".csv")
			
			if os.path.isfile(file_name):
				self.run_current_topic_data =pd.read_csv(file_name)
			
			#self.robot_speech.setText(str(self.sub_list['concepts'][self.run_cont_interator]))

			self.run_cont_interator+=1


			self.run_question_number.setText(0)

		
		self.run_question_interator = -1


	def run_next_question(self):

		self.run_question_interator+=1
		if self.run_question_interator < len(self.run_current_topic_data.index):
		#for i in self.run_cont_interator < len(self.sub_list):
			
			# self.robot_speech.setText(str(   ))

			# file_name = str(self.content_path + self.sub_list['subjects'][self.run_cont_interator] +".csv")
			
			# if os.path.isfile(file_name):
			# 	self.run_current_topic_data =pd.read_csv(file_name)
			
			self.robot_say( self.run_current_topic_data['Question'][self.run_question_interator] )
			self.run_question_number.setText(str(self.run_question_interator+1))






	def run_user_say(self):
		
		user_answer = str(self.run_user_answer.text())
		expected_answer = str(self.run_current_topic_data['Expected Answer'][self.run_question_interator])

		dist =  str(self.diag_sys.levenshtein_long_two_strings(user_answer,expected_answer))
		
		# print "user", user_answer
		# print "ex", expected_answer
		# print "dist", dist
		# print
		
		self.run_correctness.setText(dist)
		self.log(dist)








	
	### ------------ CLOCK

	def showTime(self):
		time = QTime.currentTime()
		duration = self.counter_timer.elapsed()
		sec = (duration/1000) % 60
		min = int(duration/60000)
		text = str(min).zfill(2)+':'+str(sec).zfill(2)
		if (sec %2 ) == 0:
			text = text[:2] + ' ' + text[3:]
		self.clock_display.setText(text)
		
		
	# ### -------------------------- Knowledge ----------------------

	# def know_new(self, table):
	# 	#self.knowledge_general_table.insertRow(self.knowledge_general_table.rowCount())
	# 	table.insertRow(table.rowCount())
	
	# def know_del(self, table):
	# 	#index = table.currentRow()
	# 	#print index
	# 	table.removeRow(table.currentRow())



























### -------------------------- Class Utils ----------------------


	def log(self, text):
		
		time = QTime.currentTime()

		self.log_text.setText( time.toString("hh:mm:ss") +"  -->  "+ text ) 



	def robot_say(self, text):

		self.robot_speech.setText(str(  text ))



	@pyqtSlot(str)
	def line_edit_text_changed(self, line, button):
		if line.text:  # Check to see if text is filled in
			button.setEnabled(True)
		else:
			button.setEnabled(False)

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main() # run the main function
