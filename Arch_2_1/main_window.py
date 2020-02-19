#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' 
-----------------------------------------------
	
			***********************
				R-CASTLE Project
				****************
					DTozadore
					   ***
					    *
	
	In development by Msc. Daniel Tozadore 
	dtozadore@gmail.com
 --------------------------------	---------------
 '''

# --- Qt Imports
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import threading
from multiprocessing import Queue, Process
from GUI.opening_main import My_Loading#,MyApp 
from GUI.show_graph import *#,MyApp 
from GUI import schedule 
from GUI import system_variables_control

# --- Opening dialog window
class MyOpening(Process):

    def __init__(self):
        self.queue = Queue(1)
        super(MyOpening, self).__init__()

    def run(self):
        app = QApplication([])
        d =  My_Loading()
        d.show()
        app.exec_()       


# --- Just a user 
# app1 = MyOpening()
# app1.start()





# --- Pyhton's defaults imports
import sys 
import csv
import os
import cv2
import time
import numpy as np
import pandas as pd
from utils import *
import random
import paramiko
import copy
import pickle


# --- Custumized imports 

import activities_Manager
# This file holds our MainWindow and all design related things
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
from Modules import AudioRecording #as aud_rec
from Utils import graphics, clock
from LAB import fuzzy




# class SessionInfo:
# 	def __init__(self,initi_time,final_time):
# 		self.initi_time = initi_time
# 		self.final_time = final_time





class MainApp(QMainWindow, activities_Manager.Ui_MainWindow):
	
	settings = QSettings("gui.ini", QSettings.IniFormat)


	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
	
		print '\n\n'




		# --- Initials setup

		app_icon = QIcon()
		app_icon.addFile('Robot_R-CASTLE', QSize(16,16))
		app_icon.addFile('Robot_R-CASTLE', QSize(24,24))
		app_icon.addFile('Robot_R-CASTLE', QSize(32,32))
		app_icon.addFile('Robot_R-CASTLE', QSize(48,48))
		app_icon.addFile('Robot_R-CASTLE', QSize(256,256))
		# self.setWindowIcon(QIcon('/GUI/R_CASTLE_Logo.jpeg'))
		self.setWindowIcon(app_icon)
		self.label_27.setPixmap(QPixmap('GUI/Logo'))
		#self.wel_image.setPixmap(QPixmap('GUI/Logo'))
		clock.AnalogClock(parent=self.wel_clock_widget )
		self.wel_dateEdit.setDate(QDate.currentDate())
		x= self.digital_clock_widget.geometry().width()
		y= self.digital_clock_widget.geometry().height()
		clock.DigitalClock(x,y,self.digital_clock_widget)
		#full screen
		#self.showFullScreen()


		# --- GENERAL setup!!

		self.robot = None
		self.vs= None
		#self.ds=None
		self.path_nao_records = "/home/nao/"
		#self.run_autovideo_checkBox.setChecked(True) 

		self.sys_vars = core.SystemVariablesControl()
		
		#exit()

		#self.diag_sys = dialog.DialogSystem(False, False)
		#self.sys_vars.add('user')
		QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf8"))
		
		self.supervisor ="admin"
		
		self.cur_user = None
		self.recog_flag = False #face recog flag


		self.actionSystem_Variables_Control_SVC.triggered.connect(self.open_svc)
		self.action_update_eval_index.triggered.connect(self.update_eval_index)
		self.actionOff_Line_Evaluations.triggered.connect(self.ole_batch_eval)
		self.actionBest_Weights.triggered.connect(self.eval_batch_find_weights)
		self.actionFuzzyBatch.triggered.connect(self.eval_best_fit_fuzzy)
		
		# --- Welcome screen

		self.schedule = clock.Schedule()
		self.wel_update_date()
		self.wel_open_meeting_button.clicked.connect(self.wel_open_meeting_action)
		self.wel_new_meeting_button.clicked.connect(self.wel_new_meeting_action)
		self.wel_delete_meeting_button.clicked.connect(self.wel_del_meeting_action)
		
		#meetings =[]
		self.calendar = clock.MyCalendar(self.wel_calendarWidget)#(self.wel_calendarWidget)
		#self.calendar.setLocale(QLocale.UnitedStates,QLocale.English)
		self.setLocale(QLocale(QLocale.English))
		#layout = QBoxLayout()
		self.calendar.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
		self.wel_add_meetings()
		#layout.addWidget(self.calendar)
		#self.wel_calendarWidget.setLayout(layout)
		#print self.schedule.meetings_table
		#self.schedule.save_meetings_list()
		#exit()


		# ----------------- JOAO -> TAKE A LOOK UNTIL LINE 172



		# --- Dialog
		self.answer_threshold = 1 - 0.60#self.diag_dist_thres_spinBox.value()
		#print "Thres valeu", self.answer_threshold
		entry = self.run_entry_comboBox.itemText( self.run_entry_comboBox.currentIndex())
		core.input_option = core.input_option_list[str(entry)]
				
		self.aud_rec_flag = False#True
		# self.aud_rec_flag = self.run_audio_record_checkBox.isChecked()
		#print "AQUII",self.aud_rec_flag
		
		self.diag_builder_save_button.clicked.connect( lambda: save_txt_to_file(self, self.diag_builder_textEdit,self.act.path+"/Dialog"))
		self.diag_builder_load_button.clicked.connect( lambda: load_txt_from_file(self, self.diag_builder_textEdit,self.act.path+"/Dialog"))

		#self.diag_bye_save_button.clicked.connect( lambda: save_txt_to_file(self, self.diag_bye_textEdit,self.act.path+"/Dialog"))
		#self.diag_bye_load_button.clicked.connect( lambda: load_txt_from_file(self, self.diag_bye_textEdit,self.act.path+"/Dialog"))
		self.diag_load_embeddings_button.clicked.connect(lambda: self.diag_process_dialogue("name_mus.txt"))
		self.diag_tag_button.clicked.connect(self.diag_insert_tag)

		# words_lists = pd.read_csv("Dialog/words_lists.csv")
		# self.diag_positives_list = words_lists['Pos'].toList()
		# self.diag_negatives_list = pd.read_csv("Dialog/negatives.csv")
		# self.diag_doubts_list = pd.read_csv("Dialog/doubts.csv")
		self.diag_build_frame.hide()
		self.diag_load_kw_table_button.clicked.connect(self.diag_load_kw_tables_action)
		self.diag_save_kw_table_button.clicked.connect(self.diag_save_kw_tables_action)
		self.diag_kw_pos_add_button.clicked.connect(lambda: self.diag_kws_table_add(self.diag_pos_listWidget))
		self.diag_kw_neg_add_button.clicked.connect(lambda: self.diag_kws_table_add(self.diag_neg_listWidget))
		self.diag_kw_doubt_add_button.clicked.connect(lambda: self.diag_kws_table_add(self.diag_doubt_listWidget))

		self.diag_kw_pos_del_button.clicked.connect(lambda: self.diag_kws_del(self.diag_pos_listWidget))
		self.diag_kw_neg_del_button.clicked.connect(lambda: self.diag_kws_del(self.diag_neg_listWidget))
		self.diag_kw_doubt_del_button.clicked.connect(lambda: self.diag_kws_del(self.diag_doubt_listWidget))




		#--- Vision panel
		self.display_flag = False
		#self.run_autovideo_checkBoxvideo_check_change
		self.run_display_image_radioButton.toggled.connect(lambda:self.video_check_change(self.run_display_image_radioButton))
		#self.vision_edit_button.clicked.connect(lambda:self.vision_class_setting_frame.setEnabled(True))
		self.vision_train_cnn_Button.clicked.connect(self.vision_train_model)
		self.vision_inc_db_button.clicked.connect(self.vision_create_datebase)



		#--- Content panel
		self.content_path=None
		self.subs_list = []

		self.loadactButton.clicked.connect(self.load_activity)
		self.exitButton.clicked.connect(self.close)
		self.insertQuestion_Button.clicked.connect(self.insertQuestion)
		self.loadQuestions_Button.clicked.connect(self.loadQuestions_fromFile)
		self.saveQuestions_Button.clicked.connect(self.saveQuestions_fromFile)
		#self.reportLoadButton.clicked.connect(self.loadReportsCsv)
		#self.writeReportButton.clicked.connect(self.writeReportCsv)
		
		self.content_delete_button.clicked.connect(self.content_delet_topic)
		self.contenct_newSubj_button.clicked.connect(self.content_NewSubject)
		self.content_insert_question_button.clicked.connect(self.content_InsertQuestion)
		self.content_delete_question_button.clicked.connect(self.content_DeleteQuestion)
		self.content_saveSub_button.clicked.connect(self.content_save)
		self.content_subject_comboBox.currentIndexChanged.connect(self.content_update_tab)
		self.content_clear_questions_button.clicked.connect(self.content_clear_table)
		self.content_load_from_file_button.clicked.connect(self.content_load_from_file_action)
		
		
		#--- Adaptive 
		self.user_profile = 3
		#self.adaptation_type = "Fuzzy"
		self.adaptation_type = "Rules"
		# self.adaptation_type = "Woz"

		#self.emotions = adaption.emotions
		# self.w = adaption.Weights()
		# self.op_par = adaption.OperationalParameters()
		# self.read_values=adaption.ReadValues()

		if (self.adaptation_type == "Fuzzy"):
			self.set_adaptive_fuzzy_parameters()
			
		self.adp_fuzzy_table_label.setPixmap(QPixmap("GUI/Fuzzy.png"))
		self.adp_fuzzy_logic_label.setPixmap(QPixmap("GUI/Adaptive.png"))

		#--- Knowledge panel
		self.knowledge_path="Data/"
		# DataFrames of General and Personal data
		self.know_gen_df=None
		know_data = "Data/general_knowledge_en.csv"
		self.knowledge_general_df = pd.read_csv( know_data , sep="|", encoding='utf-8')
		dataframe_to_table(self.knowledge_general_df,self.knowledge_general_table)
		self.know_gen_button_new.clicked.connect( lambda: insert_item_table(self.knowledge_general_table))
		self.know_gen_button_del.clicked.connect( lambda: delete_item_table(self.knowledge_general_table))
		self.know_gen_button_save.clicked.connect( self.know_save_file_action)
		self.know_gen_button_load.clicked.connect( self.know_load_from_file_action)
		#self.know_gen_button_load.clicked.connect( lambda: load_table(self, self.knowledge_general_table,self.know_gen_df,self.knowledge_path+"general_knowledge.csv"))

		self.know_per_df=None
		self.know_per_button_new.clicked.connect( lambda: insert_item_table(self.knowledge_personal_table))
		self.know_per_button_del.clicked.connect( lambda: delete_item_table(self.knowledge_personal_table))
		self.know_per_button_save.clicked.connect( lambda: save_table(self, self.knowledge_personal_table,self.know_per_df,self.knowledge_path+"personal_knowledge.csv"))
		self.know_per_button_load.clicked.connect( lambda: load_table(self, self.knowledge_personal_table,self.know_per_df,self.knowledge_path+"personal_knowledge.csv"))
		

		#--- Student
		
		self.students_database = UserDatabase()
		
		if os.path.exists("Usuarios"):
			dataframe_to_table(self.students_database.index_table, self.st_db_index_table)
			self.st_db_index_table.resizeColumnsToContents()

		self.user_new_button.clicked.connect( self.insert_user)
		self.user_cancel_button.clicked.connect( self.user_cancel)
		self.user_ok_button.clicked.connect( self.user_confirm_entry)
		self.user_del_button.clicked.connect( self.delete_user)
		self.user_open_table_button.clicked.connect( self.user_open)
		self.user_choose_pic_button.clicked.connect( self.user_choose_pic)
		self.user_aux_img = None



		#--- Evaluation
		self.cur_eval = None#Evaluation()
		self.cur_eval_index = 0
		self.evaluation_db = EvaluationDatabase()
		if os.path.exists("Evaluations"):
			dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)
		self.eval_index_table.resizeColumnsToContents()
		
		layout = QVBoxLayout()
		self.eval_video_player = Phonon.VideoPlayer()
		media = Phonon.MediaSource('LAB/abertura.mp4')
		self.eval_video_player.load(media)
		layout.addWidget(self.eval_video_player)
		self.eval_wid_video.setLayout(layout)
		
		#---- Time eval
		self.eval_time_questions_comboBox.currentIndexChanged.connect(self.eval_update_time_tab)
		self.eval_time_att_comboBox.currentIndexChanged.connect(self.eval_update_time_tab)
		self.eval_time_topic_comboBox.currentIndexChanged.connect(self.eval_update_time_tab)
		self.eval_gen_stats_button.clicked.connect(self.eval_gen_stats_action)
		
		self.eval_generate_graph.clicked.connect(self.eval_generate_graph_action)

		self.eval_next_pushButton.clicked.connect(self.eval_next_validation_action)
		self.eval_goToSec_tp_button.clicked.connect(lambda: self.eval_set_video_time(self.eval_tp_started_doubleSpinBox, self.eval_current_video_time_doubleSpin))
		self.eval_goToSec_qt_button.clicked.connect(lambda: self.eval_set_video_time(self.eval_qt_started_doubleSpinBox, self.eval_current_video_time_doubleSpin))
		self.eval_goToSec_att_button.clicked.connect(lambda: self.eval_set_video_time(self.eval_att_started_doubleSpinBox, self.eval_current_video_time_doubleSpin))
		
		self.eval_play_video_button.clicked.connect(self.eval_play_video)
		self.eval_pause_video_button.clicked.connect(self.eval_video_player.pause)
		self.eval_stop_video_button.clicked.connect(self.eval_video_player.stop)
		self.eval_seek_video_button.clicked.connect(lambda: self.eval_video_player.seek(float(1000*self.eval_current_video_time_doubleSpin.value())))

		# self.update_eval_index()
		# exit()

		#--- OLE
		self.eval_ole_start_button.clicked.connect(self.ole_start_eval)
		self.eval_ole_stop_button.clicked.connect(self.ole_stop_eval)
		self.eval_ole_load_models_button.clicked.connect(self.run_load_models)
		self.op_ole_open_pushButton.clicked.connect(self.op_ole_open_action_button)
		self.op_ole_compute_pushButton.clicked.connect(self.op_ole_compute_action)

		self.eval_open_button.clicked.connect( self.eval_open )
		self.eval_preview_eval_button.clicked.connect(lambda: self.eval_open('preview') )
		self.eval_next_eval_button.clicked.connect( lambda: self.eval_open('next') )
		self.eval_ok_button.clicked.connect( self.eval_confirm_entry)
		self.eval_cancel_button.clicked.connect(self.eval_cancel)
		self.eval_delete_button.clicked.connect( self.delete_eval)
		self.eval_topic_comboBox.currentIndexChanged.connect(self.eval_update_tab)
		self.eval_questions_comboBox.currentIndexChanged.connect(self.eval_update_tab)
		self.eval_att_comboBox.currentIndexChanged.connect(self.eval_update_tab)
		self.eval_ans_sup_comboBox.currentIndexChanged.connect(self.eval_validation_change)
		self.eval_ans_sys_comboBox.currentIndexChanged.connect(self.eval_validation_change)
		

		# --- GROUP ASSESSMENT
		self.grup_eval_update_tab()
		self.group_generate_button.clicked.connect(self.group_eval_generate_action)
		self.group_eval_open_button.clicked.connect(self.group_eval_open_button_pressed)
		self.group_eval_save_button.clicked.connect(self.group_eval_save_action)
		self.group_open_graph_button.clicked.connect(self.group_eval_wide_graph)
		self.group_graph_type_comboBox.currentIndexChanged.connect(self.group_eval_change_graph)		
		self.group_new_group_button.clicked.connect(self.run_new_eval_group_action)
		self.group_eval_create_button.clicked.connect(lambda: self.group_create_frame.setEnabled( not self.group_create_frame.isEnabled() ))
		self.group_eval_create_button.clicked.connect(lambda: self.group_eval_tabWidget.setEnabled(False))
		
		
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
		self.int_delete_line_button.clicked.connect(self.int_delete_line_action)


		
		#--- Plan and Run
		self.pushButton_run_activity.clicked.connect(self.start_activity)
		self.run_new_eval_group_toolButton.clicked.connect(self.run_new_eval_group_action)
		
		self.run_facerecog_pushButton.clicked.connect(self.run_facerecog)
		self.run_emotion_pushButton.clicked.connect(self.run_att_emo)
		self.run_load_pushButton.clicked.connect(self.run_load_models)
		self.run_robot_connect_button.clicked.connect(self.run_connect_robot_action)
		self.run_reset_button.clicked.connect(self.run_reset_demo_action)
		self.deviation_times=[]


		#self.pushButton_start_robot_view.clicked.connect(self.resume_display_image)
		#self.pushButton_stop_robot_view.clicked.connect(self.stop_display_image)
		#self.run_takepic_pushButton.clicked.connect(self.run_takepic)
		#self.run_picname_lineEdit.textChanged.connect( lambda: self.line_edit_text_changed(self.run_picname_lineEdit,self.run_takepic_pushButton	 ))
		#self.run_videoname_lineEdit.textChanged.connect( lambda: self.line_edit_text_changed(self.run_videoname_lineEdit,self.run_recvid_button	 ))
		#self.run_recvid_button.clicked.connect(self.run_start_recording_video)
		#self.run_stopvid_button.clicked.connect(self.run_stop_recording_video)
		
		#self.run_next_question_pushButton.clicked.connect(self.run_next_question)
		#self.run_next_topic_pushButton.clicked.connect(self.run_next_concept)
		
		self.run_next_step_button.clicked.connect(self.setNextStepFalse)
		self.next_step = True
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


		# self.model = QStandardItemModel(self)
		# self.tableView.setModel(self.model)
		# self.tableView.horizontalHeader().setStretchLastSection(True)

		# self.tableView.setModel(self.model)
		# self.tableView.horizontalHeader().setStretchLastSection(True)
		# self.layoutVertical = QVBoxLayout(self)
		# self.layoutVertical.addWidget(self.tableView)
		# self.layoutVertical.addWidget(self.reportLoadButton)
		# self.layoutVertical.addWidget(self.writeReportButton)
		
		self.head_ok_button.clicked.connect(self.create_activity)
		self.new_activity_button.clicked.connect(self.new_activity)


		#Shortcuts:
		self.shortcut = True
		#self.shortcut =  False
		
		if self.shortcut:
			self.load_activity()  # WORKSPACES
			#self.int_load_action()
			#self.int_lock_action()


		#self.evals_to_csv()
		#exit()
		restore_state(self.settings)


	def load_activity(self):
		
		if self.shortcut:

			#self.act=ct.load_Activity("./Activities/Nutrition/activity.data")#None 
			self.act=ct.load_Activity("Activities/NOVA/activity.data") #None
			#self.act=ct.load_Activity("/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Content") #None
			#dataframe_to_table(self.know_pa,table)
		else:
			filename = QFileDialog.getOpenFileName(self, 'Open File', './Activities')
			self.act=ct.load_Activity(filename)
			
		
		try:
			self.vis_dp = data_process.Data_process(self.act.path)
			self.vision_aug_button.clicked.connect(self.vis_dp.data_aug)
			self.vision_build_tree_button.clicked.connect(lambda: self.vis_dp.buildTrainValidationData(self.vision_val_per_spinBox.value()))
			self.vision_del_db_button.clicked.connect(self.vis_dp.erase_database)
			self.vision_edit_button.clicked.connect(self.vision_edit_settings_action)
			#self.vision_edit_button.clicked.connect(self.vision_show_database)
			self.vision_classes_comboBox.currentIndexChanged.connect(self.vision_show_database)
			#self.vision_inc_db_button.
		except:
			self.log("Activity has no vision settings yet", 'w')

		try:
			self.head_created_by_lineEdit.setText(self.act.created_by )
			self.head_edited_by_lineEdit.setText(self.act.edited_by)
			self.head_created_date.setDate(self.act.creation_date)
			self.head_edited_date.setDate(self.act.edition_date)
		except:
			self.log("Activity class is an old version. Creation details are missing", 'e')


		#self.name_lineEdit.setText(self.act.name)
		#self.desc_lineEdit.setText(self.act.description)		
		#self.path_lineEdit.setText(self.act.path)
		#self._lineEdit.setText(self.act.desc)
		self.head_edit_button.setEnabled(True)
		self.modules_tabWidget.setEnabled(True)
		self.content_path = self.act.path +  "/Content" +"/"
		
		#self.sub_list = load_subjects(os.path.join(self.act.path,"Content","subjects"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.cvs"))
		#print self.sub_list
		#self.content_subject_comboBox.addItems(self.sub_list[1])

		self.head_name_lineEdit.setText(self.act.name)
		self.head_path_lineEdit.setText(self.act.path)
		self.head_desc_lineEdit.setText(self.act.description)


		self.content_load_subjects()
		self.interact_database = InteractionDatabase(self.act.path)

		self.diag_load_kw_tables_action()
		
		self.modules_tabWidget.setCurrentIndex(11)



	def close(self):
		if self.robot is not None:
			self.vis_sys.unsub(0)
		
		
		#save_state(self.settings)
		#self.closeEvent(self, event)
		exit()
		#self.destroy()

	def new_activity(self):
		act_name,  ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter new Activity Name:')
		if ok:
			self.head_name_lineEdit.setText(act_name)
			path = "Activities/"+str(act_name)
			self.head_path_lineEdit.setText(path)
			self.head_desc_lineEdit.setText("")
			
			self.head_name_lineEdit.setEnabled(True)
			self.head_desc_lineEdit.setEnabled(True)
			self.head_path_lineEdit.setEnabled(True)
			self.head_ok_button.setEnabled(True)
			self.head_cancel_button.setEnabled(True)
			self.head_created_by_lineEdit.setText(self.supervisor)
			self.head_edited_by_lineEdit.setText(self.supervisor)
			self.head_created_date.setDate(QDate.currentDate())
			self.head_edited_date.setDate(QDate.currentDate())

	def create_activity(self):

		act_name = str(self.head_name_lineEdit.text())
		#act_path = str(self.head_path_lineEdit.text())

		act = ct.Activity(act_name)

		act.description = str(self.head_desc_lineEdit.text().toUtf8())

		try:
			act.created_by = self.head_created_by_lineEdit.text()
			act.edited_by = self.head_edited_by_lineEdit.text()
			act.creation_date = self.head_created_date.date()
			act.edition_date = self.head_edited_date.date()
		except:
			self.log("Activity class is an old version. Creation details are missing", 'e')


		act.print_Attributes()

		#return
		# def create_Activity(act, vs=False):
		vs=False
		'''    
		Create a new activity and set all directories
		'''


		if os.path.exists(act.path):
			core.war("Path activity exists")        
			
		else:
			core.info("Starting new activity folder in " + act.path )
			os.makedirs(act.path)
			os.makedirs(os.path.join(act.path,"Vision" ))
			os.makedirs(os.path.join(act.path, "Logs" ))

			aux_path = os.path.join(act.path, "Dialog" )
			os.makedirs(aux_path)
			df = pd.DataFrame(columns= ["Positives", "Negatives", "Doubts"])
			df.loc[-1]=["Yes","No","Maybe"]
			df.index = df.index + 1
			df.to_csv(aux_path +'/keywords.csv',index=False)
			f = open(aux_path +"/_def_question.txt",'w')
			f.write("Are you sure?")
			f.close()

			#os.makedirs(os.path.join(act.path, "Users" ))
			
			aux_path=os.path.join(act.path, "Content" )
			os.makedirs(aux_path)
			df = pd.DataFrame(columns=['subjects','concepts'])
			df.to_csv(aux_path +"/subjects.csv",index=False)

		#core.info("Writing activity attributes" )
		self.log("Writing activity attributes",'w' )
		
		
		
		if act.vision:
			core.info("Starting Vision Componets for activity: " + act.name)
			act.classes = vs.collect_database(act, camId=1)
			act.ncl = len(act.classes)
			#act.save()
			dp = data_process.Data_process(act.path )
			#dp.buildTrainValidationData()
			#dp.data_aug()		
			#dp.generate_model()
			dp.save_best()
			dp.print_classes()
		
		else:
			self.log("Activity <<" + act.name + ">> has no Vision system required",'w')	
		
			
		
		with open(os.path.join(act.path,'activity.data'), 'wb') as f:
			pickle.dump(act, f, pickle.HIGHEST_PROTOCOL)
		
		self.log("Writining successfull",'w')
		
			
	def open_svc(self):

		par = [self.sys_vars]
		svc = system_variables_control.Svc_Gui(par,self)
		ret = svc.exec_()
		#print ret


#-------------------------------------------- \Welcome ---------------------------------

	def wel_update_date(self):
		
		date = self.wel_dateEdit.date()
		#QDate date = QDateTime::currentDateTime().date();
		locale = QLocale(QLocale.English) # set the locale you want here
		strDate = locale.toString(date, "dddd, d MMMM yyyy")


		#print swedishDate	
		self.wel_date_label.setText(strDate)


		# weekday = date.toString('dddd')
		# # date = date.toString('dddd, d of MMMM of yyyy')
		# weekday = weekday.left(1).toUpper()+weekday.mid(1)
		# day		= date.toString('dd')
		# month 	= date.toString('MMMM')
		# month = month.left(1).toUpper()+month.mid(1)
		# year 	= date.toString('yyyy')
		# self.wel_wd_label.setText(weekday)
		# self.wel_month_label.setText(month)
		# self.wel_year_label.setText(year)

	def wel_add_meetings(self):
		for item in self.schedule.meetings_list:
			#print  item.date
			self.calendar.add_meeting(item.date)

	def wel_del_meeting_action(self):

		date = self.calendar.selectedDate()	
		for item in self.schedule.meetings_list:

			if item.date == date:
				dg = QMessageBox.warning(self,"Deleting Meeting", "\nAre you sure you want to delete this meeting?", QMessageBox.Ok|QMessageBox.Cancel)

				if  dg == QMessageBox.Ok:
					self.schedule.del_meeting(date)	
					dg = QMessageBox.information(self,"Deleted", "Test in date of " + date.toString("dd/MM/yyyy"), QMessageBox.Ok)
					self.calendar.clear_meetings()
					self.wel_add_meetings()
					self.calendar.update()
					return

		dg = QMessageBox.information(self,"NOUP", "NOOOO", QMessageBox.Ok)


	def wel_open_meeting_action(self):

		date = self.calendar.selectedDate()
		mts = self.schedule.meetings_list

		for item in self.schedule.meetings_list:

			if item.date == date:
				# dg = QMessageBox.information(self,"YEAH", "YEASSSSSSS", QMessageBox.Ok)
				arg = [item]
				#pprint(vars(item))
				#print "TIPO", type(item.period)

				sc =schedule.Show_schedule(arg, self)
				sc.setWindowModality(Qt.ApplicationModal)
				
				if sc.exec_() == QDialog.Accepted:
					#print "BLOCK"
					self.schedule.save_meetings_list()
					self.calendar.clear_meetings()
					self.wel_add_meetings()
					self.calendar.update()

				
				return

		
		dg = QMessageBox.critical(self,"Error", "None meeting found here.", QMessageBox.Ok)

		return

	def wel_new_meeting_action(self):

		date = self.calendar.selectedDate()
		
		item = clock.Appoitment(0,date, QTime())
		
		arg = [item]
		sc =schedule.Show_schedule(arg, self)
		# sc.setWindowModality(Qt.ApplicationModal)
		
		if sc.exec_() == QDialog.Accepted:
			#print "BLOCK"
			self.schedule.add_meeting(item)
			self.schedule.save_meetings_list()
			self.calendar.clear_meetings()
			self.wel_add_meetings()
			self.calendar.update()

		
		return

		
		
		
		
		
#----------------------------------------------- \DIALOG -----------------------------
	
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
	
	
	def diag_welcome_open(self):
		load_txt_from_file(self,self.dialog_welcome_textEdit, self.act_path+"Dialog/")


	def diag_welcome(self):
		
		text = str(self.diag_welcome_textEdit.toPlainText().toUtf8())
		print text, type(text)
		print "nome", self.cur_user.first_name
		self.log(text)
		
		#print "Tipo", type( self.cur_user.first_name)
		



	def diag_process_dialogue(self, filename):

		f = open(self.act.path+ "/Dialog/" + filename, 'r')
		text = f.read()
		f.close()
		#self.log(txt2say)
		#print txt2say
		# print "TEXT TYPE", type(text)
		# text = text.decode('utf-8')
		# print "TEXT TYPE", type(text)

		if self.cur_user is not None:
			text = text.replace('<user name>', self.cur_user.first_name)
			#text = text.replace('<user_team>', self.cur_user.preferences['team'])
		

			# aux = self.cur_user.preferences['food']#.toUtf8()
			# # aux = self.cur_user.preferences['food'].toUtf8()
			# #print "TEPE Aux", type(aux)
			# aux = str(aux)
			# text = text.replace('<user_food>', aux)
			
			# aux = self.cur_user.preferences['team'].toUtf8()
			# #aux = str(aux)
			# text = text.replace('<user_team>', aux)
			
			# aux = self.cur_user.preferences['music'].toUtf8()
			# #aux = str(aux)
			# text = text.replace('<user_music>', aux)
			

		self.robot_say(text)#, type(text)

		#self.log(text)
	


	def diag_insert_tag(self):

		cr = self.diag_builder_textEdit.textCursor()
		text = self.diag_tag_list.currentItem().text()
		text = str(text).lower()
		text = " <"+text+"> "
		cr.insertText(text)
		self.diag_builder_textEdit.textCursor().movePosition(QTextCursor.EndOfWord)
		#self.diag_builder_textEdit.
		# QTextCursor::EndOfWord
		self.diag_builder_textEdit.setFocus()

		#print self.dialog_tabWidget.parentWidget().pos()


	def diag_confirm(self):

		text = self.diag_def_question_textEdit.text()


		self.robot_say(text)

		ans = self.user_input()

		return (ans in self.diag_positives_list)




	def diag_load_kw_tables_action(self):

		path = self.act.path+"/Dialog/"
		data = pd.read_csv(path+"keywords.csv")

		#print data
		self.diag_pos_listWidget.clear()
		self.diag_neg_listWidget.clear()
		self.diag_doubt_listWidget.clear()


		self.diag_positives_list = data['Positives'].tolist()
		self.diag_positives_list = [x for x in self.diag_positives_list if str(x) != 'nan']
		self.diag_pos_listWidget.addItems(self.diag_positives_list)
		aux = self.diag_pos_listWidget
		for i in range(aux.count()):
			aux.item(i).setFlags(aux.item(i).flags() | Qt.ItemIsEditable)

		self.diag_negatives_list = data['Negatives'].tolist()
		self.diag_negatives_list = [x for x in self.diag_negatives_list if str(x) != 'nan']
		self.diag_neg_listWidget.addItems(self.diag_negatives_list)
		aux = self.diag_neg_listWidget
		for i in range(aux.count()):
			aux.item(i).setFlags(aux.item(i).flags() | Qt.ItemIsEditable)

		self.diag_doubts_list = data['Doubts'].tolist()
		self.diag_doubts_list = [x for x in self.diag_doubts_list if str(x) != 'nan']
		self.diag_doubt_listWidget.addItems(self.diag_doubts_list)
		aux = self.diag_doubt_listWidget
		for i in range(aux.count()):
			aux.item(i).setFlags(aux.item(i).flags() | Qt.ItemIsEditable)

		f = open(path+"_def_question.txt",'r')
		qt = f.read()
		f.close()

		self.diag_def_question_textEdit.setText(qt)


	def diag_save_kw_tables_action(self):

		path = self.act.path+"/Dialog/"
		#data = pd.read_csv(path+"keywords.csv")

		# #print data
		# self.diag_pos_listWidget.clear()
		# self.diag_neg_listWidget.clear()
		# self.diag_doubt_listWidget.clear()
		qt = str(self.diag_def_question_textEdit.toPlainText().toUtf8())

		f = open(path+"_def_question.txt",'w')
		f.write(qt)
		f.close()


		# self.diag_positives_list = data['Positives'].tolist()
		#print self.diag_pos_listWidget.items()
		self.diag_positives_list = [ str(self.diag_pos_listWidget.item(i).text().toUtf8()) for i in range(self.diag_pos_listWidget.count())]
		self.diag_negatives_list = [ str(self.diag_neg_listWidget.item(i).text().toUtf8()) for i in range(self.diag_neg_listWidget.count())]
		self.diag_doubts_list = [ str(self.diag_doubt_listWidget.item(i).text().toUtf8()) for i in range(self.diag_doubt_listWidget.count())]
		
		
		
		#print self.diag_negatives_list
		
		data = pd.DataFrame(columns=['Positives', 'Negatives','Doubts'])
		data['Positives'] = pd.Series(self.diag_positives_list)
		data['Negatives'] = pd.Series(self.diag_negatives_list)
		data['Doubts'] = 	pd.Series(self.diag_doubts_list)

		#print data 

		data.to_csv(path+"keywords.csv", index=False)
		return 

	

	def diag_kws_table_add (self, table):

		aux = QListWidgetItem("")#.setFlags(Qt.ItemIsEditable)
		aux.setFlags(aux.flags() | Qt.ItemIsEditable)
		
		table.addItem(aux)	
		table.setCurrentRow(table.count()-1)
		item = table.itemFromIndex(table.currentIndex())
		#print "TST", item.text() 
		table.editItem(item)
		#table.insetRow()

	def diag_kws_del(self, table):
		table.takeItem(table.currentRow())




#------------------------------------------------ \VISION -------------------------------------

	def vision_edit_settings_action(self):

		print "hello"
		self.vision_class_setting_frame.setEnabled(True)
		self.vision_classes_comboBox.clear()
		self.vision_classes_comboBox.addItems(self.vis_dp.classes)



	def vision_train_model(self):

		name 	= self.vision_model_train_name_lineEdit.text()
		steps 	= self.vision_steps_Box.value()
		batch 	= int(self.vision_batch_comboBox.currentText())
		epochs 	= self.vision_epoch_Box.value()
		validation = self.vision_val_per_spinBox.value()

		self.vis_dp.generate_model(name, steps,batch,epochs,validation)


	def vision_show_database(self):

		lbl_list = self.vision_samples_frame.findChildren(QFrame)
		#print lbl_list
		self.vision_class_setting_frame.setEnabled(True)
		
		cur_class = str(self.vision_classes_comboBox.currentText())
		# cur_class = 'Piramid' 
		# cur_class = 'Cube' 
		# cur_class = 'Piramid' 

		# Displaying the total of classes
		pic_list = os.listdir(os.path.join(self.vis_dp.work_path, "Images"))
		self.vision_total_classes.display(len(pic_list))

		# Displaying the samples per class
		path = os.path.join(self.vis_dp.work_path, "Images", cur_class)
		pic_list = os.listdir(path)
		self.vision_samples_per_class.display(len(pic_list))
		
		# Displaying samples in data .Aug path
		aug_path = os.path.join(self.vis_dp.work_path, '.train', cur_class)
		self.vision_samples_auged.display(len(os.listdir(aug_path)))


		my_rand = [random.randint(1,len(pic_list)-1) for x in range(len(lbl_list)) ]
		
		#print my_rand
		#print pic_list
		i=0
		for item in lbl_list:
			#for i in my_rand:
			im_path =os.path.join(path, pic_list[my_rand[i]])
			#print i , my_rand[i], pic_list[my_rand[i]]
			item.setPixmap(QPixmap(im_path))
			i+=1


	def vision_create_datebase(self):

		#self.vis_sys.collect_database(self.act,"NEWIMG",100)
		name = "NEWIMG/"+str(self.vision_model_train_name_lineEdit.text())

		for i in range(100):
			cv2.imwrite(name+str(i)+".png", self.image)






#------------------------------------------------ \CONTENT -------------------------------------

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
		try:
			text= str(self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()])
			
			self.content_concept.setText(text)
			file_name = str(self.content_path + self.content_subject_comboBox.currentText()+".csv")

			if os.path.isfile(file_name):
				data=pd.read_csv(file_name)
				#print "trying data", data

				dataframe_to_table(data,self.content_questions_table)

				self.log("Subject loaded: " + self.content_subject_comboBox.currentText())
				self.content_questions_table.resizeColumnsToContents()
				#self.content_questions_table.resizeRowsToContents()


			else:	
				self.log("WARNING TABLE <<" + file_name +">>  FILE DO NOT EXIST")
				labels = []
				for i in range(0,3):
					labels.append(str(self.content_questions_table.horizontalHeaderItem(i).text()))
				
				data = 	pd.DataFrame(columns=labels, index=range(0))

				#print data

				data.to_csv(self.content_path + self.content_subject_comboBox.currentText()+".csv", index=False)
				data.to_csv(file_name, index=False)

		except:
			self.log("No subject found!")


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
			

	def content_load_from_file_action(self):

		flag = True
		while (flag):
			filename = QFileDialog.getOpenFileName(self, 'Open File', self.act.path + "/Content")
			filename = str(filename)

			if filename.endswith('.csv'):
				QMessageBox.information(self, "Warning!", "Don't forget to save the table to the content!", QMessageBox.Ok )		
				break

			else:
				QMessageBox.critical(self, "Error!", "File is not a CSV file. \n\nChoose a CSV file.", QMessageBox.Ok )		

		data=pd.read_csv(filename)
		#print "trying data", data

		dataframe_to_table(data,self.content_questions_table)


#-------------------------------------------------- \KNOWLEDGE ----------------------------------------


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

			self.knowledge_general_df.loc[size]=[concept.decode('utf-8'), definition]

			#print self.knowledge_general_df.loc[size]

			self.knowledge_general_df.to_csv("Data/general_knowledge_en.csv" , sep="|", encoding='utf-8', index=False) 
			
			dataframe_to_table(self.knowledge_general_df, self.knowledge_general_table)

			return definition


	def know_save_file_action(self):

		save_table(self, self.knowledge_general_table,self.know_gen_df,self.knowledge_path)
		#self.knowledge_general_table.resizeColumnsToContents()


	def know_load_from_file_action(self):

		load_table(self, self.knowledge_general_table,self.know_gen_df,self.knowledge_path)
		self.knowledge_general_table.resizeColumnsToContents()
		
		# flag = True
		# while (flag):
		# 	filename = QFileDialog.getOpenFileName(self, 'Open File', "Data/")
		# 	filename = str(filename)

		# 	if filename is "":
		# 		break 

		# 	elif filename.endswith('.csv'):
		# 		QMessageBox.information(self, "Warning!", "Don't forget to save the table to the content!", QMessageBox.Ok )		
		# 		break

		# 	else:
		# 		QMessageBox.critical(self, "Error!", "File is not a CSV file. \n\nChoose a CSV file.", QMessageBox.Ok )		

		# print "NOMEEE", filename
		# data=pd.read_csv(filename)
		# #print "trying data", data

		# dataframe_to_table(data,self.knowledge_general_table)



#-------------------------------------------------- \ADAPTION ----------------------------------------

	def set_adaptive_fuzzy_parameters(self):
		
		max_gaze = self.face_dev_activation.value()
		max_emotions = self.negEmoAct__spinBox.value()
		max_words = self.adp_words_spinBox.value()
		max_tta = self.learningTime_doubleSpinBox.value()
		max_success = self.wrongAns_Tol_doubleSpinBox.value()

		#print max_gaze, max_emotions, max_words, max_tta, max_success

		self.states_fuzzy_control = fuzzy.StatesFuzzyControl(max_gaze=max_gaze,
															max_emotions=max_emotions,
															max_words=max_words,
															max_tta=max_tta, 
															max_success=max_success,
															print_flag=False)
		self.adaptive_fuzzy_control = fuzzy.Adaptive(False)
		#self.adaptive_fuzzy_control = fuzzy.StatesFuzzyControl(False)
	


#-------------------------------------------------- \USER ----------------------------------------


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
		
		#QPixmap qpix = self.user_image.pixmap()
		image = self.user_image.pixmap().toImage()
		
		#print type (image)

		#img = cv2.Mat(image.rows(),image.cols(),CV_8UC3,image.scanline())
		
		try:
			#print "try"
			img = qImageToMat(image)
			
		except Exception as e:
			print "Exception", e

		#print type (img)

		#cv2.imshow("test",img)
		#cv2.waitKey(0)

		aux = User(int(self.user_id_label.text()),
			(self.user_name_field.text()).toUtf8(),
			(self.user_last_name_field.text()).toUtf8(),
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
		
		#Reload the list
		self.students_database.load_users_list()

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

		self.cur_user = user2show

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






#-------------------------------------------------- \EVAL ----------------------------------------


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

		try:
			del self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()]
			self.evaluation_db.delete_eval(eval2kill)
			core.info("Evaluation ID  " + str(eval2kill.id) + " deleted!")

		except NameError as error:
			#print "PIRNT", error.message
			core.er("Delete Fail: " + error.message)

		dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)

	

	def eval_cancel(self):

		self.eval_index_frame.setEnabled(True)
		self.eval_frame.setEnabled(False)
		self.eval_index_ok_frame.setEnabled(False)


		#self.log_text.setText(self.user_name_field.text())	
		
	# def __init__(self, id, first_name, last_name, bday='None',
    #             scholl_year='None', picture='None', preferences={}, img = None, creation_Date=None):
	
	# def setPreferences(self, sport='None', team='None', toy='None', game='None', 
    #                    dance='None', music='None', hobby='None', food='None'):

	
	
	
	def eval_confirm_entry(self):
		
		

		
		self.cur_eval.date = self.eval_date.date()
		self.cur_eval.usar_id = self.eval_user_id_label.text() 
		self.cur_eval.user_name = self.eval_user_name.text()
		self.cur_eval.start_time = self.eval_start.time()
		self.cur_eval.end_time = self.eval_end.time()
		#self.cur_eval.duration = self.eval_duration.time()
		self.cur_eval.duration = self.cur_eval.start_time.msecsTo(self.cur_eval.end_time)
		self.cur_eval.robot = self.eval_robot_lineEdit.text()
		self.cur_eval.obs = self.eval_observation_textField.toPlainText()
		self.cur_eval.supervisor = self.eval_supervisor_lineEdit.text()
		self.cur_eval.user_dif_profile=self.eval_last_dif.value()


		# aux = Evaluation(int(self.eval_id_label.text()),
		# 	(self.eval_date.date()),
		# 	(self.eval_user_id_label.text()),
		# 	self.eval_user_name.text(),
		# 	#str(self.user_bd_field.textFromDateTime("dd:mm:yyyy")),
		# 	self.eval_duration.time(),
		# 	self.eval_start.time(),
		# 	self.eval_start.time(),

			
		# 	)

		
		if self.evaluation_db.insert_eval(self.cur_eval)	> 0:
			self.sys_vars.add('eval')
		
		dataframe_to_table(self.students_database.index_table, self.st_db_index_table)
		
		self.eval_index_frame.setEnabled(True)
		self.eval_frame.setEnabled(False)
		self.eval_index_ok_frame.setEnabled(False)



	def eval_open(self, index='current'):

		#self.st_db_index_table.setEnabled(False)
		self.eval_index_frame.setEnabled(False)
		self.eval_frame.setEnabled(True)
		self.eval_video_widget_buttons.setEnabled(True)
		self.eval_index_ok_frame.setEnabled(True)
		#self.user_frame.setEnabled(True)
		
		# Get the user in the selected row of the users table
		if index == 'next':
			# self.cur_eval = self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()+1]
			if self.cur_eval_index+1 > self.eval_index_table.rowCount():
				QMessageBox.critical(self,"Error!", "No Eval next")
				return	
			self.cur_eval_index += 1
			#self.eval_index_table.setItemSelected()
		elif index == 'preview':
			# self.cur_eval = self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()-1]
			if self.cur_eval_index-1 < 0:
				QMessageBox.critical(self,"Error!", "No Eval before")
				return	
			self.cur_eval_index -= 1
		
		else:
			# self.cur_eval = self.evaluation_db.evaluations_list[self.eval_index_table.currentRow()]
			self.cur_eval_index = self.eval_index_table.currentRow()

		
		self.cur_eval = self.evaluation_db.evaluations_list[self.cur_eval_index]

		self.eval_id_label.setText(str(self.cur_eval.id))
		
		user = self.students_database.get_user(self.cur_eval.user_id)

		#print self.cur_eval.user_id
		#print user #"DEU"
		#exit()


		#self.ole_start_eval

		self.eval_user_id_label.setText(str(self.cur_eval.user_id))
		self.eval_date.setDate(self.cur_eval.date)#QDate.fromString(self.cur_eval.date.toString(),"dd.MM.yyyy"))
		# self.cur_eval.duration= None
		# print "DUR", self.cur_eval.duration
		# tt = QTime(0,0).msecsTo(self.cur_eval.duration)
		# self.log("DUR ", str(self.cur_eval.duration))
		#dur =0 

		
		if (self.cur_eval.duration is None) or (type(self.cur_eval.duration)==QTime):#'PyQt4.QtCore.QTime'):
			dur = self.cur_eval.start_time.msecsTo(self.cur_eval.end_time)
			#print dur
			self.cur_eval.duration=dur
			self.evaluation_db.insert_eval(self.cur_eval)
		
			self.eval_duration.setTime(QTime(0,0).addMSecs(dur))
		else:
			#print type(self.cur_eval.duration)
			self.eval_duration.setTime(QTime(0,0).addMSecs(self.cur_eval.duration))


		self.eval_start.setTime(self.cur_eval.start_time)
		self.eval_end.setTime(self.cur_eval.end_time)
		self.eval_supervisor_lineEdit.setText(self.cur_eval.supervisor)
		self.eval_user_name.setText(str(self.cur_eval.user_name))
		self.eval_user_name.setText(str(self.cur_eval.user_name))
		#self.eval_concept_textField.setText(self.cur_eval.concept)
		self.eval_last_dif.setValue(self.cur_eval.user_dif_profile)
		self.eval_int_id_spinBox.setValue(self.cur_eval.int_id)
		self.eval_group_lineEdit.setText(self.cur_eval.group)

		self.eval_open_graphs()
		
		# try:
		# 	self.eval_duration.setTime(self.cur_eval.duration)
		# except:
		# 	self.log("Duration is None")
			
		try:
			self.eval_observation_textField.setText(self.cur_eval.obs)
		except:
			self.log("Obs was empty")
			self.eval_observation_textField.setText("")	

		path = 'Evaluations/'+str(self.cur_eval.id)+'/'+str(self.cur_eval.id)+'.avi' 
		
		if os.path.exists(path):
			media = Phonon.MediaSource(path)
			self.eval_video_player.load(media)
		
		else:
			self.log("Video not founding",'w')


		if self.cur_eval.validation:
			self.eval_gen_stats_button.setEnabled(False)
		else:
			self.eval_gen_stats_button.setEnabled(True)


		if(len(self.cur_eval.topics)==0):
			print "ERROR: Topics empty"
		

		else:

			#print self.cur_eval.tp_names
			#print self.cur_eval.topics
			self.eval_topic_comboBox.clear()
			self.eval_questions_comboBox.clear()
			self.eval_topic_comboBox.clear()
			self.eval_att_comboBox.clear()


			self.eval_topic_comboBox.addItems(self.cur_eval.tp_names)
			self.eval_time_topic_comboBox.addItems(self.cur_eval.tp_names)

			index_list = range(1,len(self.cur_eval.topics[0].questions)+1)
			index_list=["{}".format(x) for x in index_list]
			self.eval_questions_comboBox.addItems(index_list)
			self.eval_time_questions_comboBox.addItems(index_list)

			index_list = range( 1 ,len(self.cur_eval.topics[0].questions[0].attempts)+1)
			index_list=["{}".format(x) for x in index_list]
			self.eval_att_comboBox.addItems(index_list)
			self.eval_time_att_comboBox.addItems(index_list)

			#Ideia: Fazer um listner para os 3 combobox para atulizar o Topics validation tab

			#self.eval_quest_lineEdit.setText(self.cur_eval.topics[])
			

			self.eval_update_tab()
			self.eval_update_time_tab()



		self.log("Evaluation number {} Opened".format(self.cur_eval.id))
		

		#self.log_text.setText(self.eval_date.date().toString('dd/MM/yyyy') + " Opened eval of date:")



	def eval_open_graphs(self):
		try:
			graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/sys_graph"
			pixmap = QPixmap(graph_name)
			self.eval_evolution_graph.setPixmap(pixmap)
			
			graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/student_times_graph"
			pixmap = QPixmap(graph_name)
			self.eval_time_graph.setPixmap(pixmap)
			
			graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/student_times_graph"
			pixmap = QPixmap(graph_name)
			self.eval_time_graph.setPixmap(pixmap)

			graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/student_performance_graph"
			pixmap = QPixmap(graph_name)
			self.eval_std_perf_graph.setPixmap(pixmap)
			
		except:
			self.log("Graphs not generated", 'w')	

	def eval_update_tab(self):
		
		#text= str(self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()])
		
		max_tp = len(self.cur_eval.topics)
		max_qt = len(self.cur_eval.topics[0].questions)
		max_att = len(self.cur_eval.topics[0].questions[0].attempts)

		#if (self.tp_id == max_tp-1) and (self.qt_id == max_qt-1) and (self.att_id == max_att-1):
		#	self.eval_next_pushButton.setEnabled(False)
		
		self.tp_id=self.eval_topic_comboBox.currentIndex()
		self.qt_id=self.eval_questions_comboBox.currentIndex()
		self.att_id=self.eval_att_comboBox.currentIndex()

		aux_att = self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id] #Attempt()

		self.eval_concept_textField.setText(self.cur_eval.topics[self.tp_id].concept)
		self.eval_quest_lineEdit.setText(self.cur_eval.topics[self.tp_id].questions[self.qt_id].question )
		self.eval_exp_lineEdit.setText(self.cur_eval.topics[self.tp_id].questions[self.qt_id].exp_ans )
		self.eval_gave_ans_lineEdit.setText(self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].given_ans )
		self.eval_time2ans.setTime(QTime.fromString(str(aux_att.time2ans),"mm:ss"))
		self.eval_ans_sup_comboBox.setCurrentIndex(aux_att.supervisor_consideration) 
		self.eval_ans_sys_comboBox.setCurrentIndex(aux_att.system_consideration) 
		self.eval_sys_was_comboBox.setCurrentIndex(aux_att.system_was) 
		self.eval_profile_SpinBox.setValue(aux_att.profile)
		
		try:
			self.eval_dist_progressBar.setValue(100 - (aux_att.ans_dist*100))
			self.eval_dist_doubleSpinBox.setValue(aux_att.ans_dist)
			
		except:
			print "NAO"
	
		self.eval_lcdNumber.display(100 - (100*self.cur_eval.ans_threshold))

		if self.cur_eval.stats is not None:

			self.eval_ntopics_lbl.setText(str(self.cur_eval.stats.n_topics))
			self.eval_qt_per_tp_lbl.setText(str(self.cur_eval.stats.qt_tp))
			self.eval_time_per_tp_lbl.setText(str(self.cur_eval.stats.time_per_topic))
			self.eval_mistakes_lbl.setText(str(self.cur_eval.stats.mistakes))
			self.eval_total_qt_lbl.setText(str(self.cur_eval.stats.total_qt))
			self.eval_right_ans_lbl.setText(str(self.cur_eval.stats.right_answers))
			#self.eval_suc_rate_lbl.setText(str(round(self.cur_eval.stats.success_rate),2))
			self.eval_suc_rate_lbl.setText("{:0.2f}".format(self.cur_eval.stats.success_rate))
			self.eval_sys_accuracy_lbl.setText("{:0.2f}".format(self.cur_eval.stats.sys_accuracy))


	def eval_validation_change(self):

		if self.eval_ans_sys_comboBox.currentIndex() ==  self.eval_ans_sup_comboBox.currentIndex():
			result = 1
		else:
			result = 0
		
		
		#print result, self.eval_ans_sys_comboBox.currentIndex(),  self.eval_ans_sup_comboBox.currentIndex()

		self.eval_sys_was_comboBox.setCurrentIndex(result)

		self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].system_was = result
		# self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].supervisor_consideration = self.eval_ans_sup_comboBox.currentIndex()
		# self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].system_consideration = self.eval_ans_sys_comboBox.currentIndex()
		# self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id]

		# print "SUP", self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].supervisor_consideration
		# print "SYS", self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].system_consideration
		# print ""
		
		#self.evaluation_db.insert_eval(self.cur_eval)




	def eval_next_validation_action(self):

		max_tp = len(self.cur_eval.topics)
		max_qt = len(self.cur_eval.topics[0].questions)
		max_att = len(self.cur_eval.topics[0].questions[0].attempts)

		self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].supervisor_consideration = self.eval_ans_sup_comboBox.currentIndex()
		self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].system_consideration = self.eval_ans_sys_comboBox.currentIndex()
		self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].profile = self.eval_profile_SpinBox.value()

		self.evaluation_db.insert_eval(self.cur_eval)

		if (self.tp_id == max_tp-1) and (self.qt_id == max_qt-1) and (self.att_id == max_att-1):
			
			QMessageBox.information(self, "Done!", "All the validation are done!", QMessageBox.Ok )
			
			return 
		
		if self.att_id < (max_att-1):
			self.eval_att_comboBox.setCurrentIndex(self.att_id+1)
		
		elif self.qt_id < (max_qt-1):
			self.eval_questions_comboBox.setCurrentIndex(self.qt_id+1)
			self.eval_att_comboBox.setCurrentIndex(0)
		
		elif  self.tp_id < (max_tp-1):
			self.eval_topic_comboBox.setCurrentIndex(self.tp_id+1)
			self.eval_questions_comboBox.setCurrentIndex(0)
			self.eval_att_comboBox.setCurrentIndex(0)
		
		






	def eval_check_validation(self):
		max_tp = len(self.cur_eval.topics)
		max_qt = len(self.cur_eval.topics[0].questions)
		max_att = len(self.cur_eval.topics[0].questions[0].attempts)
		
		for t in range(max_tp):
			for q in range(max_qt):
				for a in range(max_att):
					if self.cur_eval.topics[t].questions[q].attempts[a].supervisor_consideration== -1:
						return False

		self.cur_eval.validation=True
		return True			




	
	def eval_update_time_tab(self):
		
		#text= str(self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()])
		
		
		
		self.tp_id=self.eval_time_topic_comboBox.currentIndex()
		self.qt_id=self.eval_time_questions_comboBox.currentIndex()
		self.att_id=self.eval_time_att_comboBox.currentIndex()

		tp = self.cur_eval.topics[self.tp_id]
		qt = self.cur_eval.topics[self.tp_id].questions[self.qt_id]
		att = self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id] #Attempt()

		self.eval_time_tp_name_label.setText(self.cur_eval.tp_names[self.tp_id])
		
		self.eval_tp_started_doubleSpinBox.setValue(tp.started)
		self.eval_tp_finished_doubleSpinBox.setValue(tp.finished)

		min_start = tp.started/60
		min_finish = tp.finished/60
		#aux1 = QTime(0,min_start,tp.started)
		#print aux1
		self.eval_tp_started_timeEdit.setTime(QTime(0,min_start,tp.started))
		self.eval_tp_finished_timeEdit.setTime(QTime(0,min_finish,tp.finished))


		# ----- QUESTION ------
		self.eval_qt_started_doubleSpinBox.setValue(qt.started)
		self.eval_qt_finished_doubleSpinBox.setValue(qt.finished)

		min_start = qt.started/60
		min_finish = qt.finished/60
		#aux1 = QTime(0,min_start,tp.started)
		#print aux1
		self.eval_qt_started_timeEdit.setTime(QTime(0,min_start,qt.started))
		self.eval_qt_finished_timeEdit.setTime(QTime(0,min_finish,qt.finished))


		# ----- ATTEMPT ------
		self.eval_att_started_doubleSpinBox.setValue(att.started)
		self.eval_att_finished_doubleSpinBox.setValue(att.finished)

		min_start = att.started/60
		min_finish = att.finished/60
		#aux1 = QTime(0,min_start,tp.started)
		#print aux1
		self.eval_att_started_timeEdit.setTime(QTime(0,min_start, att.started))
		self.eval_att_finished_timeEdit.setTime(QTime(0,min_finish,att.finished))


	def eval_gen_stats_action(self):

		# if not self.eval_check_validation():
		# 	# ERROR
		# 	QMessageBox.critical(self, "Error!", "Some validation missing!", QMessageBox.Ok )
		# 	return False
		
		max_tp = len(self.cur_eval.topics)
		max_qt = len(self.cur_eval.topics[0].questions)
		max_att= len(self.cur_eval.topics[0].questions[0].attempts)

		user_mistakes = 0
		sys_mistakes = 0
		sys_right = 0
		user_right = 0


		for t in range(max_tp):
			for q in range(max_qt):
				for a in range(max_att):
					# if supervisor said the answer was right
					if self.cur_eval.topics[t].questions[q].attempts[a].supervisor_consideration == 1:
						# if system was righ
						if self.cur_eval.topics[t].questions[q].attempts[a].system_consideration == 1:
							sys_right+= 1
						else:
							sys_mistakes+= 1
						
						user_right+= 1
					# if supervisor said the answer is wrong	
					else:
						# system was right
						if self.cur_eval.topics[t].questions[q].attempts[a].system_consideration == 0:
							sys_right+= 1
						else:
							sys_mistakes+= 1

						user_mistakes+= 1	

						
		total_qt = max_att*max_qt*max_att

		user_acc = float(user_right/(total_qt*1.0))
		sys_acc = float(sys_right/(total_qt*1.0))

		stats = Stats(n_topics = max_tp, qt_tp = max_qt, time_per_topic = -1, 
                    mistakes  = user_mistakes, total_qt = total_qt,  right_answers  = user_right,
                    success_rate  = user_acc, sys_accuracy  = sys_acc)

		
		self.cur_eval.stats=stats

		self.evaluation_db.insert_eval(self.cur_eval)

		self.log("EVAL UPDATED")

		self.eval_update_tab()

		self.eval_gen_stats_button.setEnabled(False)



		

	def eval_generate_graph_action(self): 

		
		#print "LIST", tp_qt_x
		#return

		# if self.cur_eval.validation == False:
		# 	# ERROR
			
		# 	QMessageBox.critical(self, "Error!", "Some validation missing!", QMessageBox.Ok )
		# 	return False
	
		
		self.eval_graph_1()
		
		self.eval_graph_2()

		self.eval_graph_3()

		self.eval_open_graphs()
	
		# --------------------------- SYSTEM



	def eval_graph_3(self):
		profile = []
		alpha = []
		beta = []
		gama = []
		fvalues = []

		max_tp = len(self.cur_eval.topics)
		max_qt = len(self.cur_eval.topics[0].questions)
		max_att = len(self.cur_eval.topics[0].questions[0].attempts)
		
		for t in range(max_tp):
			for q in range(max_qt):
				for a in range(max_att):
					aux = self.cur_eval.topics[t].questions[q].attempts[a]

					profile.append(aux.profile)
					alpha.append(aux.alpha)
					beta.append(aux.beta)
					gama.append(aux.gama)
					fvalues.append(aux.fvalue)

		# my_xticks = tp_qt_x
		# x = range(len(tp_qt_x))

		#'''
		
		tp_qt_x = []
		times = [] 

		for t in range(0,len(self.cur_eval.topics)):
			for q in range(0,len(self.cur_eval.topics[0].questions)):
				tp_qt_x.append("T"+str(t+1)+"_q"+str(q+1))	
				times.append(self.cur_eval.topics[t].questions[q].finished - self.cur_eval.topics[t].questions[q].started) 
	
		#print times

		my_xticks = tp_qt_x
		x = range(len(tp_qt_x))

		plt.figure(3)

		#print alpha
		#print x

		#plt.subplot(121)
		plt.xticks(x, my_xticks)
		y = alpha
		plt.plot(x, y, 'o--', color='g',  markersize=12, label="Alpha")
		for a,b in zip(x, y): 
			plt.text(a, b, "{:0.2f}".format(b))

		y=beta
		plt.plot(x, y,  's--', color='r', markersize=12, label="Beta")
		for a,b in zip(x, y): 
			plt.text(a, b, "{:0.2f}".format(b))

		y=gama
		plt.plot(x, y,  'x--', color='y', markersize=12, label="Gama")
		for a,b in zip(x, y): 
			plt.text(a, b, "{:0.2f}".format(b))

		y=fvalues
		plt.plot(x, y,  '*--', color='y', markersize=12, label="Fvalue")
		for a,b in zip(x, y): 
			plt.text(a, b, "{:0.2f}".format(b))


		plt.legend(loc='upper left', numpoints = 1,#('System right ','System Wrong ','Students right answers','Students wrong answers'),
			shadow=True,
			#loc=(0.01, 0.8),
			handlelength=1.5, 
			fontsize=12)

		plt.xlim(-1,len(my_xticks))
		plt.ylim(-.5,1.5)

		plt.title("System Variables", fontsize=32)

		plt.xlabel("Topic_Question Number", fontsize=16)
		plt.ylabel("Value", fontsize=20)
		plt.grid(True, linewidth=.15)
		#plt.show()
		graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/sys_graph"
		#plt.show()
		plt.savefig(graph_name)
		#pixmap = QPixmap(graph_name)
   		#self.eval_evolution_graph.setPixmap(pixmap)
   		#self.eval_evolution_graph.show()







	def eval_graph_1(self):
		labels = [" Right \n Answers", "Wrong \nAnswers"] 
		sizes = [self.cur_eval.stats.right_answers, self.cur_eval.stats.total_qt - self.cur_eval.stats.right_answers]
		
		colors = ['blue', 'red', 'lemonchiffon', 'gold', 'lightskyblue']
		explode = [0.1,0]
		#fig1, ax1 = plt.subplots()
		
		plt.rcParams['font.size'] = 16.0

		plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors= colors,
				shadow=True, startangle=90, explode=explode)
		
		plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

		plt.title("Student's Answers", fontsize=35, y =1.03)
		
		graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/student_performance_graph"
		plt.savefig(graph_name)
		#plt.show()
		# pixmap = QPixmap(graph_name)
   		# self.eval_std_perf_graph.setPixmap(pixmap)
   		# self.eval_std_perf_graph.show()

	def eval_graph_2(self):
		tp_qt_x = []
		times = [] 

		for t in range(0,len(self.cur_eval.topics)):
			for q in range(0,len(self.cur_eval.topics[0].questions)):
				tp_qt_x.append("T"+str(t+1)+"_q"+str(q+1))	
				times.append(self.cur_eval.topics[t].questions[q].finished - self.cur_eval.topics[t].questions[q].started) 
	
		#print times

		my_xticks = tp_qt_x
		x = range(len(tp_qt_x))

		#'''
		
		
		plt.figure(2)


		#plt.subplot(121)
		plt.xticks(x, my_xticks)
		y = times
		plt.plot(x, y, 'o--', color='g',  markersize=12, label="System's correct classifications")
		for a,b in zip(x, y): 
			plt.text(a, b, str(b))

		plt.xlim(-1,len(my_xticks))
		#plt.ylim(-1,33)

		plt.title("System Classifications", fontsize=32)

		plt.xlabel("Topic_Question Number", fontsize=16)
		plt.ylabel("Number of occurrences", fontsize=20)
		plt.grid(True, linewidth=.15)
		#plt.show()
		graph_name = self.evaluation_db.path + str(self.cur_eval.id) + "/student_times_graph"
		plt.savefig(graph_name)
		#plt.show()
		# pixmap = QPixmap(graph_name)
   		# self.eval_time_graph.setPixmap(pixmap)
   		#self.eval_time_graph.show()




	def eval_set_video_time(self, t1, t2):
		t2.setValue(t1.value())


	def eval_play_video(self):
		# self.eval_video_player.play(float(1000*self.eval_current_video_time_doubleSpin.value()))
		self.eval_video_player.play()#float(1000*self.eval_current_video_time_doubleSpin.value()))
		#self.ole_start_eval()



