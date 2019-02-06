#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import random
import threading
#from datetime import datetime
#import utils
	
#from PyQt4.QtGui import *
 
import activities_Manager # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


from Modules import vars as core
from Modules import dialog #as ds
#from Modules import motion as mt
from Modules import vision #as vs
from Modules import emotion
from Modules.Vision import predict
from Modules.Vision import data_process #as dp
from Modules import content as ct
from Modules import adaption
from Modules.userhandler import *
from Modules.evaluationhandler import *
from Modules.interactionhandler import *
from Modules.Memory import searchwiki  



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



class MainApp(QMainWindow, activities_Manager.Ui_MainWindow):
	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()

		self.setupUi(self)  # This is defined in design.py file automatically



		# GENERAL!!

		self.robot = None
		self.vs= None
		#self.ds=None


		self.sys_vars = core.SystemVariablesControl()
		self.diag_sys = dialog.DialogSystem(False, False)

		#self.sys_vars.add('user')


		QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf8"))

		self.loadactButton.clicked.connect(self.load_file)
		self.exitButton.clicked.connect(self.close)
		self.insertQuestion_Button.clicked.connect(self.insertQuestion)
		self.loadQuestions_Button.clicked.connect(self.loadQuestions_fromFile)
		self.saveQuestions_Button.clicked.connect(self.saveQuestions_fromFile)
		self.reportLoadButton.clicked.connect(self.loadReportsCsv)
		self.writeReportButton.clicked.connect(self.writeReportCsv)
		
		self.recog_flag = False
		
		
		# --- General
		self.supervisor ="admin"
		self.cur_user = None
		
		# --- Dialog

		self.answer_threshold = 1 - self.diag_dist_thres_spinBox.value()
		#print "Thres valeu", self.answer_threshold



		#--- Vision panel





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
		
		
		#--- Adaptive 
		self.user_profile = 3

		#self.emotions = adaption.emotions
		# self.w = adaption.Weights()
		# self.op_par = adaption.OperationalParameters()
		# self.read_values=adaption.ReadValues()




		#--- Knowledge panel
		self.knowledge_path="./Data/"
		# DataFrames of General and Personal data
		self.know_gen_df=None
		self.knowledge_general_df = pd.read_csv( "Data/general_knowledge.csv" , sep="|", encoding='utf-8')
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
		
		if os.path.exists("Usuarios"):
			dataframe_to_table(self.students_database.index_table, self.st_db_index_table)

		self.user_new_button.clicked.connect( self.insert_user)
		self.user_cancel_button.clicked.connect( self.user_cancel)
		self.user_ok_button.clicked.connect( self.user_confirm_entry)
		self.user_del_button.clicked.connect( self.delete_user)
		self.user_open_table_button.clicked.connect( self.user_open)
		self.user_choose_pic_button.clicked.connect( self.user_choose_pic)
		self.user_aux_img = None



		#--- Evaluation
		self.cur_eval = None#Evaluation()
		self.evaluation_db = EvaluationDatabase()
		if os.path.exists("Evaluations"):
			dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)
		
		self.eval_open_button.clicked.connect( self.eval_open)
		self.eval_delete_button.clicked.connect( self.delete_eval)
		self.eval_topic_comboBox.currentIndexChanged.connect(self.eval_update_tab)
		self.eval_questions_comboBox.currentIndexChanged.connect(self.eval_update_tab)
		self.eval_att_comboBox.currentIndexChanged.connect(self.eval_update_tab)


		#--- Interaction

		self.int_enable = False
		self.int_create_button.clicked.connect(self.int_create)
		self.int_cancel_button.clicked.connect(self.int_cancel_action)
		self.int_add_cont_button.clicked.connect(self.int_add_cont_action)
		self.int_add_per_button.clicked.connect(self.int_add_per_action)
		self.int_add_extra_button.clicked.connect(self.int_add_extra_action)
		self.int_save_button.clicked.connect(self.int_save_action)
		self.int_load_button.clicked.connect(self.int_load_action)

		self.int_lock_button.clicked.connect(self.int_lock_action)
		
		
		#--- Plan and Run
		self.pushButton_run_activity.clicked.connect(self.start_activity)
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
		self.run_robot_connect_button.clicked.connect(self.run_connect_robot_action)
		self.deviation_times=[]

		self.run_next_question_pushButton.clicked.connect(self.run_next_question)
		self.run_next_topic_pushButton.clicked.connect(self.run_next_concept)
		self.run_user_say_pushButton.clicked.connect(self.run_user_say)
		self.run_end_activity_button.clicked.connect(self.run_end_activity)
		
		#run_next_topic_pushButton
		self.user_ans_flag=False


		self.image=None
		# Define the codec and create VideoWriter object
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = None# cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
		self.run_record = False
		self.run_emotion_flag = False

		self.act = None #ct.load_Activity("./Activities/NOVA/activity.data")#None #"/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content" #None
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
		
		
		#Shortcuts:
		self.load_file()
		#self.int_load_action()
		#self.int_lock_action()





	def load_file(self):
		
		#filename = QFileDialog.getOpenFileName(self, 'Open File', './Activities/NOVA')
		#self.act=ct.load_Activity(filename)
		
		self.act=ct.load_Activity("./Activities/NOVA/activity.data")#None #"/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content" #None
		
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

		self.interact_database = InteractionDatabase(self.act.path)
		


	def close(self):
		if self.robot is not None:
			self.vis_sys.unsub(0)
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
					clearTable(self.content_questions_table)
		


					break
			else:
				break		
	
		#self.content_saveSub_button.setEnabled(True)



	def content_save(self):
		
		ret = QMessageBox.question(self, "Saving Content!", "Are you sure you want to overwrite this content?", QMessageBox.Cancel | QMessageBox.Ok )
			
		if ret == QMessageBox.Ok:
			
			
			file_name = self.act.path +  "/Content" +"/"+self.content_subject_comboBox.currentText()+".csv"
			index_file =  self.act.path +  "/Content/subjects.csv"
			#table_to_file(self.content_questions_table, file_name)
			sub_name = str(self.content_subject_comboBox.currentText())
			sub_conc = str(self.content_concept.toPlainText().toUtf8())#encode('utf-8')
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
		self.content_questions_table.setItem(self.content_questions_table.rowCount()-1,0, QTableWidgetItem(str(self.content_dif_comboBox.currentIndex()+1)))
		
	
	def content_DeleteQuestion(self):
		
		index = self.content_questions_table.currentRow()
		#print index
		self.content_questions_table.removeRow(index)
		


	def content_clear_table(self):

		#data = table_to_dataframe(self.content_questions_table)
		#data = pd.read_csv("/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content/subject2.csv")
		
		clearTable(self.content_questions_table)
		
		#print "RETRIEVED: "
		#print  data

		#dataframe_to_table(data,self.content_questions_table)



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
			




