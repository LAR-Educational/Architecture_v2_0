# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/GUI/opening.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

#from PyQt4 import QtCore, QtGui
import opening
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocessing import Queue, Process
import threading



class My_Loading(QDialog, opening.Ui_Dialog):

    def __init__(self):
        super(self.__class__, self).__init__()


        self.setupUi(self)
        self.label.setPixmap(QPixmap("GUI/OpenLogo.jpeg"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        #self.text_update()
        self.timer.start(25)

    def update(self):    
        "Function ot only plot more points"

        # text =self.label_2.text()
        # text +="."
        # print text
        # self.label_2.setText(text)
        if (self.progressBar.value()==100):
            self.close()
        self.progressBar.setValue(self.progressBar.value()+1)



class MyApp(Process):

    def __init__(self, window_type):
        self.queue = Queue(1)
        self.type = window_type
        super(MyApp, self).__init__()

    def run(self):
        app = QApplication([])
        if self.type == 'opening':
            d =  My_Loading()
        d.show()
        app.exec_()                         # and execute the app

       # self.queue.put("return_value")



if __name__=="__main__":

    app1 = MyApp('opening')
    app1.start()

    app2 = MyApp(My_Loading())
    app2.start()
    app2.join()

    app1.join()
    print("App 1 returned: " + app1.queue.get())
    print("App 2 returned: " + app2.queue.get())



    # def openDiag():
    #     print "HI"
    #     app = QApplication([])  # A new instance of QApplication
    #     d = My_Loading()
    #     d.show()
    #     app.exec_()                         # and execute the app

    # #openDiag()

    # st = threading.Thread(target=openDiag)
    # #st.started.connect(openDiag)
    # st.start()    
    # print "Finished"
        









