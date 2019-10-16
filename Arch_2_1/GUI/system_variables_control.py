# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/GUI/meeting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import window_svc
from pprint import pprint

class Svc_Gui(QtGui.QDialog, window_svc.Ui_Dialog):

    def __init__(self, svc, parent):
        #super(self.__class__, self).__init__()
        #super(self, parent).__init__()
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


        self.svc = svc[0]
        aux = self.svc
        #pprint (vars(self.svc))

        self.userIdSpinBox.setValue(aux.users_id)
        self.sessionIdSpinBox.setValue(aux.session_id)
        self.evaluationIdSpinBox.setValue(aux.evaluation_id)
        self.interactionIdSpinBox.setValue(aux.interaction_id)
        self.filePathLineEdit.setText(aux.file_name)
        
        try:
            self.groupevalIdSpinBox.setValue(aux.group_eval_id)
            self.versionSpinBox.setValue(aux.version)
            self.meetingIdSpinBox.setValue(aux.meeting_id)
        except:
            print "Old version. It dosent have 'version' or 'group eval' field"
        

    def save(self):

        # pass
        self.svc.version = self.versionSpinBox.value()  
        self.svc.users_id = self.userIdSpinBox.value()  
        self.svc.evaluation_id = self.evaluationIdSpinBox.value()  
        self.svc.interaction_id = self.interactionIdSpinBox.value()  
        self.svc.session_id = self.sessionIdSpinBox.value()  
        self.svc.group_eval_id = self.groupevalIdSpinBox.value()          
        self.svc.meeting_id = self.meetingIdSpinBox.value()     

        self.svc.save()
        # self.meeting.id
        # self.meeting.date = self.dateEdit.date()
        # self.meeting.time = self.timeEdit.time()
        # self.meeting.period = str(self.period_lineEdit.text().toUtf8())
        # self.meeting.place = str(self.place_lineEdit.text().toUtf8())
        # self.meeting.details  = str(self.textEdit.toPlainText().toUtf8())   

    def accept(self):

        self.save()    
        self.done(QtGui.QDialog.Accepted)


# if __name__=="__main__":

#     svc = Svc_Gui(None,None)
#     svc.exec_()