#-------------------------------------------------- KNOWLEDGE ----------------------------------------


	def know_add_information(self, concept):

		core.info("Inside add informatiion")

		#definition = search_engine(concept)
		
		definition = searchwiki.search(concept)

		tt= self.diag_sys.coutingWords(definition)

		if tt > 25:
			frases = definition.split(".")
			frase_final = frases[0] +"." + frases[1]+ "."

			definition = frase_final

		
		if definition =='':
			core.war("String returned is EMPTY")
			return None

		else:
			size = len(self.knowledge_general_df.index)

			self.knowledge_general_df.loc[size]=[concept, definition]

			#print self.knowledge_general_df.loc[size]

			self.knowledge_general_df.to_csv("Data/general_knowledge.csv" , sep="|", encoding='utf-8', index=False) 
			
			dataframe_to_table(self.knowledge_general_df, self.knowledge_general_table)

			return definition













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
		
	# def __init__(self, id, first_name, last_name, bday='None',self.emotions
    #             scholl_year='None', picture='None', preferences={}, img = None, creation_Date=None):
	
	# def setPreferences(self, sport='None', team='None', toy='None', game='None', 
    #                    dance='None', music='None', hobby='None', food='None'):

	
	
	
	def user_confirm_entry(self):
		
		self.emotions
		#QPixmap qpix = self.user_image.pixmap()
		image = self.user_image.pixmap().toImage()
		
		#print type (image)

		#img = cv2.Mat(image.rows(),image.cols(),CV_8UC3,image.scanline())
		
		try:
			print "try"
			img = qImageToMat(image)
			
		except Exception as e:
			print "Exception", e

		#print type (img)

		#cv2.imshow("test",img)
		#cv2.waitKey(0)

		aux = User(int(self.user_id_label.text()),
			str(self.user_name_field.text()),
			str(self.user_last_name_field.text()),
			#str(self.user_bd_field.textFromDateTime("dd:mm:yyyy")),
			bday=(self.user_bd_field.date()),
			scholl_year=str(self.user_school_year.text()),
			img=img,
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
		
		# Get the user in the selected row of the users table
		user2show = self.students_database.users[self.st_db_index_table.currentRow()]

		self.user_id_label.setText(str(user2show.id))
		#self.user_bd_field.setDate()self.emotions
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

		#aux_pic = "Usuarios/18014/Daniel.png"
		aux_pic = "Usuarios/"+ str(user2show.id) +"/"+str(user2show.id) +".png"
		
		#print"PIC NAME",  aux_pic

		if os.path.exists(aux_pic):
			self.user_image.setPixmap( QPixmap(aux_pic))
			#print "YES"
			#self.user_image.setPixmap(cvmat_to_qimg(img))
		else:
			self.user_image.setPixmap( QPixmap("GUI/user2.png"))
			#print "NO"
			#pass

		# filename = QFileDialog.getOpenFileName(self, 'Open File', './images')
		
		# #print filename

		# img = cv2.imread(str(filename))
		
		# self.user_aux_img = img

		# self.user_image.setPixmap(cvmat_to_qimg(img))




	def user_choose_pic(self):

		filename = QFileDialog.getOpenFileName(self, 'Open File', './images')
		
		#print filename

		img = cv2.imread(str(filename))
		
		self.user_aux_img = img

		self.user_image.setPixmap(cvmat_to_qimg(img))






#-------------------------------------------------- EVAL ----------------------------------------


	# def insert_user(self):

	# 	self.frame_18.setEnabled(False)
	# 	self.user_frame.setEnabled(True)
	# 	self.user_name_field.setEnabled(True)
	# 	self.user_id_label.setText(str(self.sys_vars.users_id+1))
	# 	#self.user_name_field.setFocus()
	# 	self.user_creation_date.setDate(QDate.currentDate())
	# 	self.user_bd_field.setDate(QDate.currentDate())
		
	# 	#self.user_id_label.setText(str(user2show.id))
	# 	#self.user_bd_field.setDate()
	# 	self.user_name_field.setText("")
	# 	self.user_last_name_field.setText("")
	# 	self.user_school_year.setValue(0)
	# 	self.user_image.setPixmap(QPixmap("GUI/user2.png"))
	# 	#self.user_last_name_field.setText(str())
	# 	#self.user_last_name_field.setText(str())
	# 	#self.user_last_name_field.setText(str())

	# 	self.user_sport.setText("")
	# 	self.user_team.setText("")
	# 	self.user_toy.setText("")
	# 	self.user_game.setText("")
	# 	self.user_dance.setText("")
	# 	self.user_music.setText("")
	# 	self.user_hobby.setText("")
	# 	self.user_food.setText("")


		

	def delete_eval(self):

		#print self.students_database.index_table[self.st_db_index_table.currentRow()]
		#print self.st_db_index_table.currentRow()

		# print self.students_database.users[self.st_db_index_table.currentRow()]
		eval2kill = self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()]

		self.evaluation_db.delete_eval(eval2kill)
		dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)

	

	def eval_cancel(self):

		self.frame_26.setEnabled(True)
		self.eval_frame.setEnabled(False)


		#self.log_text.setText(self.user_name_field.text())	
		
	# def __init__(self, id, first_name, last_name, bday='None',
    #             scholl_year='None', picture='None', preferences={}, img = None, creation_Date=None):
	
	# def setPreferences(self, sport='None', team='None', toy='None', game='None', 
    #                    dance='None', music='None', hobby='None', food='None'):

	
	
	
	'''def eval_confirm_entry(self):
		
		
		
		aux = Evaluation(int(self.eval_id_label.text()),
			(self.eval_date.date()),
			(self.eval_user_id_label.text()),
			self.eval_user_name.text(),
			#str(self.user_bd_field.textFromDateTime("dd:mm:yyyy")),
			self.eval_duration.time(),
			self.eval_start.time(),

			
			)

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
	'''
	


	def eval_open(self):

		#self.st_db_index_table.setEnabled(False)
		self.frame_26.setEnabled(False)
		self.eval_frame.setEnabled(True)
		
		#self.user_frame.setEnabled(True)
		
		# Get the user in the selected row of the users table
		self.cur_eval = self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()]


		self.eval_user_id_label.setText(str(self.cur_eval.user_id))
		self.eval_date.setDate(self.cur_eval.date)#QDate.fromString(self.cur_eval.date.toString(),"dd.MM.yyyy"))
		#self.eval_duration.setTime(self.cur_eval.duration)
		self.eval_start.setTime(self.cur_eval.start_time)
		self.eval_end.setTime(self.cur_eval.end_time)
		self.eval_supervisor.setText(self.cur_eval.supervisor)
		self.eval_user_name.setText(self.cur_eval.user_name)
		#self.eval_concept_textField.setText(self.cur_eval.concept)
		self.eval_last_dif.setText(str(self.cur_eval.user_dif_profile))
		if(len(self.cur_eval.topics)==0):
			print "ERROR: Topics empty"
		
		else:

			#print self.cur_eval.tp_names



			self.eval_topic_comboBox.addItems(self.cur_eval.tp_names)

			index_list = range(1,len(self.cur_eval.topics[0].questions))

			index_list=["{}".format(x) for x in index_list]

			self.eval_questions_comboBox.addItems(index_list)

			index_list = range(1,len(self.cur_eval.topics[0].questions[0].attempts))

			index_list=["{}".format(x) for x in index_list]

			self.eval_att_comboBox.addItems(index_list)

			#Ideia: Fazer um listner para os 3 combobox para atulizar o Topics validation tab

			#self.eval_quest_lineEdit.setText(self.cur_eval.topics[])

			self.eval_update_tab()




		

		self.log_text.setText(self.eval_date.date().toString('dd/MM/yyyy') + " Opened eval of date:")




	def eval_update_tab(self):
		
		#text= str(self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()])
		
		tp_id=self.eval_topic_comboBox.currentIndex()
		qt_id=self.eval_questions_comboBox.currentIndex()
		att_id=self.eval_att_comboBox.currentIndex()

		aux_att = self.cur_eval.topics[tp_id].questions[qt_id].attempts[att_id] #Attempt()

		self.eval_concept_textField.setText(self.cur_eval.topics[tp_id].concept)
		self.eval_quest_lineEdit.setText(self.cur_eval.topics[tp_id].questions[qt_id].question )
		self.eval_exp_lineEdit.setText(self.cur_eval.topics[tp_id].questions[qt_id].exp_ans )
		self.eval_gave_ans_lineEdit.setText(self.cur_eval.topics[tp_id].questions[qt_id].attempts[att_id].given_ans )
		self.eval_time2ans.setTime(QTime.fromString(str(aux_att.time2ans),"mm:ss"))
		self.eval_ans_sup_comboBox.setCurrentIndex(aux_att.supervisor_consideration) 
		self.eval_ans_sys_comboBox.setCurrentIndex(aux_att.system_consideration) 
		self.eval_sys_was_comboBox.setCurrentIndex(aux_att.sytem_was) 





		# self.content_concept.setText(text)
		# file_name = str(self.content_path + self.content_subject_comboBox.currentText()+".csv")
		
		# if os.path.isfile(file_name):
		# 	data=pd.read_csv(file_name)
		# 	#print "trying data", data

		# 	dataframe_to_table(data,self.content_questions_table)

		# 	self.log("Subject loaded: " + self.content_subject_comboBox.currentText())
			

		# else:	
		# 	self.log("WARNING TABLE <<"+file_name +">>  FILE DO NOT EXIST")
		# 	labels = []
		# 	for i in range(0,3):
		# 		labels.append(str(self.content_questions_table.horizontalHeaderItem(i).text()))
			
		# 	data = 	pd.DataFrame(columns=labels, index=range(0))

		# 	#print data

		# 	data.to_csv(self.content_path + self.content_subject_comboBox.currentText()+".csv", index=False)
		# 	data.to_csv(file_name, index=False)