# ------------------------------------- \OLE -- Off Line Evaluation



	def ole_start_eval(self):

		eval_name = "Evaluations/" + str(self.cur_eval.id) +"/" + str(self.cur_eval.id) + '.avi'

		self.log(str("OLE Started with " + str(eval_name)))
		

		if not os.path.isfile(eval_name):
		
			QMessageBox.critical(self,"Video not Found", "\nNo session video found for this evaluation")
			return 
		
		elif (len(self.cur_eval.topics)==0):
			QMessageBox.critical(self,"Topics not Found", "\nNo topic found for this evaluation")
			return
		



		self.n_deviations = self.time_disattention = 0
		self.static_time = self.dynamic_time = self.time_attention = self.time_emotion = time.time()

		self.w = adaption.Weights(0, 0, self.gamaWeight.value())

		self.op_par = adaption.OperationalParameters(
										self.face_dev_activation.value(),
										self.negEmoAct__spinBox.value(),
										self.adp_words_spinBox.value(), #3, #number of words
										self.learningTime_doubleSpinBox.value(),
										1)
		self.read_values=adaption.ReadValues()

		self.adapt_sys = adaption.AdaptiveSystem(
			self.robot,
			self.op_par,
			self.w,
			self.read_values)

		self.ole_cap = cv2.VideoCapture(eval_name)
		self.fps = self.ole_cap.get(cv2.CAP_PROP_FPS)
		total_frames = self.ole_cap.get(cv2.CAP_PROP_FRAME_COUNT)
		self.ole_progressBar.setMaximum(total_frames)
		self.ole_progressBar.setValue(0)
		#convert = int(self.cur_eval.duration)
		#print "DURATION", self.cur_eval.duration
		
		dur = QTime(0,0).addMSecs(self.cur_eval.start_time.msecsTo(self.cur_eval.end_time))
		#print dur
		self.ole_duration_timeEdit.setTime(dur)#QTime(0,0).addMSecs(convert))

		self.ole_max_tp = len(self.cur_eval.topics)
		self.ole_max_qt = len(self.cur_eval.topics[0].questions)
		self.ole_max_att = len(self.cur_eval.topics[0].questions[0].attempts)

		self.ole_cur_eval = copy.deepcopy(self.cur_eval)

		# CHANGE TOPIC
		self.ole_tp_id = 1
		self.ole_qt_id = -1
		self.ole_att_id  = 0

		self.ole_att = self.cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id].attempts[self.ole_att_id]
		self.ole_qt = self.cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id]
		self.ole_tp = self.cur_eval.topics[self.ole_tp_id]

		self.ole_clock = QTime(0,0)

		#print fps
		self.ole_timer = QTimer(self)
		self.ole_timer.timeout.connect(self.ole_update_frame)
		
		# ret = QMessageBox.question(self, "Time", "Evaluation in real time?", QMessageBox.No|QMessageBox.Cancel|QMessageBox.Yes)
		
		# if ret == QMessageBox.Yes:
		prop = 1000.0/self.fps
		
		# elif ret == QMessageBox.No:
		# 	prop = 1

		# else:
		# 	return

		#print prop
		#return 
		self.classified_emotion = "Waiting"
		self.ole_timer.start(prop)
		

		self.ole_question_changed()
		

	def ole_stop_eval(self):

		# self.ole_cap = cv2.VideoCapture(str(self.cur_eval.id)+ '.avi')
		# self.ole_timer = QTimer(self)
		# self.ole_timer.timeout.connect(self.ole_update_frame)
		self.ole_timer.stop()
		self.ole_cap.release()
		# print "OLE STOPED"
		
		''' OLDE VERSIONNN
		dg = QMessageBox.question(self, "Finished", "Off-Line Evaluation Ended!", QMessageBox.Ok|QMessageBox.Cancel)

		if dg == QMessageBox.Ok:

			#print os.listdir("Evaluations/"+str(self.cur_eval.id))
			path = "Evaluations/"+str(self.cur_eval.id)+"/OffLineEvals"
			if not os.path.exists(path):
				os.mkdir(path)

			# print os.listdir(path)
			id_ole = len(os.listdir(path))
			name = str(self.cur_eval.id)+"_"+str(id_ole)+".ole"
	
			filename = QFileDialog.getSaveFileName(self, "Save OffLine Eval", path+"/"+name, "Ole files(*.Ole)")
			
			if filename != "":
				self.evaluation_db.save_eval(self.ole_cur_eval,filename)

				QMessageBox.information(self, "Saved", "Off-Line Evaluation Saved!")
				self.log("Off-Line Evaluation Saved in " + filename )
			else:
				QMessageBox.information(self, "Saved", "Off-Line Evaluation NOT Saved!")
		'''


		path = "Evaluations/"+str(self.cur_eval.id)+"/OffLineEvals"
		if not os.path.exists(path):
			os.mkdir(path)

		# print os.listdir(path)
		id_ole = len(os.listdir(path))
		name = str(self.cur_eval.id)+"_"+str(id_ole)+".ole"

		filename = path+"/"+name
		self.evaluation_db.save_eval(self.ole_cur_eval,filename)

		self.log("Off-Line Evaluation Ended!")
		self.ole_on_course = False

	
	
	
	def ole_update_frame(self):
		


		if(self.ole_cap.isOpened()):
			
			self.ole_progressBar.setValue(self.ole_progressBar.value()+1)
			
			if self.ole_progressBar.value() == self.ole_progressBar.maximum():
				#self.log("ESTOUROU")
				self.ole_stop_eval()
				return

			#rint self.ole_progressBar.value(), self.ole_progressBar.maximum()

			frame_count = self.ole_cap.get(cv2.CAP_PROP_POS_FRAMES)
			ret, frame = self.ole_cap.read()

			frame = self.run_attention_emotion_thread(frame)
			self.ole_emotion_label.setText(self.classified_emotion)
			self.ole_dev_spinBox.setValue(self.n_deviations)
			self.ole_bademo_spinBox.setValue(self.adapt_sys.getBadEmotions())
			runing_time = QTime(0,(frame_count/self.fps)/60,(frame_count/self.fps)%60)
			self.ole_timeEdit.setTime( runing_time )

			# self.ole_qt.finished
			# aux = QTime(0,0).addMSecs(runing_time.msecsTo())
			# aux = QTime(0,0).addMSecs(self.ole_qt.finished)
			aux = self.ole_qt_ends_timeEdit.time()

			diff = runing_time.msecsTo(aux)
			aux = QTime(0,0).addMSecs(diff)
			#print diff, aux
			self.ole_qt_cd_timeEdit.setTime(aux)

			if diff < 0 :
				self.log("Changing question number")
				
				#self.adapt_sys.
				
				self.read_values.set(self.n_deviations,
									self.adapt_sys.getBadEmotions(),
									#self.diag_sys.coutingWords(user_answer),
									len(self.ole_att.given_ans.split()),
									self.ole_att.time2ans,
									self.ole_att.ans_dist)

				# Clear Variables
				self.n_deviation = 0
				self.adapt_sys.clear_emo_variables()

				if (self.adaptation_type=="Fuzzy"):

					pprint(vars(self.read_values))

					values = self.states_fuzzy_control.compute_states(self.read_values)
					alpha = values[0]
					beta = values[1]
					gama = values[2]

					fvalue = self.adaptive_fuzzy_control.compute_fvalue(values) / 10.0


				elif (self.adaptation_type=="Rules"):
 					fvalue, alpha, beta, gama = self.adapt_sys.adp_function(self.ole_qt_id)
					act = self.adapt_sys.activation_function(fvalue)
				
				core.info("Alpha: "+ str(alpha))
				core.info("Beta: "+ str(beta))
				core.info("Alpha: "+ str(gama))
				core.info("FVALUE -> " +str(fvalue))
				core.info("Act -> " +str(act))
				
			 	aux_att = self.ole_cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id].attempts[self.ole_att_id] 

				aux_att.alpha=alpha
				aux_att.beta=beta 
				aux_att.gama=gama 
				aux_att.fvalue=fvalue 
				aux_att.profile=self.adapt_sys.robot_communication_profile+1
				aux_att.read_values=copy.deepcopy(self.read_values)

				self.ole_cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id].attempts[self.ole_att_id] = aux_att 


				self.ole_verticalSlider.setValue(self.adapt_sys.robot_communication_profile+1)


				#Changing the question parameters
				self.ole_question_changed()

			
			if self.eval_ole_display_radioButton.isChecked():
				self.ole_display_img(frame)
			# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# cv2.imshow('frame',gray)
			# if cv2.waitKey(1) & 0xFF == ord('q'):
			# 	break
		else:
			print "Image not found!"
			#cv2.destroyAllWindows()



	def ole_question_changed(self):


		if (self.ole_tp_id == self.ole_max_tp-1) and (self.ole_qt_id == self.ole_max_qt-1) and (self.ole_att_id == self.ole_max_att-1):
			
			#QMessageBox.information(self, "Done!", "All the validation are done!", QMessageBox.Ok )
			
			self.ole_stop_eval()
			return
		
		if self.ole_att_id < (self.ole_max_att-1):
			#self.eval_att_comboBox.setCurrentIndex(self.att_id+1)
			self.ole_att_id+=1


		elif self.ole_qt_id < (self.ole_max_qt-1):
			# self.eval_questions_comboBox.setCurrentIndex(self.qt_id+1)
			# self.eval_att_comboBox.setCurrentIndex(0)
			self.ole_qt_id+=1
			self.ole_att_id=0

		
		elif  self.ole_tp_id < (self.ole_max_tp-1):
			# self.eval_topic_comboBox.setCurrentIndex(self.tp_id+1)
			# self.eval_questions_comboBox.setCurrentIndex(0)
			# self.eval_att_comboBox.setCurrentIndex(0)
			self.ole_tp_id+=1
			self.ole_qt_id=0
			self.ole_att_id=0

		self.ole_att = self.cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id].attempts[self.ole_att_id]
		self.ole_qt = self.cur_eval.topics[self.ole_tp_id].questions[self.ole_qt_id]
		self.ole_tp = self.cur_eval.topics[self.ole_tp_id]


		# ----- SETTING GUI

		self.ole_question_label.setText(self.ole_qt.question)
		self.ole_exp_label.setText(self.ole_qt.exp_ans)
		gave_ans = self.ole_att.given_ans
		self.ole_gave_label.setText(gave_ans)

		self.ole_correctness_doubleSpinBox.setValue(self.ole_att.ans_dist)
		self.ole_time2ans_spinBox_2.setValue(self.ole_att.time2ans)

		words =  len(gave_ans.split()) 

		self.ole_words_spinBox.setValue(words)

		# print frame_count/self.fps
		
		# Question
		self.ole_qt_number_spinBox.setValue(self.ole_qt_id+1)
		begin = self.ole_qt.started
		# print begin
		# print "type", type(begin)
		# convert = 
		# print "convert",convert
		mtime =  QTime(0,0)
		mtime = mtime.addMSecs(int(begin*1000))
		#print mtime
		self.ole_qt_starts_timeEdit.setTime(mtime)

		
		end = self.ole_qt.finished
		mtime = QTime(0,0)
		mtime = mtime.addMSecs(int(end*1000))
		self.ole_qt_ends_timeEdit.setTime(mtime)

		# print end	
		# print mtime.second()

		frame2go = self.fps*begin
		self.ole_cap.set(cv2.CAP_PROP_POS_FRAMES, frame2go)
		self.ole_progressBar.setValue(frame2go	)



	def ole_display_img(self, img):
		qformat = QImage.Format_Indexed8
		if len(img.shape)==3:
				if img.shape[2]==4:
					qformat = QImage.Format_RGBA8888
				else :
					qformat = QImage.Format_RGB888
		
		outImage= QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
		outImage = outImage.rgbSwapped()

		self.ole_img.setPixmap(QPixmap.fromImage(outImage))
		#self.img_from_cam.setScaledContentes(True)






	def ole_batch_eval(self):

		self.modules_tabWidget.setCurrentIndex(7)
		self.eval_frame.setCurrentIndex(5)
		self.run_load_models()


		for self.cur_eval in self.evaluation_db.evaluations_list:
			#self.cur_eval.duration = self.cur_eval.start_time.msecsTo(self.cur_eval.end_time)
			#print self.cur_eval.id, self.cur_eval.duration
			self.ole_on_course = True

			self.ole_start_eval()

			while self.ole_on_course:
				QCoreApplication.processEvents()


		self.log("BATCH FINISEHD")

		#self.eval_batch_find_weights()




	def op_ole_open_action_button(self):

		path = "Evaluations/"+str(self.cur_eval.id)+"/OffLineEvals"
		
		if not os.path.exists(path):
			QMessageBox.critical(self, "Off Line Evals missing", "There are none Off Line Evaluations for this evaluation")
			return

		filename = QFileDialog.getOpenFileName(self, "Save OffLine Eval", path, "Ole files(*.Ole)" )
		
		self.ole_cur_eval = self.evaluation_db.load_eval(filename)
		
		self.op_ole_open_action(filename)


		


	def op_ole_open_action(self, name=""):
		
		name = name.split("/")[-1]

		self.w = adaption.Weights(self.alfaWeight.value(), self.betaWeight.value(), self.gamaWeight.value())

		self.op_par = adaption.OperationalParameters(
										self.face_dev_activation.value(),
										self.negEmoAct__spinBox.value(),
										self.adp_words_spinBox.value(),#3, #number of words
										self.learningTime_doubleSpinBox.value(),
										1)
		
		self.read_values=adaption.ReadValues()

		self.adapt_sys = adaption.AdaptiveSystem(
			self.robot,
			self.op_par,
			self.w,
			self.read_values)


		self.op_ole_name_lineEdit.setText(name)
		self.op_ole_topic_comboBox.clear()
		self.op_ole_questions_comboBox.clear()
		self.op_ole_att_comboBox.clear()

		self.op_ole_topic_comboBox.currentIndexChanged.connect(self.op_ole_update_tab)
		self.op_ole_questions_comboBox.currentIndexChanged.connect(self.op_ole_update_tab)
		self.op_ole_att_comboBox.currentIndexChanged.connect(self.op_ole_update_tab)

		self.op_ole_topic_comboBox.addItems(self.ole_cur_eval.tp_names)
		
		index_list = range(1,len(self.ole_cur_eval.topics[0].questions)+1)
		index_list=["{}".format(x) for x in index_list]
		self.op_ole_questions_comboBox.addItems(index_list)
		
		index_list = range( 1 ,len(self.ole_cur_eval.topics[0].questions[0].attempts)+1)
		index_list=["{}".format(x) for x in index_list]
		self.op_ole_att_comboBox.addItems(index_list)






	def op_ole_update_tab(self):
		
		
		tp_id=self.op_ole_topic_comboBox.currentIndex()
		qt_id=self.op_ole_questions_comboBox.currentIndex()
		att_id=self.op_ole_att_comboBox.currentIndex()

		tp = self.ole_cur_eval.topics[tp_id]
		qt = self.ole_cur_eval.topics[tp_id].questions[qt_id]
		self.aux_att = self.ole_cur_eval.topics[tp_id].questions[qt_id].attempts[att_id] #Attempt()
		rv = self.aux_att.read_values

		self.op_ole_qt_number_spinBox.setValue(qt_id+1)
		
		self.op_ole_dev_spinBox.setValue(rv.deviations)
		self.op_ole_time2ans_spinBox.setValue(rv.time2ans)
		self.op_ole_correctness_doubleSpinBox.setValue(rv.sucRate)
		self.op_ole_bademo_spinBox.setValue(rv.emotionCount)
		self.op_ole_words_spinBox.setValue(rv.numberWord)
		
		self.op_ole_original_verticalSlide.setValue(self.aux_att.profile)


	def op_ole_compute_action(self):

		self.adapt_sys.read_values=self.aux_att.read_values

		self.adapt_sys.w = adaption.Weights(
				self.op_ole_alfaWeight.value(),
				self.op_ole_betaWeight.value(),
				self.op_ole_gamaWeight.value()	)

		fvalue, alpha, beta, gama = self.adapt_sys.adp_function(self.op_ole_qt_number_spinBox.value())
		achieved = self.adapt_sys.activation_function(fvalue)

		self.op_ole_alpha_DoubleSpinBox.setValue(alpha)
		self.op_ole_beta_DoubleSpinBox.setValue(beta)
		self.op_ole_gama_DoubleSpinBox.setValue(gama)
		self.op_ole_fValue_DoubleSpinBox.setValue(fvalue)

		# self.op_ole_achieved_verticalSlide.setValue(self.op_ole_achieved_verticalSlide.value() + achieved)
		self.adapt_sys.change_behavior(achieved)

		# self.preview_profile = self.user_profile 
		self.user_profile = self.adapt_sys.robot_communication_profile+1
		
		# self.log("ACHIEVED "+ str(achieved))

		self.op_ole_achieved_verticalSlide.setValue(self.user_profile)









	def eval_best_fit_fuzzy(self):

		# best_weights = np.zeros((10,10,10))

		self.set_adaptive_fuzzy_parameters()

		self.w = adaption.Weights(0,0,0)#self.alfaWeight.value(), self.betaWeight.value(), self.gamaWeight.value())

		ff = open("Read_values.txt", "w")

		ff.write(
				str("Eval ID")+ " , " +    
				str("Question #") + " , " +    
				str("Deviations")+ " , " +    
				str("EmotionCount")+ " , " +    
				str("NumberWord")+ " , " +    
				str("SucRate")+ " , " +    
				str("Time2ans")+ " , " +    
				str("Alpha")+ " , " +    
				str("Beta")+ " , " +    
				str("Gama")+ " , " +    
				str("Achieved")+ " , " +    
				str("Original")+ " , " +    
				str("Cur Level")+ "\n ")    
		

		self.op_par = adaption.OperationalParameters(
										self.face_dev_activation.value(),
										self.negEmoAct__spinBox.value(),
										self.adp_words_spinBox.value(),#3, #number of words
										self.learningTime_doubleSpinBox.value(),
										1)
		
		self.read_values=adaption.ReadValues()

		self.adapt_sys = adaption.AdaptiveSystem(
			self.robot,
			self.op_par,
			self.w,
			self.read_values)


		right = 0
		wrong = 0

		for self.cur_eval in self.evaluation_db.evaluations_list:

		#self.cur_eval = self.evaluation_db.evaluations_list[0]
		

			path = "Evaluations/"+str(self.cur_eval.id)+"/OffLineEvals/"+str(self.cur_eval.id)+"_0.ole"
		
			self.ole_cur_eval = self.evaluation_db.load_eval(path)
			#self.op_ole_open_action(filename)
			
			tp = self.ole_cur_eval.topics[1]
			matches = 0 

			# for wa in range(10):
			# 	for wb in range(10):
			# 		for wg in range(10):

			#self.adapt_sys.w=adaption.Weights(wa/10.0, wb/10.0, wg/10.0)
			#fitness = 0
			cur_level = 3
			for qt in range(3):
				
				try:
					original = tp.questions[qt+1].attempts[0].profile
				except:
					original = self.ole_cur_eval.user_dif_profile

				rv = tp.questions[qt].attempts[0].read_values

				rv.sucRate = 10-rv.sucRate*10

				self.read_values=rv


				try:
					values = self.states_fuzzy_control.compute_states(self.read_values)
					right+=1
				except Exception as ex:
					self.log("Evaluation number {} with problems in question {}".format(self.cur_eval.id, qt+1 ), "e")
					self.log('ERROR: \n {}'.format(ex), 'e')
					wrong+=1
					#ff.write(" 		ERROR\n")
					
					continue
				
				#ff.write('\n')

				alpha = values[0]
				beta = values[1]
				gama = values[2]

				#core.info("Alpha Fuzzy: "+ str(alpha))
				#core.info("Beta Fuzzy: "+ str(beta))
				#core.info("Gama Fuzzy: "+ str(gama))
				fvalue = self.adaptive_fuzzy_control.compute_fvalue(values) / 10.0
				core.info("FVALUE -> " +str(fvalue))

				#fvalue, alpha, beta, gama = self.adapt_sys.adp_function(qt)

				achieved = self.adapt_sys.activation_function(fvalue)
				
				cur_level += achieved

				if original == cur_level:
					print original, cur_level
					#best_weights[wa][wb][wg]+=1
					matches += 1

				ff.write(
					str(self.cur_eval.id)+ " , " +    
					str(qt+1)+ " , " +    
					"{:.2f}".format(self.read_values.deviations)+ " , " +    
					"{:.2f}".format(self.read_values.emotionCount)+ " , " +    
					"{:.2f}".format(self.read_values.numberWord)+ " , " +    
					"{:.2f}".format(self.read_values.sucRate)+ " , " +    
					"{:.2f}".format(self.read_values.time2ans)+ " , " +    
					"{:.2f}".format(alpha)+ " , " +    
					"{:.2f}".format(beta)+ " , " +    
					"{:.2f}".format(gama)+ " , " +    
					str(achieved)+ " , " +    
					str(original)+ " , " +    
					str(cur_level)+ "\n ")    
					



		# out = open("Evaluations/weights.csv","w+")

		# for wa in range(10):
		# 	for wb in range(10):
		# 		for wg in range(10):
		# 			out.write(str(wa/10.0)+","+str(wb/10.0)+","+str(wg/10.0)+","+str(best_weights[wa][wb][wg])+"\n")

		# out.close()
		ff.close()
		self.log("\n\nEnded with {} matches!".format(matches))
		print "Right:", right
		print "Wrong:", wrong














	def eval_batch_find_weights(self):


		best_weights = np.zeros((10,10,10))

		self.w = adaption.Weights(0,0,0)#self.alfaWeight.value(), self.betaWeight.value(), self.gamaWeight.value())

		self.op_par = adaption.OperationalParameters(
										self.face_dev_activation.value(),
										self.negEmoAct__spinBox.value(),
										self.adp_words_spinBox.value(),#3, #number of words
										self.learningTime_doubleSpinBox.value(),
										1)
		
		self.read_values=adaption.ReadValues()

		self.adapt_sys = adaption.AdaptiveSystem(
			self.robot,
			self.op_par,
			self.w,
			self.read_values)



		for self.cur_eval in self.evaluation_db.evaluations_list:

		#self.cur_eval = self.evaluation_db.evaluations_list[0]
		

			path = "Evaluations/"+str(self.cur_eval.id)+"/OffLineEvals/"+str(self.cur_eval.id)+"_0.ole"
		
			self.ole_cur_eval = self.evaluation_db.load_eval(path)
			#self.op_ole_open_action(filename)
			
			tp = self.ole_cur_eval.topics[1]
			matches = 0 

			for wa in range(10):
				for wb in range(10):
					for wg in range(10):

						self.adapt_sys.w=adaption.Weights(wa/10.0, wb/10.0, wg/10.0)
						#fitness = 0
						cur_level = 3
						for qt in range(3):
							
							try:
								original = tp.questions[qt+1].attempts[0].profile
							except:
								original = self.ole_cur_eval.user_dif_profile

							rv = tp.questions[qt].attempts[0].read_values

							self.adapt_sys.read_values=rv

							fvalue, alpha, beta, gama = self.adapt_sys.adp_function(qt)
							achieved = self.adapt_sys.activation_function(fvalue)
							
							cur_level += achieved

							if original == cur_level:
								print original, cur_level
								best_weights[wa][wb][wg]+=1
								matches += 1

		out = open("Evaluations/weights.csv","w+")

		for wa in range(10):
			for wb in range(10):
				for wg in range(10):
					out.write(str(wa/10.0)+","+str(wb/10.0)+","+str(wg/10.0)+","+str(best_weights[wa][wb][wg])+"\n")

		out.close()

		
		self.log("\n\nEnded with {} matches!".format(matches))

