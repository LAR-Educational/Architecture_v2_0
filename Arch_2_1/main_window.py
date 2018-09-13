#from PyQt4 import QtGui, QtCore # Import the PyQt4 module we'll need

from PyQt4.QtCore import *
from PyQt4.QtGui import *


#import PyQt4
import sys # We need sys so that we can pass argv to QApplication
import csv
import os
import cv2
import numpy as np
import pandas as pd

#from PyQt4.QtGui import *
 
import activities_Manager # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer


from Modules import vars as core
#from Modules import dialog #as diag
#from Modules import motion as mt
from Modules import vision #as vs
from Modules.Vision import predict
from Modules.Vision import data_process #as dp
from Modules import content as ct


class SessionInfo:
	def __init__(self,itime,ftime,):
		self.itime=itime
		self.ftime=ftime


class PandasModel(QAbstractTableModel):
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QVariant()



class ExampleApp(QMainWindow, activities_Manager.Ui_MainWindow):
	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the design.py file
		super(self.__class__, self).__init__()

		self.setupUi(self)  # This is defined in design.py file automatically

		self.loadactButton.clicked.connect(self.load_file)
		self.exitButton.clicked.connect(self.close)
		self.insertQuestion_Button.clicked.connect(self.insertQuestion)
		self.loadQuestions_Button.clicked.connect(self.loadQuestions_fromFile)
		self.saveQuestions_Button.clicked.connect(self.saveQuestions_fromFile)
		self.reportLoadButton.clicked.connect(self.loadReportsCsv)
		self.writeReportButton.clicked.connect(self.writeReportCsv)
		
		

		#--- Content panel
		self.content_path=None
		self.contenct_newSubj_button.clicked.connect(self.content_NewSubject)
		self.content_insert_question_button.clicked.connect(self.content_InsertQuestion)
		self.content_delete_question_button.clicked.connect(self.content_DeleteQuestion)
		self.content_saveSub_button.clicked.connect(self.content_save)
		self.content_subject_comboBox.currentIndexChanged.connect(self.content_update_tab)
		self.contenct_clear_questions_button.clicked.connect(self.content_clear_table)
		

		#--- Plan and Run
		self.pushButton_run_activity.clicked.connect(self.start_display_image)
		self.pushButton_start_robot_view.clicked.connect(self.resume_display_image)
		self.pushButton_stop_robot_view.clicked.connect(self.stop_display_image)
		
		self.image=None
		
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
		
		self.subs_list = []








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
					break
			else:
				break		
	
		#self.content_saveSub_button.setEnabled(True)
		self.sub_list.loc[len(self.sub_list.index)] = [cont_name,""]
		self.content_subject_comboBox.setCurrentIndex(self.content_subject_comboBox.count()-1)



	def content_save(self):
		file_name = self.act.path +  "/Content" +"/"+self.content_subject_comboBox.currentText()+".csv"

		#table_to_file(self.content_questions_table, file_name)
		sub_name = str(self.content_subject_comboBox.currentText())
		sub_conc = str(self.content_concept.toPlainText())
		self.sub_list.loc[self.content_subject_comboBox.currentIndex()] = [sub_name,sub_conc]
		
		data = table_to_dataframe(self.content_questions_table)
		data.to_csv(file_name, index=False)

		#self.log_text.setText("Subject saved at " + QDateTime.currentDateTime())




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
			

	def content_load_subjects(self):
		self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		#self.sub_list = pd.read_csv(os.path.join(self.act.path,"Content","subjects.csv"))
		self.content_subject_comboBox.addItems(self.sub_list['subjects'].tolist())
		self.content_update_tab()

	def content_update_tab(self):
		#text= self.sub_list['concepts'][self.sub_list['subjects'][self.sub_list['subjects']==str(self.content_subject_comboBox.currentText())].index[0]]
		text= self.sub_list['concepts'][self.content_subject_comboBox.currentIndex()]
		
		self.content_concept.setText(text)
		file_name = str(self.content_path + self.content_subject_comboBox.currentText()+".csv")
		
		if os.path.isfile(file_name):
			data=pd.read_csv(file_name)
			#print "trying data", data

			df_to_table(data,self.content_questions_table)

			self.log_text.setText("Subject loaded: " + self.content_subject_comboBox.currentText())
			

		else:	
			self.log_text.setText("WARNING TABLE <<"+file_name +">>  FILE DO NOT EXIST")
			labels = []
			for i in range(0,3):
				labels.append(str(self.content_questions_table.horizontalHeaderItem(i).text()))
			
			data = 	pd.DataFrame(columns=labels, index=range(0))

			print data

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
		
		
		print "RETRIEVED: "
		print  data

		df_to_table(data,self.content_questions_table)



#-------------------------------------------------- RUN ----------------------------------------

	def start_display_image(self):
		self.capture = cv2.VideoCapture(0)
		self.pushButton_start_robot_view.setEnabled(True)
		self.pushButton_stop_robot_view.setEnabled(True)

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
		
		
		
	def resume_display_image(self):
		self.pushButton_start_robot_view.setEnabled(False)
		self.pushButton_stop_robot_view.setEnabled(True)

		self.timer.start(5)

	def update_frame(self):
		ret, self.image=self.capture.read()
		self.image = cv2.flip(self.image,1)
		#cv2.imshow("testwindow",self.image )
		#cv2.waitKey()

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





### -------------------------- GLOBALS -----------------------


def clearTable(table):	
	
	while (table.rowCount() > 0):
		table.removeRow(0);



def load_subjects(filename):

	subject_matrix = []
	with open(filename+'.csv', "rb") as fileInput:
		#print "OLARRR"
		for row in csv.reader(fileInput):    
			#print row					
			subject_matrix.append(row) 

	return subject_matrix 



def load_csv_as_matrix(filename):
	
	subject_matrix = False
	
	with open(filename+'.csv', "rb") as fileInput:
		for row in csv.reader(fileInput):    
			for item in row:
				aux.append(item)	
			subject_matrix.append(aux) 
			
	return subject_matrix 


def table_to_file(table_name, file_name):
	
		
		with open(file_name, "wb") as fileOutput:
			
			writer = csv.writer(fileOutput)
			for row in range(table_name.rowCount()):
				row_data = []
				for column in range(table_name.columnCount()):
					item = table_name.item(row, column)
					if item is not None:
						row_data.append(item.text())
					else:
						row_data.append('')
				writer.writerow(row_data)



def table_to_dataframe(table):
	row_numb = table.rowCount() 
	col_numb = table.columnCount()

	#get header labels
	labels = []
	for i in range(0,col_numb):
		labels.append(str(table.horizontalHeaderItem(i).text()))
	
	data = 	pd.DataFrame(columns=labels, index=range(row_numb))
	
	for i in range(row_numb):
		for j in range(col_numb):
			#print i,j
			#print  table.item(i,j)
			if table.item(i,j) == None:
				item = 'nan'
			else:
				item = table.item(i,j).text()
			data.ix[i,j] = item
	
	return data	


def df_to_table(df,table):
	
	table.setColumnCount(len(df.columns))
	table.setRowCount(len(df.index))
	#print df.columns

	table.setHorizontalHeaderLabels(df.columns)
	for i in range(len(df.index)):
		for j in range(len(df.columns)):
			item = str(df.iat[i, j])
			if item == 'nan':
				item = ''
			
			table.setItem(i, j, QTableWidgetItem(item))

	#table.resizeColumnsToContents()
	#table.resizeRowsToContents()



def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main() # run the main function