#-------------------------------------------------- INTERACTION ----------------------------------------



	def int_change_enable(self):

		if self.int_enable:
			self.int_enable=False
		else:
			self.int_enable=True

		self.int_cont_frame.setEnabled(self.int_enable)
		self.int_per_frame.setEnabled(self.int_enable)
		self.int_tl_frame.setEnabled(self.int_enable)
		self.int_extra_frame.setEnabled(self.int_enable)
		self.int_gen_frame.setEnabled(self.int_enable)
		#self.int_timeline_table.setEnabled(self.int_enable)



	def int_cancel_action(self):
		self.int_create_button.setEnabled(True)
		self.int_load_button.setEnabled(True)
		self.int_change_enable()


	def int_create(self):
		
		self.int_load_button.setEnabled(False)
		self.int_create_button.setEnabled(False)
		self.int_cancel_button.setEnabled(True)
		self.int_change_enable()

		self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		self.int_cont_comboBox.addItems(self.sub_list['subjects'].tolist())

		path = os.path.join(self.act.path, "Interactions" )
		
		if not os.path.exists(path):
			os.mkdir(path)
		
		self.int_id_show.setText(str(self.sys_vars.interaction_id))

	
	def int_load_action(self):
		
		aux_path = self.act.path+"/"+"Interactions"
		
		if len(os.listdir(aux_path)) == 0:

			QMessageBox.information(self, 'Loading Interations',"No Interactions saved" ,QMessageBox.Ok)

			return 0



		#/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Interactions
		filename = QFileDialog.getOpenFileName(self, 'Open File' ,self.act.path+"/"+"Interactions")
		
		#filename = self.act.path+"/"+"Interactions/1.int"

		interact = self.interact_database.load_interact(filename)

		self.int_load_button.setEnabled(False)
		self.int_create_button.setEnabled(False)
		self.int_cancel_button.setEnabled(True)
		self.int_change_enable()



		self.int_ques_per_top.setValue(interact.ques_per_topic)
		self.int_att_per_ques.setValue(interact.att_per_ques)
		self.int_name_linedit.setText(interact.name)
		dataframe_to_table(interact.data, self.int_timeline_table)


	
		self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		self.int_cont_comboBox.addItems(self.sub_list['subjects'].tolist())




	def int_save_action(self):

		data = table_to_dataframe(self.int_timeline_table)
		#data.to_csv()

		#print self.int_ques_per_top.value()

		self.cur_interact = Interaction(0,
											self.int_ques_per_top.value(),
											self.int_att_per_ques.value(),
											self.int_name_linedit.text(),
											data=data
												)

		self.interact_database.save_interact(
						self.cur_interact,
						self.interact_database.path+"/"+str(self.int_name_linedit.text())+ ".int"
						)




	def int_lock_action(self):
		
		self.int_save_action()
		self.int_change_enable()

		self.pushButton_run_activity.setEnabled(True)
		self.run_int_name_label.setText(self.cur_interact.name)
		self.modules_tabWidget.setCurrentIndex(9)

	def int_add_cont_action(self):

		self.int_timeline_table.insertRow(self.int_timeline_table.rowCount())		

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				0,
				QTableWidgetItem("Content"))

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				1,
				QTableWidgetItem(self.int_cont_comboBox.currentText()))						


	def int_add_per_action(self):
		
		self.int_timeline_table.insertRow(self.int_timeline_table.rowCount())		

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				0,
				QTableWidgetItem("Personal"))

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				1,
				QTableWidgetItem(self.int_per_comboBox.currentText()))						




	def int_add_extra_action(self):
		
		self.int_timeline_table.insertRow(self.int_timeline_table.rowCount())		

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				0,
				QTableWidgetItem("Extra"))

		self.int_timeline_table.setItem(
				self.int_timeline_table.rowCount()-1,
				1,
				QTableWidgetItem(self.int_extra_comboBox.currentText()))						




