# ------------------------------------ \GROUP EVAL
	
	def grup_eval_update_tab(self):

		self.group_eval_comboBox.addItems(self.evaluation_db.group_list)
		#print self.evaluation_db.group_list


	def group_gen_status(self, group_name, tp_range=None, time_threshold=10):

		durations = []
		measures = [[],[],[],[],[]]
		if tp_range is None:
			tp_range = [0,10]

		for item in self.evaluation_db.evaluations_list:

			if item.group==group_name:

				item.duration = item.start_time.secsTo(item.end_time)	

				if item.duration < time_threshold:
					continue

				durations.append(item.duration)
				for tp in item.topics[tp_range[0]:(tp_range[1]+1)]:
					for qt in tp.questions:
						for at in qt.attempts:
							measures[0].append(at.alpha)
							measures[1].append(at.beta)
							measures[2].append(at.gama)
							measures[3].append(at.fvalue)
							measures[4].append(at.profile)
				#print measures

		#print duration
		#print len(durations)
		return durations, measures





	def group_eval_generate_action(self):

		group = self.group_eval_comboBox.currentText()
		self.group_eval_tabWidget.setEnabled(True)
		#table_name="Test1.csv"
		eval_name= str(self.group_eval_name_lineEdit.text())
		#eval_name = table_name
		table_name="Evaluations/Groups/"+eval_name+".csv"

		tp_range = [0,1]

		self.evals_to_csv(group, table_name, tp_range)

		durs, mea = self.group_gen_status(group, tp_range)
		# print len(mea[0])
		# exit()
		self.group_eval_data_table = pd.read_csv(table_name)
		data = self.group_eval_data_table

		dataframe_to_table(self.group_eval_data_table, self.group_eval_tableWidget)
		self.group_eval_tableWidget.resizeColumnsToContents()
		self.group_eval_tableWidget.resizeRowsToContents()

		#[u'Name', u'Duration', u'Topic', u'Interaction_name', u'Question_number',
		#    u'Dificult', u'Question', u'Exp_ans', u'Under_ans', u'Sup_ans',
		#    u'Sys_ans', u'Sys_was', u'Time_to_answer'],
		#   dtype='object')
		#print self.group_eval_data_table["Name"][0]

		dur_av = float(sum(durs)/len(durs))
		dur_sd = np.std(durs)

		sr = data[data['Sys_was']==1].index.size
		sw = data[data['Sys_was']==0].index.size
		sa = int(float(sr)/float(data['Sys_was'].index.size)*100)
		
		ur = data[data['Sup_ans']==1].index.size
		t = data['Sup_ans'].index.size
		ua = int(float(ur)/float(t) *100)
		uw = data[data['Sup_ans']==0].index.size

		# exit()
		#print "SIZE",sa 
		filename = self.evaluation_db.path +"Groups/"+eval_name

		aux = GroupStatus(20,table_name,filename,group,durs, dur_av, 
							dur_sd, mea,len(durs), ur, ua, uw,
							sr, sa, sw )

		
		#print filename
		gt = graphics.users_group_eval(self,data,filename)  

		aux.graphs_trans['User Validation']=gt[0]
		aux.graphs_trans['System Validation']=gt[1]
		aux.graphs_trans['User Accuracy']=gt[2]
		aux.graphs_trans['System Accuracy']=gt[3]

		#print aux.graphs_trans
		self.cur_group_eval=aux
		self.group_eval_open_action(aux)

		aux.save_group_eval( filename+".group")
		
		return




	def group_eval_open_button_pressed(self):

		filename = QFileDialog.getOpenFileName(self, "Open Eval",self.evaluation_db.path+"/Groups", "Group files(*.group)")
		#print filename
		#aux = GroupStatus(0,"")
		self.group_eval_tabWidget.setEnabled(True)		
		self.cur_group_eval = load_group_eval(filename) 
		self.group_eval_open_action(self.cur_group_eval)
		#print self.group_eval.group_name
		#exit()
		





	def group_eval_open_action(self, group_eval):

		self.group_id_spinBox.setValue(group_eval.id)
		
		self.group_name_lineEdit.setText(group_eval.group_name)
		self.group_int_lineEdit.setText(group_eval.path)
		self.group_savedname_lineEdit.setText(group_eval.name)
		self.group_participants_spinBox.setValue(group_eval.participants)
		self.group_total_questions_spinBox.setValue(group_eval.users_right_rate + group_eval.users_wrong_rate)
		self.group_timeAv_doubleSpinBox.setValue(group_eval.dur_av)
		self.group_timeSd_doubleSpinBox.setValue(group_eval.dur_sd)

		self.group_ur_spinBox.setValue(group_eval.users_right_rate)
		self.group_uw_spinBox.setValue(group_eval.users_wrong_rate)
		self.group_ua_spinBox.setValue(group_eval.users_accuracy)

		self.group_sr_spinBox.setValue(group_eval.system_right_rate)
		self.group_sw_spinBox.setValue(group_eval.system_wrong_rate)
		self.group_sa_spinBox.setValue(group_eval.system_accuracy)
		self.group_obs_textEdit.setText(group_eval.obs)

		tablepath= group_eval.name
		#print tablepath
		
		self.group_eval_data_table = pd.read_csv(str(tablepath))
		data = self.group_eval_data_table
		dataframe_to_table(self.group_eval_data_table, self.group_eval_tableWidget)

		#self.group_graph_type_comboBox.addItems(['User Validation', 'System Validation','User Accuracy','System Accuracy'])
		self.group_eval_change_graph()
		self.cur_group_eval=group_eval

	def group_eval_wide_graph(self):
		path = self.cur_group_eval.graphs_trans[str(self.group_graph_type_comboBox.currentText())]
		#filename = self.cur_group_eval.graphs_trans()
		graph = Show_graph(path,self)
		graph.setWindowModality(Qt.ApplicationModal)
		graph.show()
		pass

	
	def group_eval_change_graph(self):
		
		path = self.cur_group_eval.graphs_trans[str(self.group_graph_type_comboBox.currentText())]
		
		self.group_display_graph.setPixmap(QPixmap(path))


	def group_eval_save_action(self):
		
		#group_eval = GroupStatus(self.group_id_spinBox.value(), 
		#				self.group_name_lineEdit.text())
		
		group_eval = self.cur_group_eval
		
		group_eval.group_name =self.group_int_lineEdit.text()
		group_eval.name=self.group_savedname_lineEdit.text()
		group_eval.participants=self.group_participants_spinBox.value()
		#=self.group_total_questions_spinBox.value(group_eval.users_right_rate + group_eval.users_wrong_rate)
		group_eval.dur_av=self.group_timeAv_doubleSpinBox.value()
		group_eval.dur_sd=self.group_timeSd_doubleSpinBox.value()
		group_eval.users_right_rate=self.group_ur_spinBox.value()
		group_eval.users_wrong_rate=self.group_uw_spinBox.value()
		group_eval.users_accuracy=self.group_ua_spinBox.value()
		group_eval.system_right_rate=self.group_sr_spinBox.value()
		group_eval.system_wrong_rate=self.group_sw_spinBox.value()
		group_eval.system_accuracy=self.group_sa_spinBox.value()
		group_eval.obs=self.group_obs_textEdit.toPlainText()

		filename = QFileDialog.getSaveFileName(self, "Save Eval",self.evaluation_db.path+"/Groups", "Group files(*.group)")
		filename = str(filename)
		group_eval.path = filename
		group_eval.save_group_eval(filename)
		#print group_eval.path














