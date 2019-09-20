import os
import pickle
import cPickle
import pandas as pd
from pprint import pprint








class SystemVariablesControl():
    def __init__(self):
       
        self.file_name = ".system_control.dat"
        self.users_id = None
        self.session_id = None
        self.evaluation_id = None
        self.interaction_id = None

       
        if os.path.exists(self.file_name):
            
            #print "File Exists"
            self.load()

        else:
            self.users_id = 18001
            self.session_id = 18001
            self.evaluation_id = 18001
            self.interaction_id = 18001
        
            self.save()



    def reset_vals(self):
        
        self.users_id = 18001
        self.session_id = 18001
        self.evaluation_id = 18001
        self.interaction_id = 18001
        
     

    
    
    def printClass(self):
        pprint(vars(self))


    def load(self):
        f = open(self.file_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()

        print tmp_dict          

        self.__dict__.update(tmp_dict) 


    def save(self):
        f = open(self.file_name, 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()


    def add(self, att):

        if(att=='user'):
            self.users_id+=1
        elif(att=='interaction'):
            self.interaction_id+=1
        elif(att=='session'):
            self.session_id+=1
        elif(att=='evaluation'):
            self.evaluation_id+=1
        else:
            raise NameError('Variable "' + att +'" unkwon in add System Variables')
            #return False    
            
        self.save()    







def save(svc):
    print "Saving"
    with open(svc.file_name, 'wb') as f:
        pickle.dump(svc, f, pickle.HIGHEST_PROTOCOL)


def load(svc):
    print "Loading"
    with open(svc.file_name, 'rb+') as f:
        return pickle.load(f)


# class SystemVariablesControl():
#     def __init__(self):
        
#         self.file_name = ".system_control.csv"
#         self.
#         if os.path.exists(self.file_name):
            

#         else:
                








def old_main():

    svc = SystemVariablesControl()

   
    svc.printClass()

    print "dps"
   
    try:
       svc.add('evalua')
       pass
    except Exception as inst:
        print(inst.args)     # arguments stored in .args
        print(type(inst))    # the exception instance
        print(inst)

    #svc.save()

    svc.printClass()

    return

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
class MyApp(QMainWindow):
	

    def __init__(self):
        super(self.__class__, self).__init__()
        app_icon = QIcon()
        app_icon.addFile('../GUI/Logo.png', QSize(16,16))
        app_icon.addFile('../GUI/Logo.png', QSize(24,24))
        app_icon.addFile('../GUI/Logo.png', QSize(32,32))
        app_icon.addFile('../GUI/Logo.png', QSize(48,48))
        app_icon.addFile('vectors.png', QSize(256,256))
        # self.setWindowIcon(QIcon('/GUI/R_CASTLE_Logo.jpeg'))

        print "path", os.getcwd()

        self.setWindowIcon(app_icon)
        self.setWindowTitle("HOLA")
        self.setGeometry(450,350,500,300)
        
        self.centralwidget = QWidget(self)
        #self.centralwidget.setGeometry(50,0, 50,50)
        #addWidget(QLabel("ROLA"))
        self.frame_17 = QFrame(self.centralwidget)
        #self.frame_17 = QFrame(self)
        #self.gridLayoutr = QGridLayout(self)   
        self.v = QVBoxLayout(self.frame_17)
        lab = QLabel("HOla")
        lab.setMinimumSize(QSize(320, 240))
        lab.setPixmap(QPixmap('GUI/Logo.png'))     
        # lab.setPixmap(QPixmap('/GUI/Logo.png'))     
        #lab.setFixedSize(300,300)  
        lab.setScaledContents(True)   
        self.v.addWidget(lab)
        #self.
        #self.label_27.setPixmap(QPixmap('/GUI/Logo.png'))
        #self.setLayout()


def main():
    a = QApplication(sys.argv)  # A new instance of QApplication
    w = MyApp()
    w.show()
    a.exec_()



if __name__=="__main__":
    main()   











