#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys # We need sys so that we can pass argv to QApplication
import csv
import os
import cv2
import numpy as np
import pandas as pd
import math
import duckduckgo as ddg

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np




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
				#item = 'nan'
				item = ''
			else:
				item = table.item(i,j).text().toUtf8()
				#print "Before", item, type(item )

				#item = QString.fromUtf8(item)
				#print "After",  type(item )

			data.ix[i,j] = item
	
	return data	


def dataframe_to_table(df,table):

    table.setColumnCount(len(df.columns))
    table.setRowCount(len(df.index))
    #print df.columns

    table.setHorizontalHeaderLabels(df.columns)
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
			
			#print "Item and Type  ", df.iat[i, j], type(df.iat[i, j])

			item = df.iat[i, j]

			if item == 'nan':
				item = ''
			elif isinstance(item, int):
				item = QString.number(item)
			elif isinstance(item, float):
				item = QString.number(item)
				if item == 'nan':
					item = ''
			else:
				item = QString(item)
				
			#print "AFTER", type(item)
			#print "AFTER", item, type(item)

			item = QString.fromUtf8(item)

			table.setItem(i, j, QTableWidgetItem(item))

    #table.wordWrap(True)
    #table.resizeColumnsToContents()
    table.resizeRowsToContents()



def qImageToMat(incomingImage):
	'''  Converts a QImage into an opencv MAT format  '''


	try:

		#print "try dentro"
		incomingImage = incomingImage.convertToFormat(4)

		width = incomingImage.width()
		height = incomingImage.height()

		ptr = incomingImage.bits()
		ptr.setsize(incomingImage.byteCount())
		arr = np.array(ptr).reshape(height, width, 4)  #  Copies the data
		return arr

	except Exception as ex:
		print("Unexpected error:", ex)
		#raise






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


def cvmat_to_qimg(image):

	# image = QImage(image, image.shape[1],\
    #                         image.shape[0], image.shape[1] * 3, QImage.Format_RGB888)
	# #pix = QtGui.QPixmap(image)
	# return QPixmap(image)

	height, width, channel = image.shape
	bytesPerLine = 3 * width
	return  QPixmap((QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)).rgbSwapped())


positive_list = ['sim','certo','certa', 'ok', 'exato', 'correto', 'correta', 'acertou']

def check_positive_afirmation(string, list = positive_list):

	for i in list:
		if i in string:
			return True

	return False	





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


personal_translate={
		'sport':"Qual o seu esporte preferido?",
		'music':"Qual a sua música preferida?",
		'dance':"Qual a sua dança preferida?",
		'team':"Qual o seu time de futebol preferido?",
		'toy':"Qual o seu brinquedo preferido?",
		'hobby':"O que você gosta de fazer no tempo livre?",
		'game':"Qual a sua brincadeira preferida?",
		'food':"Qual a sua comida preferida?",
}

sports_dict = {
	'natação':'natação pura',
	'ginastica': 'ginastica artistica'
}

teams_dict = {
	'são paulo':'são paulo futebol clube',
	'santos': 'santos futebol clube',
	'flamengo': 'clube de regatas do flamengo',
	'fluminense':'fluminense futebol clube',
	'botafogo': 'botafogo de futebol e regatas',
	'cruzeiro': 'cruzeiro esporte clube',
	'são carlos': 'são carlos futebol clube',
}

hobbies_dict = {
	'dormir': 'pt.wikipedia:sono',
	'comer': 'pt.wikipedia:comer'
}

dance_dict = {
	'funk': 'funk carioca'
}

#termos com problema (futebol, handebol, esconde-esconde, balé, ).
#axé retorna em ingles


def search_engine(query):

	print "Processing query !"

	return ddg.query(query, kad='pt_BR').abstract.text




