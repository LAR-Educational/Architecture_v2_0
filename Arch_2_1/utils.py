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
    #table.resizeColumnsToContents()
    table.resizeRowsToContents()

	
def delete_item_table(table):
	#index = table.currentRow()
	#print index
    table.removeRow(table.currentRow())


def save_table(window, table, dataframe, filename):

    ret = QMessageBox.question(window, "Saving table!", "Are you sure you want to overwrite this file table?"+
                                    "\nOld version will be lost!", QMessageBox.Cancel | QMessageBox.Ok )
    if ret == QMessageBox.Ok:
       dataframe = table_to_dataframe(table)
       dataframe.to_csv(filename, index=False, sep="|")#, encoding='utf-8')


def load_table(window, table, dataframe, filename):
	

    if os.path.exists(filename):

        ret = QMessageBox.question(window, "Loading table!", "Are you sure you want to overwrite this screen table?"+
                                        "\nCurrent content will be lost!", QMessageBox.Cancel | QMessageBox.Ok )
        if ret == QMessageBox.Ok:
            dataframe = pd.read_csv(filename, sep="|", encoding='utf-8')
            #print "DATAFRAME"
            #print dataframe
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
				item = str(table.item(i,j).text())
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
			#print df.iat[i, j]
			#print i, j
			#print item
			#item = u''.join((df.iat[i, j])).encode('utf-8').strip()
			
			if item == 'nan':
				item = ''

			table.setItem(i, j, QTableWidgetItem(item))

    #table.wordWrap(True)
    #table.resizeColumnsToContents()
    table.resizeRowsToContents()



def qImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(4)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
    return arr






def matcv_to_qimg(img):

	qformat = QImage.Format_Indexed8
	if len(img.shape)==3:
			if img.shape[2]==4:
				qformat = QImage.Format_RGBA8888
			else :
				qformat = QImage.Format_RGB888
	
	outImage= QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
	outImage = outImage.rgbSwapped()

	return outImage


#def qimg_to_cvmat()












#---------------------------------- USELESS- -------------------------------



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


