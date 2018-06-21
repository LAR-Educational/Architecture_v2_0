from PyQt4 import QtGui, QtCore # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
import csv
import os

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







class ExampleApp(QtGui.QMainWindow, activities_Manager.Ui_MainWindow):
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
		
		
		self.insertQuestion_Button_2.clicked.connect(self.content_InsertQuestion)
		
		
		
		self.act = False
		self.qRow = 0
		self.qCol = 0


		self.model = QtGui.QStandardItemModel(self)
		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)

		self.tableView.setModel(self.model)
		self.tableView.horizontalHeader().setStretchLastSection(True)
		self.layoutVertical = QtGui.QVBoxLayout(self)
		self.layoutVertical.addWidget(self.tableView)
		self.layoutVertical.addWidget(self.reportLoadButton)
		self.layoutVertical.addWidget(self.writeReportButton)
		
		self.subs_list = []








	def load_file(self):
		
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', './Activities/NOVA')
		
		self.act=ct.load_Activity(filename)
		
		#self.name_lineEdit.setText(self.act.name)
		#self.desc_lineEdit.setText(self.act.description)		
		#self.path_lineEdit.setText(self.act.path)
		#self._lineEdit.setText(self.act.desc)
		self.editButton.setEnabled(True)
		self.modules_tabWidget.setEnabled(True)
		self.sub_list = load_subjects(os.path.join(self.act.path,"Content","subjects"))
		
		print self.sub_list
		self.comboBox_6.addItems(self.sub_list[1])

	def close(self):
		exit()
		#self.destroy()

	
	
	
	def insertQuestion(self):
		
		self.sysQuestionsTable.insertRow(self.qRow)
		self.sysQuestionsTable.setCurrentCell(self.qRow,0)
		#self.questions_tableWidget.setItem(0,0, QtGui.QTableWidgetItem("TESTE"))
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
				self.sysQuestionsTable.setItem(self.qRow, 0, QtGui.QTableWidgetItem(item[0]))
				self.sysQuestionsTable.setItem(self.qRow, 1, QtGui.QTableWidgetItem(item[1]))
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
				    QtGui.QStandardItem(field)
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
				        QtCore.Qt.DisplayRole
				    )
				    for columnNumber in range(self.model.columnCount())
				]
				writer.writerow(fields)
	
	
	def content_InsertQuestion(self):
		
		self.questions_tableWidget_2.insertRow(self.questions_tableWidget_2.rowCount())
		#self.questions_tableWidget_2.setCurrentCell(self.qRow,0)
		#self.questions_tableWidget.setItem(0,0, QtGui.QTableWidgetItem("TESTE"))
		#self.qRow+=1
	
	

	
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





def main():
    app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
	main() # run the main function
