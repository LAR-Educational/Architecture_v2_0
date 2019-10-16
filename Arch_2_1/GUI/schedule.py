# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/GUI/meeting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import meeting

class Show_schedule(QtGui.QDialog, meeting.Ui_Dialog):

    def __init__(self, meeting, parent):
        #super(self.__class__, self).__init__()
        #super(self, parent).__init__()
        QtGui.QDialog.__init__(self, parent)

        self.meeting = meeting[0]

        self.setupUi(self)

        date = self.meeting.date
        weekday = date.toString('dddd')
        # date = date.toString('dddd, d of MMMM of yyyy')
        weekday = weekday.left(1).toUpper()+weekday.mid(1)
        day		= date.toString('dd')
        month 	= date.toString('MMMM')
        month = month.left(1).toUpper()+month.mid(1)
        year 	= date.toString('yyyy')
        self.md_label.setText(day)
        self.wd_label.setText(weekday)
        self.month_label.setText(month)
        self.year_label.setText(year)
        self.dateEdit.setDate(date)

        self.period_lineEdit.setText(self.meeting.period)
        self.place_lineEdit.setText(self.meeting.place)
        self.textEdit.setText(self.meeting.details)
        self.timeEdit.setTime(self.meeting.time)

    def save(self):

        #self.meeting.id
        self.meeting.date = self.dateEdit.date()
        self.meeting.time = self.timeEdit.time()
        self.meeting.period = str(self.period_lineEdit.text().toUtf8())
        self.meeting.place = str(self.place_lineEdit.text().toUtf8())
        self.meeting.details  = str(self.textEdit.toPlainText().toUtf8())   

    def accept(self):

        self.save()    
        self.done(QtGui.QDialog.Accepted)