#-------------------------------------------------- \INTERACTION ----------------------------------------



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
		#self.sys_vars.add('interaction')
		
	
	def int_load_action(self):
		
		aux_path = self.act.path+"/"+"Interactions"
		
		if len(os.listdir(aux_path)) == 0:

			QMessageBox.information(self, 'Loading Interations',"No Interactions saved" ,QMessageBox.Ok)

			return 0

		filename = QFileDialog.getOpenFileName(self, 'Open File' ,self.act.path+"/"+"Interactions")


		# if self.shortcut:
		# 	filename = self.act.path+"/"+"Interactions/First_int.int"
		# else:
		# 	#/home/tozadore/Projects/Arch_2/Arch_2_1/Activities/NOVA/Interactions
		# 	filename = QFileDialog.getOpenFileName(self, 'Open File' ,self.act.path+"/"+"Interactions")
		

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

		self.cur_interact = Interaction(self.sys_vars.interaction_id,
											self.int_ques_per_top.value(),
											self.int_att_per_ques.value(),
											self.int_name_linedit.text(),
											data=data
												)
		
		
		self.interact_database.save_interact(
						self.cur_interact,
						self.interact_database.path+"/"+str(self.int_name_linedit.text())+ ".int"
						)


	def int_delete_line_action(self):


		# # print self.students_database.users[self.st_db_index_table.currentRow()]
		# user2kill = self.students_database.users[self.st_db_index_table.currentRow()]

		# self.students_database.delete_user(user2kill)
		# dataframe_to_table(self.students_database.index_table, self.st_db_index_table)
		self.int_timeline_table.removeRow(self.int_timeline_table.currentRow())


	def int_lock_action(self):
		
		self.int_save_action()
		self.int_change_enable()
	
		# LOAD GROUP EVAL COMBOBOX
		self.run_group_eval_comboBox.clear()
		self.run_group_eval_comboBox.addItems(self.evaluation_db.group_list)

		print 

		#self.pushButton_run_activity.setEnabled(True)
		self.run_int_name_label.setText(self.cur_interact.name)
		self.run_int_id_spinBox.setValue(self.cur_interact.id)
		self.modules_tabWidget.setCurrentIndex(10)

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

		text = str(self.int_extra_comboBox.currentText())

		if text == 'Dialogue':
			self.int_timeline_table.setItem(self.int_timeline_table.rowCount()-1, 0, QTableWidgetItem("Dialogue"))
			filename = QFileDialog.getOpenFileName(self, 'Open File', self.act.path+"/Dialog")
			name = QFileInfo(filename).fileName()
			filename = str(filename)
			#print (url)
			#filename = filename.replace(self.act.path+"/Dialog",'')
			#filename = filename.replace(".txt",'')
			self.int_timeline_table.setItem(self.int_timeline_table.rowCount()-1, 1, QTableWidgetItem(name))						


		else:	
			self.int_timeline_table.setItem(self.int_timeline_table.rowCount()-1, 0, QTableWidgetItem("Extra"))
			self.int_timeline_table.setItem(self.int_timeline_table.rowCount()-1, 1, QTableWidgetItem(self.int_extra_comboBox.currentText()))						