def generate_graph():


	df = pd.read_csv("final_evals.csv")


	#rights = df[ (df['Question_number']==1) & (df['System_was']==1) ]


	sys_good = []
	sys_bad =[]
	miss = []
	sup_good=[]
	sup_bad=[]

	for i in range(1,4):


		yg = df[ (df['Question_number']==i) & (df['System_was']==1) & (df['Topic']=='Encontro Vocalico') ] 
		yb = df[ (df['Question_number']==i) & (df['System_was']==0) & (df['Topic']=='Encontro Vocalico') ] 
		pg = df[ (df['Question_number']==i) & (df['Supervisor']==1) & (df['System_was']>=0) & (df['Topic']=='Encontro Vocalico') ] 
		pb = df[ (df['Question_number']==i) & (df['Supervisor']==0) & (df['System_was']>=0) & (df['Topic']=='Encontro Vocalico') ] 
		sys_good.append( len(yg.index) )
		sys_bad.append( len(yb.index) )
		sup_good.append( len(pg.index) )
		sup_bad.append( len(pb.index) )

		m  = df[ (df['Question_number']==i) & (df['System_was']<0)  & (df['Topic']=='Encontro Vocalico') ] 
		miss.append( len(m.index) )
	
	for i in range(1,4):


		yg = df[ (df['Question_number']==i) & (df['System_was']==1) & (df['Topic']=='Digrafo') ] 
		yb = df[ (df['Question_number']==i) & (df['System_was']==0) & (df['Topic']=='Digrafo') ] 
		pg = df[ (df['Question_number']==i) & (df['Supervisor']==1) & (df['System_was']>=0) & (df['Topic']=='Digrafo') ] 
		pb =df[ (df['Question_number']==i) & (df['Supervisor']==0) & (df['System_was']>=0) & (df['Topic']=='Digrafo') ] 

		sys_good.append( len(yg.index) )
		sys_bad.append( len(yb.index) )
		sup_good.append( len(pg.index) )
		sup_bad.append( len(pb.index) )

		m  = df[ (df['Question_number']==i) & (df['System_was']<0)  & (df['Topic']=='Digrafo') ] 
		miss.append( len(m.index) )
	

	#print sys_good
	#print sys_bad
	#print sup_good
	#print sup_bad


	x = [1, 2, 3, 4, 5, 6]
	my_xticks = ["V.E. 1", "V.E. 2", "V.E. T3", "D. 1", "D. 5", "D. 6"]
	

	#'''
	plt.figure(1)


	#plt.subplot(121)
	plt.xticks(x, my_xticks)
	y = sys_good
	plt.plot(x, y, 'o--', color='g',  markersize=12, label="System's correct classifications")
	for a,b in zip(x, y): 
		plt.text(a-0.1, b-2.3, str(b))

	y=sys_bad
	plt.plot(x, y,  's--', color='r', markersize=12, label="System's wrong classifications")
	for a,b in zip(x, y): 
		plt.text(a-0.05, b+1.5, str(b))

	y=miss
	plt.plot(x, y,  'x--', color='y', markersize=12, label="Listening problem")
	for a,b in zip(x, y): 
		plt.text(a+0.18, b-0.2, str(b))


	plt.legend(loc='upper left', numpoints = 1,#('System right ','System Wrong ','Students right answers','Students wrong answers'),
           #shadow=True,
		   #loc=(0.01, 0.8),
		   #handlelength=1.5, 
		   fontsize=12)

	plt.xlim(0,7)
	plt.ylim(-1,33)

	plt.title("System Classifications", fontsize=32)

	plt.xlabel("Topic_Question Number", fontsize=16)
	plt.ylabel("Number of occurrences", fontsize=20)
	plt.grid(True, linewidth=.15)
	plt.show()
	#'''

	plt.figure(2)

	#return
	
	#plt.subplot(122)
	plt.xticks(x, my_xticks)

	y=sup_good
	plt.plot(x, y, 'o--', color='b', markersize=12, label="Classified as right")
	for a,b in zip(x, y): 
		plt.text(a-0.05, b+1.0, str(b))

	
	y=sup_bad
	plt.plot(x, y, 's--', color='r', markersize=12, label="Classified as wrong")
	for a,b in zip(x, y): 
		plt.text(a-0.081, b-1.5, str(b))
	
	y=miss
	plt.plot(x, y,  'x--', color='y', markersize=12, label="Listening problem")
	for a,b in zip(x, y): 
		plt.text(a+0.18, b-0.2, str(b))

	
	plt.legend(loc='upper right', numpoints = 1,#('System right ','System Wrong ','Students right answers','Students wrong answers'),
		#shadow=True,
		#loc=(0.01, 0.8),
		#handlelength=1.5, 
		fontsize=12)


	plt.xlim(0,7)
	plt.ylim(-1,22)

	plt.title("Supervisor Classifications", fontsize=32)

	plt.xlabel("Topic_Question Number", fontsize=16)
	plt.ylabel("Number of occurrences", fontsize=20)
	plt.grid(True, linewidth=.15)
	plt.show()
	




