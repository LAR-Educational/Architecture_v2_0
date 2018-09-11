from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys # We need sys so that we can pass argv to QApplication
import csv
import os
import cv2
import numpy as np
import pandas as pd







### -------------------------- GLOBALS -----------------------


def clearTable(table):	
	
	while (table.rowCount() > 0):
		table.removeRow(0);



def insert_item_table(table):
	#self.knowledge_general_table.insertRow(self.knowledge_general_table.rowCount())
	table.insertRow(table.rowCount())
	
def delete_item_table(table):
	#index = table.currentRow()
	#print index
	table.removeRow(table.currentRow())


def save_table(window, table, dataframe, filename):

    ret = QMessageBox.question(window, "Saving table!", "Are you sure you want to overwrite this file table?"+
                                    "\nOld version will be lost!", QMessageBox.Cancel | QMessageBox.Ok )
    if ret == QMessageBox.Ok:
       dataframe = table_to_dataframe(table)
       dataframe.to_csv(filename, index=False)


def load_table(window, table, dataframe, filename):
	

    if os.path.exists(filename):

        ret = QMessageBox.question(window, "Loading table!", "Are you sure you want to overwrite this screen table?"+
                                        "\nCurrent content will be lost!", QMessageBox.Cancel | QMessageBox.Ok )
        if ret == QMessageBox.Ok:
            dataframe = pd.read_csv(filename)
            dataframe_to_table(dataframe,table)

    else:

        QMessageBox.critical(window, "Error!", "File to load does not exist!", QMessageBox.Ok )

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


def dataframe_to_table(df,table):
	
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