#-------------------------------------------------- \RUN ----------------------------------------

	def start_activity(self):
		
		# if self.robot is None:
		# 	self.capture = cv2.VideoCapture(0)

		# 	if not self.capture.isOpened():
		# 		QMessageBox.critical(self, "ERROR!", " Unable to open camera!", QMessageBox.Ok)
				
		# 		self.interatction_parser()
				
				
		# 		return -1

		#self.run_robot_connect_button.setEnabled(False)
		self.pushButton_run_activity.setEnabled(False)
		self.run_end_activity_button.setEnabled(True)
		self.run_frame_tracking.setEnabled(True)
		self.run_frame_int_settings.setEnabled(False)
		self.run_next_step_button.setEnabled(True)
		self.run_frame_dialog.setEnabled(True)


		del self.cur_eval #=  Evaluation()	
		self.cur_eval =  Evaluation(
								id=self.sys_vars.evaluation_id,
								date=QDate.currentDate(),
								start_time=QTime.currentTime(),
								supervisor=self.supervisor,
								ans_threshold=self.answer_threshold
								#topics = [],
								#tp_names=[] 	
								)
		
		#self.cur_eval.tp_names = []
		#self.cur_eval.topics = []
		
		#self.run_options_frame.setEnabled(True)
		#self.pushButton_start_robot_view.setEnabled(True)
		#self.pushButton_stop_robot_view.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(False)
		self.run_facerecog_pushButton.setEnabled(False)
		#self.run_takepic_pushButton.setEnabled(True)
		#self.run_recvid_button.setEnabled(True)

		self.adapt_sys.out_path = str(self.cur_eval.id)
		
		self.user_profile=3
		
		self.timer.start()
		#self.counter_timer.restart()
		self.counter_timer.start()
		self.clock_timer.start(1000)
		
		# -- Initializing AUdio Recording
		if self.aud_rec_flag:
			self.aud_rec = AudioRecording.AudioRecording()
			self.aud_rec_thread = AudioRecording.ThreadAudioRecording(self.aud_rec, 'set')
			self.aud_rec_thread.start()
			#self.aud_rec_thread.join()

		if self.nao_connected:
			if self.run_autovideo_checkBox.isChecked():
				self.robot.audio_recording.startMicrophonesRecording(
						self.path_nao_records + "/" + str(self.cur_eval.id)+ ".wav" , 'wav', 16000, (0,0,1,0)
						)
				
				self.robot.video_recording.setFrameRate(10.0)
				self.robot.video_recording.setResolution(2)
				self.robot.video_recording.startRecording(self.path_nao_records, str(self.cur_eval.id))
		# Emotion not running
		#self.run_att_emo()
		
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

			
		
		#WAKEUP
		self.robot.motors.wakeUp()
				
		# Não conehce
		#self.interact_know_person()
		
		#Já conhece
		#self.interact_recognize_person()
		
		# Start interaction engine
		self.interatction_parser()
		self.display_flag = True 
		#self.pushButton_run_activity.setEnabled(True)



	def run_end_activity(self):

		#  if self.robot is not None:
		# 	self.vis_sys.unsub(0)
		self.pushButton_run_activity.setEnabled(True)
		self.run_end_activity_button.setEnabled(False)
		self.run_frame_int_settings.setEnabled(True)
		
		self.timer.stop()
		
		self.clock_timer.stop()



		#self.cur_eval.
		#self.cur_eval.
		#self.cur_eval.
		
		self.cur_eval.end_time = QTime.currentTime()
		secs = self.cur_eval.start_time.secsTo(self.cur_eval.end_time)
		#print"DURRR", secs
		
		sec = QTime(0,0,second=secs )

		#print sec

		self.cur_eval.duration = sec#self.cur_eval.start_time.secsTo(self.cur_eval.end_time)

		if self.cur_user is not None:		
			self.cur_eval.user_name = (self.cur_user.first_name) + " "+ (self.cur_user.last_name)
		else:
			self.cur_eval.user_name = "None"

		self.cur_eval.user_dif_profile = self.user_profile
		self.cur_eval.group = str(self.run_group_eval_comboBox.currentText())
		self.cur_eval.int_id = self.cur_interact.id

		if self.evaluation_db.insert_eval(self.cur_eval) > 0:
			self.sys_vars.add('evaluation')
			#self.evaluation_db.add_evaluation_group(str(self.run_group_eval_comboBox.currentText()))


		dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)

		self.run_frame_tracking.setEnabled(False)
		#self.run_frame_robot_resources.setEnabled(True)
		self.run_frame_dialog.setEnabled(False)
		#self.run_frame_robot_view.setEnabled(True)
		
		if self.nao_connected:
			if self.run_autovideo_checkBox.isChecked():
				self.robot.audio_recording.stopMicrophonesRecording()
				self.robot.video_recording.stopRecording()
				
				#ssh_transfer()
				self.flag_ssh = [True]
				print "antes", self.flag_ssh[0]
				t1 = threading.Thread(name="ssh", target=ssh_transfer,args=(self.robot_ip, str(self.cur_eval.id), self.flag_ssh))
		#self.pushButton_run_activity.setEnabled(True)
				t1.start()

				# while self.flag_ssh[0]:
				# 	QCoreApplication.processEvents()
				t1.join()
				print "DEPOIS", self.flag_ssh[0]

		sentence = " Would you like to perform data validation of this session right now?"

		#change = QMessageBox.information(self, "Finished!", sentence, QMessageBox.Ok | QMessagebox.Cancel )
		ret = QMessageBox.warning(self, "This sessions has ended", sentence, 					
									QMessageBox.Cancel | QMessageBox.Ok )
			
		if ret == QMessageBox.Ok:
			self.modules_tabWidget.setCurrentIndex(7)
			self.eval_open()


	def run_connect_robot_action(self):
		
		self.robot_ip = str(self.run_robot_ip_comboBox.currentText())
		robot_port = int(self.run_robot_port.text())
		
		try:
			self.robot=core.Robot(self.robot_ip, robot_port)
			self.nao_connected = True
			#self.run_robot_connect_button.setEnabled(False)


		except:
			self.nao_connected = False

			ret = QMessageBox.critical(self, "Error!", "ROBOT NOT CONNECT!\n Continue with computer resources?", 
									QMessageBox.Cancel | QMessageBox.Ok )
			
			if ret == QMessageBox.Ok:

				if self.robot is None:
					self.capture = cv2.VideoCapture(0)
					core.info("CAMERA OPENED")

					if not self.capture.isOpened():
						QMessageBox.critical(self, "ERROR!", " Unable to open camera!", QMessageBox.Ok)
						
						#self.interatction_parser()
						
						core.er("CAMERA NOT CONNECTED")
						return -1

			else:
				core.info("Aborting due to camera issues.")
				self.log("Aborting due to camera issues.")	
				return -1
		
		
			
			
			
			#return	

		self.vis_sys = vision.VisionSystem(self.robot)
		self.diag_sys = dialog.DialogSystem(self.robot, None)
		#self.embeddings = self.diag_sys.load()		
		self.embeddings = None#self.diag_sys.load()		
		
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
		
		#Fuzzy
		#if (self.adaptation_type == "Fuzzy"):
		
		core.info("Loading Models!")
		#self.run_load_models()
		
		#self.diag_sys.say("Estou Pronto.", False)
	

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_frame)
		self.timer.start(5)

		self.clock_timer = QTimer()
		self.counter_timer = QTime()
		self.clock_timer.timeout.connect(self.showTime)
		self.clock_timer.start(1000)
		self.clock_timer.stop()
		time = QTime.currentTime()
		#time = time.toString('hh:mm:ss') 
		#self.cur_sess=SessionInfo(time,None)
		self.counter_timer.start()
		
		if self.robot is not None:
			self.vis_sys.subscribe(0)
		
		#self.run_robot_connect_button.setEnabled(False)
		self.run_connection_frame.setEnabled(False)
		self.run_frame_int_settings.setEnabled(True)
		self.run_frame_robot_resources.setEnabled(True)
		self.run_frame_dialog.setEnabled(True)
		self.run_frame_robot_view.setEnabled(True)
		self.pushButton_run_activity.setEnabled(True)
		self.run_end_activity_button.setEnabled(False)
		#self.pushButton_start_robot_view.setEnabled(True)
		#self.pushButton_stop_robot_view.setEnabled(True)
		self.frame_57.setEnabled(True)
		self.run_reset_button.setEnabled(False)
		self.run_emotion_pushButton.setEnabled(True)
		#self.run_next_step_button.setEnabled(False)
		self.run_user_answer.setEnabled(False)
		self.run_reset_button.setEnabled(False)
		self.run_emotion_pushButton.setEnabled(False)
		
		
		#self.robot_say("Estou Pronto.", False)
		self.robot_say("I am ready.", False)
		core.info("Robot Connected")






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

		#print "TYPE ", type(self.cur_interact.data.iloc[0]['Type'])

		for i in range(0,cmds):
			core.info("Inside parser " + str(i) + "  " + self.cur_interact.data.iloc[i]['Type'])
			
			if self.aud_rec_flag:
				self.aud_rec_thread.join()

			self.run_phase.setText(QString.fromUtf8(self.cur_interact.data.iloc[i]['Name']))

			if self.cur_interact.data.iloc[i]['Type'] == "Content":
				self.content_interac_template(self.cur_interact.data.iloc[i]['Name'])

			if self.cur_interact.data.iloc[i]['Type'] == "Personal":
				print "Personal", self.cur_interact.data.iloc[i]['Name']
				self.personal_interact_talk(self.cur_interact.data.iloc[i]['Name'])

			if self.cur_interact.data.iloc[i]['Type'] == "Dialogue":
				#print "Extra: ", self.cur_interact.data.iloc[i]['Name']
				self.diag_process_dialogue(self.cur_interact.data.iloc[i]['Name'])

			if self.cur_interact.data.iloc[i]['Type'] == "Extra":
				#print "Extra: ", self.cur_interact.data.iloc[i]['Name']
				#self.extra_interact(self.cur_interact.data.iloc[i]['Name'])
				if self.cur_interact.data.iloc[i]['Name'] == 'Register User':
					self.interact_know_person()

				elif self.cur_interact.data.iloc[i]['Name'] == 'Recognize User':
					self.interact_recognize_person()
					


		#self.run_final_dialog()		
		self.run_end_activity()	


	def personal_interact_talk(self, talk_subject):

		core.info("Inside personal interact")

		talk_subject = str(talk_subject).lower()

		pref  = self.cur_user.preferences[talk_subject]

		#print pref 
		x = random.randint(0,1)

		if x > 0:
			# self.robot_say("Deixe-me ver se lembro do que você gosta")
			self.robot_say("Lets talk about your interests.")
		else:
			# self.robot_say("Você me contou do que gostava. deixa eu lembrar.")
			self.robot_say("Let me guess your interests.")

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
			else:
				#pref = pref.decode('utf-8')#.strip()
				# pref = pref.encode('utf-8')
				pref = str(pref)#.encode('utf-8')
			

			self.robot_say("You have an interest for  " + pref )
			
		concept_list = [ x.encode('utf-8') for x in self.knowledge_general_df['Concept'].tolist() ]
		#concept_list = [ x.decode('utf-8')for x in self.knowledge_general_df['Concept'].tolist() ]
		
		#print "PREF", pref
		#print "CONCEPT", concept_list

		if pref == "não sei".decode('utf-8') or pref == "não tenho".decode('utf-8') or pref == "eu não tenho".decode('utf-8'):
			self.robot_say("Não tem problema.")
		
		else:
			try:	
				pref = pref.encode('utf-8')
			except:
				pass 

				
			if pref in concept_list:	
			#if pref in concept_list:	
				#self.robot_say("Eu sei o que é isso!")
				self.robot_say("I think I know what it is")
				ind = concept_list.index(pref)#).decode('utf-8'))	
				
				#tosay = u' '.join(self.knowledge_general_df['Definition'][ind]).encode('utf-8')
				tosay = (self.knowledge_general_df['Definition'][ind]).encode('utf-8')
				
				#print "STRING" ,tosay,  type(tosay)
				#print	

				self.robot_say(tosay)
			
			else:
				self.robot_say("I do not have it in my database. Let me search for it on the internet", False)
				# self.robot_say("Só um momento. Eu não conheço nada sobre isso ainda. Vou pesquisar na internet!", False)
				
				tosay=self.know_add_information(pref) 
				
				if tosay is not None:
					self.robot_say("Done! Found it.")
					# self.robot_say("Pronto!")
					self.robot_say(tosay.encode('utf-8'))
				else:
					self.robot_say("Sorry. It was not possible to find it now. Will serach for it later")	
					# self.robot_say("Não consegui encontrar nada sobre isso. Vou procurar melhor e depois te falo")	

			# self.robot_say("Porque você gosta disso?")
			# self.user_input()


	def interact_recognize_person(self):

        # print ""

		self.log("Generating econdings")
		self.students_database.generate_encodings()
		self.log("Econdings Done")
		#self.robot.posture.
		self.run_display_image_radioButton.setChecked(True)
		self.recog_flag=True

		self.cur_user=None
		while self.cur_user is None:
		# for i in range(0,50):
			QCoreApplication.processEvents()
			self.cur_user= self.students_database.get_user(self.recog_user_id)

		#self.cur_user = self.students_database.get_user()

		self.recog_flag=False


		self.run_display_image_radioButton.setChecked(False)


		#self.robot_say("Eu me lembro de você.")
		self.robot_say("Oh. I remember you.")
		
		try:
			nome = str(self.cur_user.first_name)
			#self.robot_say("Você se chama " + nome)
			self.robot_say("Your name is " + nome)
		except:
			nome = self.cur_user.first_name.encode('utf-8')
			#self.robot_say("Você se chama " + nome)
			self.robot_say("Your name is " + nome)

		self.robot_say("Please to meet you again")

		return True	
		
		
		sport = self.cur_user.preferences['sport']#.toUtf8())
		
		if type(sport) == QtCore.QString:
			sport = str(sport.toUtf8())
		
		else:

			#sport = self.cur_user.preferences['sport'].toUtf8()
			sport = str(self.cur_user.preferences['sport'])
		
		
		try:
			self.robot_say("Your favorite sport is " + sport)
			# self.robot_say("Eu lembro que seu esporte preferido é " + sport)
		except:	
			try:
				self.robot_say("Eu lembro que seu esporte preferido é " + sport.encode('utf-8'))
			except:
				pass


		music = (self.cur_user.preferences['food'])#.toUtf8()
		
		# if type(music) == QtCore.QString:
		# 	music = music.toUtf8()
		
		try:
			self.robot_say("E que você também gosta de comer " + music)
		except:
			try:
				self.robot_say("E que você também gosta de comer " + music.encode('utf-8'))
			except:
				pass

		#sport = self.cur_user.preferences['sport'].encode('utf-8')
		#self.robot_say("Eu lembro que seu esporte preferido é " + sport)
		
		#music = self.cur_user.preferences['food'].encode('utf-8')
		#self.robot_say("E que você também gosta de comer " + music)
		#self.robot_say("Não é mesmo?")






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

		#self.robot_say("Olá amiguinho. Nós ainda não nos conhecemos. Eu me chamo Tédi.") 
		# self.robot_say("Hey! We don't know each other. I'm Joaquim!") 
		self.robot_say("Let me know you better.") 
		
		
		self.robot_say("What is your name?", False)
		name = self.user_input()#.decode('utf-8')

		self.robot_say("And the last name?")
		last_name = self.user_input()#.decode('utf-8')

		# self.display_flag =True
		# self.run_display_image_radioButton.setChecked(True)
		
		if self.robot is not None:
			self.image = self.vis_sys.get_img(0)

			self.image = cv2.flip(self.image,1)
		else:
			ret, self.image=self.capture.read()

		self.displayImage(self.image)

		self.cur_user = User(self.sys_vars.users_id+1,
						name,
						last_name,
						bday=QDate.currentDate(),
						img=self.image,
						creation_date=QDate.currentDate())

		# self.run_display_image_radioButton.setChecked(False)
		# self.display_flag =False

  
		self.cur_user.setPreferences()

		if self.students_database.insert_user(self.cur_user)	> 0:
			self.sys_vars.add('user')

		self.log("User " + name + " added!")

		self.robot_say("Please to meet you, " + name)
		#self.robot_say("Let's start!")
		
		try:
			self.run_recognized_user_label.setText(name)
			
		except expression as identifier:
			pass



	#recieve the Topic To Approach (tta)
	def content_interac_template(self, tta):

		
		core.info("INSIDE CONTENT FUNCTON " + tta)
		#print self.sub_list
		
		self.preview_profile = 3	
		self.user_profile = 3	
		self.adapt_sys.robot_communication_profile=2


		core.info("Initializing emotion thread")
		#self.run_emotion_flag = True

		ind = self.sub_list[self.sub_list['subjects']==tta].index[0]
		
		text = self.sub_list['concepts'].iloc[ind]
		
		#started_time = QTime.currentTime()


		topic = Topic(text)
		topic.questions =[]
		#topic.tp_names =[]
		self.cur_eval.tp_names.append(str(tta))
		topic.started = self.counter_timer.elapsed()/1000.0
		
		#Explicação!!!!
		#self.robot_say("Agora vamos praticar gramática. Preste atenção na explicação.")
		#self.robot_say("Vamos estudar um pouco de gramática. Atenção para a explicação.")
		self.robot_say("Ok then. Let's play!")
		self.robot_say(text)


		# Load the table with questions and expected answers
		file_name = str(self.content_path + tta +".csv")
		
		
		try:	
			data=pd.read_csv(file_name)
		except:
			raise


		# Start the loop for the question number of the interaction
		for i in range(0,self.cur_interact.ques_per_topic):
			
			
			#reset question object
			quest = None
			quest = Question()
			quest.attempts = []
			quest.started = self.counter_timer.elapsed()/1000.0

			#self.robot_say("Preste atenção para pergunta.")
			# self.robot_say("Se você não entender, pode pedir pra eu repetir")
			#self.robot_say("Here comes the question. I can repeat if you want.")
			self.robot_say("Here comes the question.")

			core.info("Question number: " + str(i))
			core.war("PROFILE :" + str(self.user_profile))

			try:
				self.label_126.setText(str(self.user_profile))
				self.verticalSlider_3.setValue(self.user_profile)
				self.label_129.setText(str(self.preview_profile)) 
				self.label_128.setText(str(i+1))
			
			except:
				pass

			# Select the possibilities according to the user profile detected

			if self.user_profile > 5:
				self.user_profile = 5
			elif self.user_profile < 1:
				self.user_profile = 1

			dfp= data.loc[data['Difficulty'] == self.user_profile]
			possibilities = len(data.loc[data['Difficulty'] == self.user_profile])#['Question']

			#Reset the index of resulting possibilities (Original will overflow dataframe)
			dfp=dfp.reset_index(drop=True)

			#print"Index after", dfp.index
			#Randomly choose a question in possibilities range

			#if possibilities >=5


			rand = random.randint(0, possibilities-1)

			# attribute variables
			chosen_question = str(dfp.loc[rand]['Question'])
			expected_answer = str(dfp.loc[rand]['Expected Answer'])

			# Store the raffled question and exp answer
			quest.question=chosen_question			
			quest.exp_ans=expected_answer

		
			#Loop for attempt
			for j in range(0, self.cur_interact.att_per_ques):

				att = None
				att = Attempt()
				att.started = self.counter_timer.elapsed()/1000.0
				#print "Question:", chosen_question
				print "Exp: ", expected_answer

				self.run_exp_ans.setText( expected_answer)

				t1 = time.time()

			
				# Loop for repete question
				repete_flag = True
				while repete_flag:
					self.robot_say(chosen_question,ask=False)
					user_answer = self.user_input()

					if ("repetir" in user_answer):
						repete_flag = True

					elif ("repete" in user_answer):
						repete_flag = True
					elif ("repita" in user_answer):
						repete_flag = True

					else:
						repete_flag = False

				# Loop for understand right
				repete_flag = False #True
				while repete_flag: 
					
					# self.robot_say("Eu entendi que sua resposta foi:")
					self.robot_say("Eu entendi que sua resposta foi:")
					self.robot_say(user_answer)
					self.robot_say("Estou certo?")
					
					yes_not = self.user_input(record_flag=False)

					if check_positive_afirmation(yes_not):
						#self.robot_say("Certo")
						repete_flag = False
					else:
						self.robot_say("Vamos tentar de novo")
						self.robot_say("Pode repetir")
						user_answer = self.user_input(record_flag=False)



				#clear textedit
				self.run_user_answer.clear()

				#print "User ans: ", user_answer

				# Calculate answer similarity
				dist =  (self.diag_sys.adaptation_funct(self.embeddings, user_answer,expected_answer))
			
				print "DIST", dist, "Tresh", self.answer_threshold
				#print type(dist), type(self.answer_threshold)

				self.run_correctness.setText(str(dist))

				att.given_ans = user_answer
				#att.time2ans = time.time() - t1
				att.time2ans = time.time() - t1
				att.ans_dist = dist
				print "TIME TO ANS:", att.time2ans 

				self.run_under_ans.setText(user_answer)
				att.finished = self.counter_timer.elapsed()/1000.0


				if dist < self.answer_threshold:
					
					att.system_consideration = 1
					att.finished = self.counter_timer.elapsed()/1000.0
					#att.ans_dist = dist
					#quest.insert_attempt(att)	
					# self.robot_say("Parabéns. A resposta que eu esperava e a que você deu me parecem iguais!")
					self.robot_say("Congratulation. You got it!")
			 		self.robot_say("I was expecting:")
					self.robot_say(expected_answer)
					self.robot_say("And you said")
					self.robot_say(user_answer)


				else:
					
					att.system_consideration = 0
					att.finished = self.counter_timer.elapsed()/1000.0
					#att.ans_dist = dist
					#quest.insert_attempt(att)
					# self.robot_say("Eu notei que existe uma diferença entre a resposta que eu esperava e a que você deu.")
					# self.robot_say("Eu esperava a resposta:")
					# self.robot_say(expected_answer)
					# self.robot_say("E eu entendi que você respondeu:")
					# self.robot_say(user_answer)
					# self.robot_say("Não se preocupe. Eu também estou aprendendo.")
					

					self.robot_say("Sorry. I may be wrong but I expected something different.")
					self.robot_say("I was expecting something like:")
					self.robot_say(expected_answer)
					self.robot_say("And I understood")
					self.robot_say(user_answer)

					self.robot_say("Don't worry. I'm also learning and it takes time")


				# Setting Adaptive Parameters!

				#core.info("Finalizing emotion thread")
				#self.run_emotion_flag = False

				self.read_values.set(0, #self.n_deviations,
									0, #self.adapt_sys.getBadEmotions(),
									3 - self.diag_sys.coutingWords(user_answer),
									att.time2ans,
									dist)

				# Clear Variables
				self.n_deviation = 0
				self.adapt_sys.clear_emo_variables()




				if (self.adaptation_type=="Woz"):

					self.timer.stop()
					result = QMessageBox.question(self,
                                    "Increasing communication level profile",
                                    "Para incrementar o nível de dificuldade:\n\n Yes -> Aumenta\nIgnore - > Mantém\n No -> Diminui\n\n",
                                    QMessageBox.No | QMessageBox.Ignore | QMessageBox.Yes  )
					
					self.preview_profile = self.user_profile 
					self.timer.start()

					alpha = 0
					beta = 0
					gama = 0


					if result == QMessageBox.Yes:
						fvalue = 0
						print "Yes "

					elif result == QMessageBox.No:
						fvalue = 1
						print "No "
					
					elif result == QMessageBox.Ignore:
						fvalue = 0.5
						print "Ignore "

					fvalue = self.adapt_sys.activation_function(fvalue)


				elif (self.adaptation_type=="Fuzzy"):

					pprint(vars(self.read_values))

					values = self.states_fuzzy_control.compute_states(self.read_values)
					alpha = values[0]
					beta = values[1]
					gama = values[2]

					core.info("Alpha Fuzzy: "+ str(alpha))
					core.info("Beta Fuzzy: "+ str(beta))
					core.info("Alpha Fuzzy: "+ str(gama))
					fvalue = self.adaptive_fuzzy_control.compute_fvalue(values) / 10.0
					core.info("FVALUE -> " +str(fvalue))


				elif (self.adaptation_type=="Rules"):
					fvalue, alpha, beta, gama = self.adapt_sys.adp_function(j)
					fvalue = self.adapt_sys.activation_function(fvalue)
					
				



				self.adapt_sys.change_behavior(fvalue)

				self.preview_profile = self.user_profile 
				self.user_profile = self.adapt_sys.robot_communication_profile+1
				
				#print "FVALUE_________________>", fvalue


				att.alpha=alpha
				att.beta=beta	
				att.gama=gama
				att.fvalue=fvalue
				att.read_values = copy.deepcopy(self.read_values)
				att.profile=self.preview_profile

					
				quest.insert_attempt(att)	
				
				
				#END OF A ATTEMPT CYCLE


			
			# End of a question cycle
			# Insert current question in topic  
			quest.finished = self.counter_timer.elapsed()/1000.0
			topic.insert_question(quest)


		self.cur_eval.int_name=self.cur_interact.name
		# Insert current topic in eval
		topic.finished = self.counter_timer.elapsed()/1000.0
		self.cur_eval.insert_topic(topic)
		
		print "\n\n"




	def run_final_dialog(self):

		self.robot_say("Por hoje é isso")
		if (self.robot is not None):
			self.robot.behavior.runBehavior('animations/Stand/Gestures/Hey_1')
		self.robot_say("Foi um prazer brincar com você, " + self.cur_user.first_name, block=False)
		self.robot_say("Até mais")

		#self.robot.behavior.runBehavior("hi/hi")
		
		#print "PAssou"
		if (self.robot is not None):
			self.robot.motors.rest()

		# try:
		# except OSError as err:
		# 	print("OS error: {0}".format(err))
		# except ValueError:
		# 	print("Could not convert data to an integer.")
		# except:
		# 	print("Unexpected error:", sys.exc_info()[0])
		# 	core.er("DEU MERDA NO TCHAU")




	# def my_load(self):
				
	# 	#Loading selected model
	# 	model = emotion.classifier_options[self.emoModel_comboBox.currentIndex()]
	# 	self.emotion_classifier = emotion.Classifier(model)
	# 	self.face_cascade = cv2.CascadeClassifier('Modules/haarcascade_frontalface_alt.xml')
	# 	self.students_database.generate_encodings()
	
	# class TLoad(QThread):
				
	# 	def run(self):
	# 		self.my_load()

	# #class MyDiag(QDialog):
	# class MyDiag(QMessageBox):

	# 	def __init__(self, parent=None):
	# 		super(MyDiag, self).__init__(parent)
	# 		# ...

	# 		self.setWindowTitle("Waiting for models to load")
	# 		self.setText("Go take a coffee!")
			
	# 		self.setIcon(QMessageBox.Information)
			
	# 		self.thread = TLoad()
	# 		self.thread.finished.connect(self.close)
	# 		self.thread.start()	
	# 		#flag_list[0]=False




	def run_load_models(self):
		#self.students_database.generate_encodings()

		thread = False

		model = emotion.classifier_options[self.emoModel_comboBox.currentIndex()]
		if thread:
			msg=MyDiag(self)
			msg.exec_()

		else:
			msg=MyDiag(self)
			msg.exec_()

			self.emotion_classifier = emotion.Classifier(model)
			self.face_cascade = cv2.CascadeClassifier('Modules/haarcascade_frontalface_alt.xml')
			self.students_database.generate_encodings()
		
			QMessageBox.information(self, "Models Loaded", "Ok to go!")

		#self.faces = self.face_cascade.detectMultiScale(image_gray, 1.3, self.minNei_spinBox.value() )#minNeighbors=5)
		self.run_display_image_radioButton.setChecked(True)
		self.run_facerecog_pushButton.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(True)
		self.run_load_pushButton.setEnabled(False)
		self.run_reset_button.setEnabled(True)
		self.log("Models loaded. Emotion classification model: "+model)


	def run_facerecog(self):
		self.recog_flag=True
		self.run_emotion_pushButton.setEnabled(False)
		#self.interact_recognize_person()
		self.run_reset_button.setEnabled(True)
		self.run_facerecog_pushButton.setEnabled(False)


	def run_att_emo(self):
		self.run_emotion_flag=True
		self.run_facerecog_pushButton.setEnabled(False)
		# static measuring time, dynamic measuring time, time on atention, time for emotion classifier
		self.n_deviations = self.time_disattention = 0
		self.static_time = self.dynamic_time = self.time_attention = self.time_emotion = time.time()
		self.run_reset_button.setEnabled(True)
		self.run_emotion_pushButton.setEnabled(False)


	def run_reset_demo_action(self):
		self.run_emotion_flag=False
		self.recog_flag=False
		self.run_emotion_pushButton.setEnabled(True)
		self.run_facerecog_pushButton.setEnabled(True)
		self.run_reset_button.setEnabled(False)




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

	def setNextStepFalse(self):
		self.next_step = False
		
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

		if self.display_flag:
			
			if self.robot is not None:
				self.image = self.vis_sys.get_img(0)

				# rself.image = cv2.flip(self.image,1)
			else:
				ret, self.image=self.capture.read()

		#cv2.imshow("testwindow",self.image )
		#cv2.waitKey()

		# RECOGNIZING USER
		if (self.recog_flag):
			self.image, self.recog_user_id = self.students_database.face_recognition(self.image)
			#self.cur_user= self.students_database.get_user(self.recog_user_id)
			
			#print "AQUIIIIIIIII", self.recog_user_id
			if self.recog_user_id is not None:
				#print  self.recog_user_id
				self.run_recognized_user_label.setText(str(self.students_database.get_user(self.recog_user_id).first_name))
			else:
				self.log("USER NOT DETECTED")


		# CLASSIFYING EMOTION
		if (self.run_emotion_flag):
			self.image = self.run_attention_emotion_thread(self.image)

		# RECORDING VIDEO (NEVER USED)
		if(self.run_record):
			frame = self.image #cv2.flip(self.image,-1)
			self.out.write(frame)

		if self.display_flag:
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
						self.classified_emotion = self.emotion_classifier.inference(face_to_classify)
						# writes emotion on the image, to be shown on screen
						#cv2.putText(image, classified_emotion, (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)			
						# store image on a folder, for future analysis
						#cv2.imwrite("emotion_imgs/{}.png".format(dynamic_time), face)
						#c.write("{} {}\n".format(dynamic_time, classified_emotion))
						# reset time
						self.time_emotion = self.time_diff
						#core.info("Emotion classified: {}".format(classified_emotion))
						self.run_emotion_label.setText(self.classified_emotion)

						self.adapt_sys.emotions[self.classified_emotion] += 1
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



	def run_new_eval_group_action(self):

		while True:
			cont_name,  ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter new evaluation group:')
			cont_name = str(cont_name.toUtf8())
			if ok:
				# Check if the name already exists
				if (cont_name in self.evaluation_db.group_list):
					QMessageBox.critical(self, "Error!", "Group already exists!\nChoose another name!", QMessageBox.Ok )
				else:		
					self.evaluation_db.add_evaluation_group(cont_name)
					self.run_group_eval_comboBox.addItem(cont_name)
					self.group_eval_comboBox.addItem(cont_name)


					break
			else:
				break


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


	def log(self, text, msg_type='i'):
		
		time = QTime.currentTime()
		text = time.toString("hh:mm:ss") +"  -->  "+ text
		self.log_text.setText( text ) 
		
		if msg_type == 'i':
			core.info(text)
		elif msg_type == 'w':
			core.war(text)
		elif msg_type == 'e':
			core.er(text)
		else:
			print text

	def robot_say(self, text, ask =False, block=True):

		self.robot_speech.setText(str(  text ))
		core.nao_say(text)

		if self.robot is not None:
		
			self.user_ans_flag = True

			t1 = threading.Thread(name='robot_say_action', target=self.robot_say_action, args=(text, ask, block))
			t1.start()

			while self.user_ans_flag:

				QCoreApplication.processEvents()

			#t2 = threading.Thread(name='my_service', target=my_service)
			#self.robot_say_action(text, False, True)

		else:

			self.run_next_step_button.setEnabled(True)
			while self.next_step:
					
				QCoreApplication.processEvents()
				
			self.next_step = True
			#self.run_next_step_button.setEnabled(False)
			self.log("PRESS NEXT STEP BUTTON")



	def robot_say_action(self, text, ask, block ):

		#self.robot_say_block()
		self.diag_sys.say(str2say=text,ask=ask, block=block)
		self.user_ans_flag = False



	#def robot_say_block(self,):





	def user_input(self, record_flag= True):
		"""
		Wait user to answer in the correct 
		field and press corresponding button
		"""
		#core.info("Inside User input ")

		if self.aud_rec_flag and record_flag:
			th_exec = AudioRecording.ThreadAudioRecording(self.aud_rec,'listen')
			th_stop = AudioRecording.ThreadAudioRecording(self.aud_rec,'stop')
			th_exec.start()

		#print "Input Option", core.input_option

		# IF MIC
		if core.input_option == 0 :

			ans = QMessageBox.question(self, "Woz Answer!", "Is the user answer right?", 
									QMessageBox.Cancel | QMessageBox.Ok )
			
			if ans == QMessageBox.Ok:

				ret = True
				
			else:
				ret = False


		elif core.input_option > 0 :


			#if self.robot is not None:
		
			#self.user_ans_flag = True

			#t1 = threading.Thread(name='wait', target=self.get_ans_mic)
			#t1.start()

			ret = self.diag_sys.getFromMic_Pt()#.decode('utf-8')

			#self.user_ans_flag = False
			self.run_under_ans.setText(ret)
			#t1.join()


	
		
		# IF text
		else :
			self.user_ans_flag = False

			self.run_user_answer.setEnabled(True)
			self.run_user_answer.setFocus()
			self.timer.stop()
			while not self.user_ans_flag:
					
				#self.label_132.setText(str(time.time("hh:mm:ss")))
				QCoreApplication.processEvents()
				#time.sleep(0.05)

			self.user_ans_flag = False
			self.timer.start()
			ret = str(self.run_user_answer.text().toUtf8())
			self.run_user_answer.setText("")
			self.run_user_answer.setEnabled(False)



		if self.aud_rec_flag and record_flag:
			th_stop.start()
			th_exec.join()
			th_stop.join()


		return ret 


	def get_ans_mic(self):

		while self.user_ans_flag:
			QCoreApplication.processEvents()



	def correct_evals(self):
		
		for item in range(len(self.evaluation_db.evaluations_list)):
			
			if len(self.evaluation_db.evaluations_list[item].topics) >2:
				#print 

				#while len(self.evaluation_db.evaluations_list[item].topics) >2 :
				print "Deleting"
				del self.evaluation_db.evaluations_list[item].topics[2:len(self.evaluation_db.evaluations_list[item].topics)]
				del self.evaluation_db.evaluations_list[item].tp_names[2:len(self.evaluation_db.evaluations_list[item].tp_names)]

				pprint(vars(self.evaluation_db.evaluations_list[item]))
				self.evaluation_db.insert_eval(self.evaluation_db.evaluations_list[item])



	def evals_to_csv(self, group, table_name, tp_range =None):

		
		df = pd.DataFrame(columns=(	"Id",
									"Name", 
									"Duration", 
									"Topic", 
									"Interaction_name", 
									"Question_number", 
									"Dificult",	
									"Question",
									"Exp_ans", 
									"Under_ans", 
									"Sup_ans",
									"Sys_ans", 
									"Sys_was",
									"Time_to_answer"))
		
		#print df
		t=0
		flag_validation = False
		for item in range(len(self.evaluation_db.evaluations_list)):
			
			#pprint((self.evaluation_db.evaluations_list[item].date)) 
			#if self.evaluation_db.evaluations_list[item].date == QDate(2019,2,18) or self.evaluation_db.evaluations_list[item].date == QDate(2019,2,19):
			if self.evaluation_db.evaluations_list[item].group == group:
				
				aux = self.evaluation_db.evaluations_list[item]
				name = aux.user_name
				duration = aux.start_time.secsTo(aux.end_time)

				try:
					if tp_range is None:
						tpsranges = range(len(aux.topics))
					else:
						tpsranges = range(tp_range[0],tp_range[1]+1)	 
					
					#print "RANGE", tpsranges
					# if len(aux.topics)==0:
					# 	continue 

					#for tp in range(len(aux.topics)):
					for tp in tpsranges:
						try:
							topic_name = aux.tp_names[tp]
						except:
							continue

						#print tp 
						#print self.evaluation_db.evaluations_list[item].id


						for q in range(len(aux.topics[tp].questions)):

							question = aux.topics[tp].questions[q]
							att = question.attempts[0]

							#Check for incomplete validation
							if att.supervisor_consideration<0:
								flag_validation = True						
							
							df.loc[-1]= [	aux.id,
											name, 
											duration, 
											topic_name,
											aux.int_name, 
											q+1, 
											att.profile, 
											question.question, 
											question.exp_ans, 
											att.given_ans,
											att.supervisor_consideration,
											att.system_consideration, 
											att.system_was, 
											att.time2ans]

							
							
							# 
							df.index = df.index + 1  # shifting index
							#df = df.sort_index()  # sorting by index
						#pass
				except:
					self.log("Problem with eval id: " + str(aux.id))
				#pass

		if flag_validation:
			QMessageBox.information(self, "Validation missing!", "Some validation in this group is missing", QMessageBox.Ok )

		df.to_csv(table_name, index=False)

		

	def video_check_change(self, b):
		
		if b.isChecked() == True:
			self.display_flag = True
		else:
			self.display_flag = False



	def gui_wait(self, flag_list):

	

		while flag_list[0]:
			QCoreApplication.processEvents()

		flag_list[0]= True


	def save_state(self):
		print "--- Saving ---"
		started = time.time()
		f = open("win", 'wb')
		cPickle.dump(self.__dict__, f, 2)
		f.close()
		print "--- Save done in {} seconds\n".format(time.time()-started)

	def load_state(self):
		f = open("win", 'rb')
		tmp_dict = cPickle.load(f)
		f.close()
		self.__dict__.update(tmp_dict) 




	def update_eval_index(self):

		path = "Evaluations"

		os.rename("Evaluations/index_table.csv", "Evaluations/BK_index_table.csv" )

		f = open(path+"/index_table.csv","w+")

		f.write("Id,Date,Group,Student Name\n")

		file_list = os.listdir(path)

		file_list.sort()

		for item in file_list:

			if item.isdigit() and len(item)==5:
				#print "YES"
				try:
					aux = self.evaluation_db.load_eval(os.path.join(path,item, item+".eval"))
				except:
					print "Error trying to opening evaluation:", item 
					continue

				if aux.group != "Woz-B":
				#if aux.group != "grupoA-WozgrupoB-Woz":
					print aux.group
					continue
	
				# if aux.duration < 60000:
				# 	continue
				# #print "MENOOR"
				#self.evaluation_db.delete_eval(self.cur_eval)

				# if aux.group == "grupoA-Woz":
				# 	aux.group = "Woz-A"
				# if aux.group == "grupoA-WozgrupoB-Woz":
				# 	aux.group = "Woz-B"

				try:
					name = str(aux.user_name.toUtf8())
				except:
					try:
						name = aux.user_name.encode('utf-8')
					except:
						name = aux.user_name	

				try:

					if aux.group not in self.evaluation_db.group_list:
						self.evaluation_db.add_evaluation_group(aux.group)

				except:
					print "Evaluation {} has no group".format(item)
					self.evaluation_db.delete_eval(aux)
					continue


				mystr = str(aux.id).encode('utf-8') +","+ str(aux.date.toString("dd.MM.yyyy").toUtf8()) +","+ str(aux.group) +","+ name			
				#mystr = u' '.join((str(aux.id),",",str(aux.date.toString("dd.MM.yyyy")), ",", str(aux.user_name))).encode('utf-8').strip()			
				#print mystr
				f.write(mystr)
				f.write('\n')




			else:
				print "Not a evaluation:",item

		f.close()

		self.evaluation_db.index_table = pd.read_csv(self.evaluation_db.index_path)
		self.evaluation_db.group_list = pd.read_csv(self.evaluation_db.path + "group_list.csv")
		self.evaluation_db.load_evaluations_list()
		dataframe_to_table(self.evaluation_db.index_table, self.eval_index_table)
		self.eval_index_table.resizeColumnsToContents()

		self.log("Evaluation Index updated!")


	@pyqtSlot(str)
	def line_edit_text_changed(self, line, button):
		if line.text:  # Check to see if text is filled in
			button.setEnabled(True)
		else:		# self.cur_eval.topics[self.tp_id].questions[self.qt_id].attempts[self.att_id].system_consideration = self.eval_ans_sys_comboBox.currentIndex()
			button.setEnabled(False)

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = MainApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main() # run the main function