def generate_graph_frequency():


	df = pd.read_csv("final_evals.csv")


	#rights = df[ (df['Question_number']==1) & (df['System_was']==1) ]


	mat = np.zeros((5,6))


	for i in range(1,4):


		a1 = df[ (df['Question_number']==i) & (df['Dificult']==1) & (df['Topic']=='Encontro Vocalico') ] 
		a2 = df[ (df['Question_number']==i) & (df['Dificult']==2) & (df['Topic']=='Encontro Vocalico') ] 
		a3 = df[ (df['Question_number']==i) & (df['Dificult']==3) & (df['Topic']=='Encontro Vocalico') ] 
		a4 = df[ (df['Question_number']==i) & (df['Dificult']==4) & (df['Topic']=='Encontro Vocalico') ] 
		a5 = df[ (df['Question_number']==i) & (df['Dificult']==5) & (df['Topic']=='Encontro Vocalico') ] 
		
		mat[0,i-1] = len(a1.index)
		mat[1,i-1] = len(a2.index)
		mat[2,i-1] = len(a3.index)
		mat[3,i-1] = len(a4.index)
		mat[4,i-1] = len(a5.index)


	# for i in range(1,4):
	# 	print i+2
	
	# return

	for i in range(1,4):

		a1 = df[ (df['Question_number']==i) & (df['Dificult']==1) & (df['Topic']=='Digrafo') ] 
		a2 = df[ (df['Question_number']==i) & (df['Dificult']==2) & (df['Topic']=='Digrafo') ] 
		a3 = df[ (df['Question_number']==i) & (df['Dificult']==3) & (df['Topic']=='Digrafo') ] 
		a4 = df[ (df['Question_number']==i) & (df['Dificult']==4) & (df['Topic']=='Digrafo') ] 
		a5 = df[ (df['Question_number']==i) & (df['Dificult']==5) & (df['Topic']=='Digrafo') ] 
		
		mat[0,i+2] = len(a1.index)
		mat[1,i+2] = len(a2.index)
		mat[2,i+2] = len(a3.index)
		mat[3,i+2] = len(a4.index)
		mat[4,i+2] = len(a5.index)

	print mat 

	w =0

	cor = [ 'aqua', 'dodgerblue','b', 'darkviolet', 'indigo']
	cor2 = [ 'paleturquoise', 'cyan','springgreen', 'green', 'darkgreen']

	labels = range(1,6) 	
	
	plt.figure(1)
	x=range(1,7)

	#x = [1, 2, 3, 4, 5, 6]
	my_xticks = ["V.E. 1", "V.E. 2", "V.E. T3", "D. 1", "D. 5", "D. 6"]
	
	plt.xticks(x, my_xticks)

	print labels
	#return 
	for i in range(5):

		y = mat[i]
		plt.plot(x, y, 'o--', color=cor2[i], markersize=10, label=i+1)
		for a,b in zip(x, y): 
			plt.text(a+0.15, b-0.1, str(int(b)))	
			
			


		# for j in range(5):
		# 	x=(i-2*w)+1
		# 	y = mat[i,j]
		# 	plt.plot(x, y, '--', color=cor[j], markersize=10)
			# for a,b in zip(x, y): 
			# 	plt.text(a-0.05, b+1.5, str(b))
			

	plt.legend(title='Difficulty', loc='upper right', 
		numpoints = 1,
		shadow=True,
		handlelength=1.5, 
		fontsize=12)


	plt.xlim(0,7)
	plt.ylim(-1,33)

	plt.title("Questions' Difficulty Occurrences", fontsize=32)

	plt.xlabel("Topic_Question Number", fontsize=18)
	plt.ylabel("Number of occurrences", fontsize=22)
	plt.show()



def generate_pie():

	df = pd.read_csv("final_evals.csv")

	rights = df[ (df['System_was']==1) ]

	wrongs = df[ (df['System_was']==0) ]

	miss = df[ (df['System_was']==-1) ]

	r = len(rights.index)
	w = len(wrongs.index)
	m = len(miss.index)

	labels = ["Right Classification", "Wrong Classification", "Listening Problem"] 
	sizes = [r,w,m]
	colors = ['paleturquoise', 'lightcoral', 'lemonchiffon', 'gold', 'lightskyblue']
	explode = [0.1,0,0]
	#fig1, ax1 = plt.subplots()
	
	plt.rcParams['font.size'] = 16.0

	plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors= colors,
			shadow=True, startangle=90, explode=explode)
	
	plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	plt.title("System Overall Accuracy", fontsize=32)
	plt.show()

	print r,w,m

	ac = (float(r)/float(r+w))

	print ac






def hole():
	
	pass


if __name__=='__main__':
	
	#generate_graph()
	#generate_graph_frequency()
	generate_pie()
	
		# if(search_engine('bla'))=='':#, type(search_engine('santos').encode('utf-8'))
		# 	print "YES"