#-------------------------------------------------- RUN ----------------------------------------

	def start_activity(self):
		
		if self.robot is None:
			self.capture = cv2.VideoCapture(0)

			if not self.capture.isOpened():
				QMessageBox.critical(self, "ERROR!", " Unable to open camera!", QMessageBox.Ok)
				
				self.interatction_parser()
				
				
				return -1
			
		self.cur_eval =  Evaluation(
								id=self.sys_vars.evaluation_id,
								date=QDate.currentDate(),
								start_time=QTime.currentTime(),
								supervisor=self.supervisor 	
								)

		self.run_options_frame.setEnabled(True)
		self.pushButton_start_robot_view.setEnabled(True)
		self.pushButton_stop_robot_view.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(False)
		self.run_facerecog_pushButton.setEnabled(False)
		self.run_takepic_pushButton.setEnabled(True)
		self.run_recvid_button.setEnabled(True)

		self.adapt_sys.out_path = str(self.cur_eval.id)
		
		self.user_profile=3
		
		self.run_att_emo()

		# self.timer = QTimer(self)
		# self.timer.timeout.connect(self.update_frame)
		# self.timer.start(5)

		# self.clock_timer = QTimer()
		# self.counter_timer = QTime()
		# self.clock_timer.timeout.connect(self.showTime)
		# self.clock_timer.start(1000)
		# time = QTime.currentTime()
		# #time = time.toString('hh:mm:ss') 
		# self.cur_sess=SessionInfo(time,None)
		# self.counter_timer.start()
		#if self.robot is not None:
		#	self.vis_sys.subscribe(0)
		
		self.run_cont_interator = 0
		
		self.run_question_interator = -1

		self.robot.motors.wakeUp()
			

		
		# Não conehce
		self.interact_know_person()
		
		#Já conhece
		#self.interact_recognize_person()
		
		# Start interaction engine
		self.interatction_parser()




	def run_end_activity(self):
		
		if self.robot is not None:
			self.vis_sys.unsub(0)

		self.timer.stop()

		#self.cur_eval.
		#self.cur_eval.
		#self.cur_eval.
		
		self.cur_eval.end_time=QTime.currentTime()
		self.cur_eval.user_name = (self.cur_user.first_name) + " "+ (self.cur_user.last_name)
		self.cur_eval.user_dif_profile = self.user_profile

		if self.evaluation_db.insert_eval(self.cur_eval) > 0:
			self.sys_vars.add('evaluation')
		
		
		# self.modules_tabWidget.setCurrentIndex(7)

		dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)



	def run_connect_robot_action(self):
		
		robot_ip = str(self.run_robot_ip_comboBox.currentText())
		robot_port = int(self.run_robot_port.text())
		self.robot=core.Robot(robot_ip, robot_port)

		self.vis_sys = vision.VisionSystem(self.robot)
		self.diag_sys = dialog.DialogSystem(self.robot, None)
		
		
		#self.w = adaption.Weights(self.alfaWeight.value(),
		#						self.betaWeight.value(),
		#						self.gamaWeight.value())
		
		self.w = adaption.Weights(0,
								0,
								self.gamaWeight.value())

		
		# Não esta pegando do painel do adaptavtio algumas coisas!!!
		self.op_par = adaption.OperationalParameters(
										self.face_dev_activation.value(),
										self.negEmoAct__spinBox.value(),
										3, #number of words
										self.learningTime_doubleSpinBox.value(),
										1)

		
		self.read_values=adaption.ReadValues()

		self.adapt_sys = adaption.AdaptiveSystem(
			self.robot,
			self.op_par,
			self.w,
			self.read_values)
			#str(self.cur_eval.id))
		
		
		core.info("Loading Models!")
		self.run_load_models()
		
		self.diag_sys.say("Estou Pronto.", False)
		core.info("Robot Connected")

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
		if self.robot is not None:
			self.vis_sys.subscribe(0)


	def interatction_parser(self):

		# core.info("Wait image load")
		# for i in range(0,10):
		# 	QCoreApplication.processEvents()
		# core.info("Done Wait ")

		# Não conehce ainda
		#self.interact_know_person()

		

		cmds = len(self.cur_interact.data.index)
		
		#print len(self.cur_interact.data.index)

		#print self.cur_interact.data

		print "TYPE ", type(self.cur_interact.data.iloc[0]['Type'])

		for i in range(0,cmds):
			core.info("Inside parser " + str(i) + "  " + self.cur_interact.data.iloc[i]['Type'])
			

			self.run_phase.setText(QString.fromUtf8(self.cur_interact.data.iloc[i]['Name']))

			if self.cur_interact.data.iloc[i]['Type'] == "Content":
				self.content_interac_template(self.cur_interact.data.iloc[i]['Name'])

			if self.cur_interact.data.iloc[i]['Type'] == "Personal":
				print "Personal", self.cur_interact.data.iloc[i]['Name']
				self.personal_interact_talk(self.cur_interact.data.iloc[i]['Name'])

			if self.cur_interact.data.iloc[i]['Type'] == "Extra":
				print "Extra: ", self.cur_interact.data.iloc[i]['Name']
				#self.extra_interact(self.cur_interact.data.iloc[i]['Name'])

			print "\n\n\n"

		self.run_final_dialog()		
		self.run_end_activity()	






	def personal_interact_talk(self, talk_subject):

		core.info("Inside personal interact")

		talk_subject = str(talk_subject).lower()

		pref  = self.cur_user.preferences[talk_subject]

		#print pref 
		x = random.randint(0,1)

		if x >0:
			self.robot_say("Vamos conversar um pouco.")
		else:
			self.robot_say("Deixa eu te conhecer melhor")

		#não tem cadastrado ainda
		if pref == "":
			self.robot_say(personal_translate[talk_subject])
			pref = self.user_input().decode('utf-8')
			self.cur_user.add_preference(talk_subject, pref)
			self.students_database.insert_user(self.cur_user)
			core.info("USER UPDATED")

		# Já tem cadastrado
		else:
			#print type(pref)
			if type(pref) is QString:
				#print "TRUE"
				pref = str(pref.toUtf8())

			pref = pref.decode('utf-8').strip()
			pref = pref.encode('utf-8')

			self.robot_say("Você gosta de " + pref )
			
		concept_list = [ x.encode('utf-8')for x in self.knowledge_general_df['Concept'].tolist() ]
		
		

		if pref in concept_list:	
			self.robot_say("Eu sei o que é isso!")
			ind = concept_list.index(pref)	
			
			#tosay = u' '.join(self.knowledge_general_df['Definition'][ind]).encode('utf-8')
			tosay = (self.knowledge_general_df['Definition'][ind]).encode('utf-8')
			
			#print "STRING" ,tosay,  type(tosay)
			#print	

			self.robot_say((tosay))
		
		else:
			self.robot_say("Só um momento. Eu não conheço nada sobre isso ainda. Vou pesquisar na internet!", False)
			
			tosay=self.know_add_information(pref) 
			
			if tosay is not None:
				self.robot_say("Pronto!")
				self.robot_say(tosay.encode('utf-8'))
			else:
				self.robot_say("Não consegui encontrar nada sobre isso. Vou procurar melhor e depois te falo")	

		self.robot_say("Porque você gosta disso?")
		self.user_input()


	def interact_recognize_person(self):
		self.students_database.generate_encodings()
		#self.recog_flag=True
		self.cur_user = None

		while self.cur_user is None:

			if self.image is not None:
				self.image, self.recog_user_id = self.students_database.face_recognition(self.image)
					
				self.cur_user= self.students_database.get_user(self.recog_user_id)
					
				if self.cur_user is not None:
					self.run_recognized_user_label.setText(self.cur_user.first_name)
					self.log("USER DETECTED")

				else:
					QCoreApplication.processEvents()

					self.log("USER NOT DETECTED")
			else:
				QCoreApplication.processEvents()
				core.war("Image is None")

		#self.recog_flag=False
		




	def interact_know_person(self):
		
		self.robot_say("Olá amiguinho. Nós ainda não nos conhecemos. Eu me chamo Tédi.") 
		
		
		self.robot_say("Qual seu nome?", False)
		name = self.user_input()#.decode('utf-8')

		self.robot_say("E seu Sobrenome?", False)
		last_name = self.user_input()#.decode('utf-8')

		
		self.cur_user = User(self.sys_vars.users_id+1,
						name,
						last_name,
						bday=QDate.currentDate(),
						img=self.image,
						creation_date=QDate.currentDate())


		self.cur_user.setPreferences()

		if self.students_database.insert_user(self.cur_user)	> 0:
			self.sys_vars.add('user')

		self.log("User " + name + " added!")

		self.robot_say("Certo. Muito prazer, " + name)
		self.robot_say("Vamos começar as atividades")








	#recieve the Topic To Approach (tta)
	def content_interac_template(self, tta):

		
		core.info("INSIDE CONTENT FUNCTON " + tta)
		#print self.sub_list


		core.info("Initializing emotion thread")
		self.run_emotion_flag = True

		ind = self.sub_list[self.sub_list['subjects']==tta].index[0]
		
		text = self.sub_list['concepts'].iloc[ind]
		


		#print str(text)
		topic = Topic(text)
		self.cur_eval.tp_names.append(str(tta))
		att = Attempt(time2ans=0)
		#print "Concept", topic.concept

		self.robot_say(text)


		# Load the table with questions and expected answers
		file_name = str(self.content_path + tta +".csv")
		
		#if os.path.isfile(file_name):

		try:	
			data=pd.read_csv(file_name)
			#print "Data\n\n", data
		except:
			raise
			
		quest = Question()
		# Start the loop for the question number of the interaction
		for i in range(0,self.cur_interact.ques_per_topic):
			

			core.info("Question number: " + str(i))
			core.war("PROFILE :" + str(self.user_profile))
			# Select the possibilities according to the user profile detected
			dfp= data.loc[data['Difficulty'] == self.user_profile]
			possibilities = len(data.loc[data['Difficulty'] == self.user_profile])#['Question']

			#Reset the index of resulting possibilities (Original will overflow dataframe)
			dfp=dfp.reset_index(drop=True)

			#print"Index after", dfp.index
			#Randomly choose a question in possibilities range
			rand = random.randint(0, possibilities-1)

			# attribute variables
			chosen_question = str(dfp.loc[rand]['Question'])
			expected_answer = str(dfp.loc[rand]['Expected Answer'])

			# Store the raffled question and exp answer
			quest.question=chosen_question			
			quest.exp_ans=expected_answer




			#Loop for attempt
			for j in range(0, self.cur_interact.att_per_ques):

				#print "Question:", chosen_question
				self.robot_say(chosen_question)
				print "Exp: ", expected_answer

				t1 = time.time()

				self.run_exp_ans.setText(expected_answer)

				# Wait for the user answer: Change to verbal answer soon
				# while not self.user_ans_flag:
					
				# 	#self.label_132.setText(str(time.time("hh:mm:ss")))
				# 	QCoreApplication.processEvents()
				# 	#time.sleep(0.05)

				# self.user_ans_flag = False



				# Get user answer from GUI
				user_answer = self.user_input()

				#clear textedit
				self.run_user_answer.clear()

				#print "User ans: ", user_answer

				# Calculate answer similarity
				dist =  (self.diag_sys.levenshtein_long_two_strings(user_answer,expected_answer))
			
				print "DIST", dist, "Tresh", self.answer_threshold
				#print type(dist), type(self.answer_threshold)

				self.run_correctness.setText(str(dist))

				att.given_ans = user_answer
				att.time2ans += time.time() - t1

				print "TIME TO ANS:", att.time2ans 

				self.run_under_ans.setText(user_answer)


				if dist < self.answer_threshold:
					#self.log("ANSWER IS CORRET")

					att.system_consideration = 1
					quest.insert_attempt(att)	
					self.robot_say("Parabéns. Você acertou!")
					#self.robot_speech.setText("Congratulations. You did!")
					#time.sleep(3)
					break

				else:
					#self.log("ANSWER IS WRONG")

					att.system_consideration = 0
					quest.insert_attempt(att)
					self.robot_say("Que pena. Eu acho que você errou!")

					#self.robot_speech.setText("Not Correct. Lets Try again!")
					#time.sleep(3)



			# Setting Adaptive Parameters!

			core.info("Finalizing emotion thread")
			self.run_emotion_flag = False

			self.read_values.set(self.n_deviations,
								self.adapt_sys.getBadEmotions(),
								3 - self.diag_sys.coutingWords(user_answer),
								att.time2ans,
								dist)

			# Clear Variables
			self.n_deviation = 0
			self.adapt_sys.clear_emo_variables()

			fvalue = self.adapt_sys.adp_function(j)
			fvalue = self.adapt_sys.activation_function(fvalue)
			self.adapt_sys.change_behavior(fvalue)

			self.user_profile = self.adapt_sys.robot_communication_profile+1

			#TROCA O VALOR DO USER PROFILE!!!
			
			# End of a question cycle
			# Insert current question in topic 
			topic.insert_question(quest)


		# Insert current topic in eval
		self.cur_eval.insert_topic(topic)
		print "\n\n"




	def run_final_dialog(self):

		self.robot_say("Bom! Por hoje é isso")
		self.robot.behavior.runBehavior('animations/Stand/Gestures/Hey_1')
		self.robot_say("Foi um prazer brincar com você, " + self.cur_user.first_name, block=False)
		#self.robot.behavior.runBehavior("hi/hi")
		
		print "PAssou"
		self.robot.motors.rest()

		# try:
		# except OSError as err:
		# 	print("OS error: {0}".format(err))
		# except ValueError:
		# 	print("Could not convert data to an integer.")
		# except:
		# 	print("Unexpected error:", sys.exc_info()[0])
		# 	core.er("DEU MERDA NO TCHAU")







	def run_load_models(self):
		#self.students_database.generate_encodings()
		self.run_facerecog_pushButton.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(True)
		self.emotion_classifier = emotion.Classifier()
		self.face_cascade = cv2.CascadeClassifier('Modules/haarcascade_frontalface_alt.xml')
		#self.faces = self.face_cascade.detectMultiScale(image_gray, 1.3, self.minNei_spinBox.value() )#minNeighbors=5)
		self.run_load_pushButton.setEnabled(False)

	def run_facerecog(self):
		self.recog_flag=True
		self.run_emotion_pushButton.setEnabled(False)
		#self.interact_recognize_person()


	def run_att_emo(self):
		#self.run_emotion_flag=True
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
		self.out =  cv2.VideoWriter(video_name,self.fourcc, 60.0, (640,480))
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
		
		# IF robot not connected
		#ret, self.image=self.capture.read()

		self.image = self.vis_sys.get_img(0)

		self.image = cv2.flip(self.image,1)
		#cv2.imshow("testwindow",self.image )
		#cv2.waitKey()

		if (self.recog_flag):
			self.image, self.recog_user_id = self.students_database.face_recognition(self.image)
			
			#self.cur_user= self.students_database.get_user(self.recog_user_id)
			 
			if self.recog_user_id:
				self.run_recognized_user_label.setText(self.recog_user_id)
			else:
				self.log("USER NOT DETECTED")

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

						self.adapt_sys.emotions[classified_emotion] += 1
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
		
		#user_answer = str(self.run_user_answer.text())
		#expected_answer = str(self.run_current_topic_data['Expected Answer'][self.run_question_interator])

		#dist =  str(self.diag_sys.levenshtein_long_two_strings(user_answer,expected_answer))
		
		# print "user", user_answer
		# print "ex", expected_answer
		# print "dist", dist
		# print
		
		#self.run_correctness.setText(dist)
		#self.log(dist)
		
		self.user_ans_flag=True


	






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



	def robot_say(self, text, block=True):

		self.robot_speech.setText(str(  text ))

		if self.robot is not None:
		
			self.user_ans_flag = True

			t1 = threading.Thread(name='robot_say_action', target=self.robot_say_action, args=(text, block))
			t1.start()

			while self.user_ans_flag:

				QCoreApplication.processEvents()

			#t2 = threading.Thread(name='my_service', target=my_service)
			#self.robot_say_action(text)




	def robot_say_action(self, text, block ):

		#self.robot_say_block()
		self.diag_sys.say(text, block=block)
		self.user_ans_flag = False



	#def robot_say_block(self,):





	def user_input(self):
		"""
		Wait user to answer in the correct 
		field and press corresponding button
		"""
		#core.info("Inside User input ")


		#print "Input Option", core.input_option

		# IF MIC
		if core.input_option > 0 :


			if self.robot is not None:
		
				#self.user_ans_flag = True

				#t1 = threading.Thread(name='wait', target=self.get_ans_mic)
				#t1.start()

				ret = self.diag_sys.getFromMic_Pt()#.decode('utf-8')

				#self.user_ans_flag = False
				self.run_under_ans.setText(ret)
				#t1.join()


	
		
		# IF text
		else:
			self.user_ans_flag = False

			while not self.user_ans_flag:
					
				#self.label_132.setText(str(time.time("hh:mm:ss")))
				QCoreApplication.processEvents()
				#time.sleep(0.05)

			self.user_ans_flag = False
			
			ret = str(self.run_user_answer.text().toUtf8())
			self.run_user_answer.setText("")


		return ret 


	def get_ans_mic(self):

		while self.user_ans_flag:
			QCoreApplication.processEvents()





	@pyqtSlot(str)
	def line_edit_text_changed(self, line, button):
		if line.text:  # Check to see if text is filled in
			button.setEnabled(True)
		else:
			button.setEnabled(False)

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main() # run the main function
