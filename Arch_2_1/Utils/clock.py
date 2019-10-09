
import os
import pandas as pd
from PyQt4 import QtCore, QtGui
from pprint import pprint

class Appoitment:

    def __init__(self, _id, date, time, period = "", place = "", details=""):

        self.id = _id
        self.date = date

        weekday = date.toString('dddd')
        # date = date.toString('dddd, d of MMMM of yyyy')
        self.wday = weekday.left(1).toUpper()+weekday.mid(1)
        self.day		= date.toString('dd')
        month 	= date.toString('MMMM')
        self.month = month.left(1).toUpper()+month.mid(1)

        self.year 	= date.toString('yyyy')

        self.time = time
        self.place = place
        self.details = details
        self.period = period




class Schedule:

    def __init__(self):

        self.path = "Schedule/"
        self.table_name = self.path + "schedule.csv"
        # self.meetings_table = self.path + "/schedule.csv"
        self.meetings_list = []
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)


        if os.path.exists(self.table_name):
            # self.meetings_table = pd.DataFrame()
            self.meetings_table = pd.read_csv(self.table_name)
            
            self.load_meetings_list()
            
        else:  
            #os.mkdir(self.path)  
            self.meetings_table = pd.DataFrame(columns=['Id', 'Date', 'Time', 'Period','Place','Details'])
            #print self.meetings_table
            self.meetings_table.to_csv(self.table_name, index=False)

        
        
        
        self.size = len(self.meetings_table.index)

        #print self.meetings_table


    def add_meeting(self, aux):
        self.meetings_list.append(aux)
    
    def del_meeting(self, date):
        
        for i, o in enumerate(self.meetings_list):
            if o.date == date:
                del self.meetings_list[i]
                print "DONE"
                break
        
        #self.meetings_list = self.meetings_list[self.meetings_list['Date'] != aux.date]
        self.save_meetings_list()

       
    def load_meetings_list(self):
        
        for index, row in self.meetings_table.head().iterrows():

           date = QtCore.QDate.fromString(row['Date'],'dd/MM/yyyy') 
           time = QtCore.QTime.fromString(row['Time'],'hh:mm') 
           
           # Workarround for NaN's .... 
           period = row['Period']
           if period != period:
               period = ""

           place = row['Place']
           if place != place:
               place = ""
           
           details= row['Details']
           if details != details:
               details = ""

           aux = Appoitment(row['Id'],date , time, period, place, details)
           #pprint(vars(aux)) 

           self.meetings_list.append(aux)
        
        
        
        
    def save_meetings_list(self):
        
        aux = pd.DataFrame(columns=['Id', 'Date', 'Time', 'Period','Place','Details'])
        #print type(aux.period)
        i=0
       
        for item in self.meetings_list:
            
            # aux = Appoitment(row['Id'],row['Date'], row['Time'], row['Period'],row['Place'],'row[Details'])
            date = item.date.toString('dd/MM/yyyy')
            time = item.time.toString('hh:mm')
            period = str(item.period)#.toUtf8())
            place = str(item.place)#.toUtf8())
            details = str(item.details)#.toUtf8())
            row = [item.id, date, time, period, place, details]   
            aux.loc[i] = row
            aux.index +1
            # aux.sort_index()
            i+=1

        aux.to_csv(self.table_name, index=False)
     

    def get_meeting(self, _id):

        for item in self.meetings_list:

            if item.id == _id:
                return item

        return None


class AnalogClock(QtGui.QWidget):
    hourHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -40)
    ])

    minuteHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -70)
    ])

    hourColor = QtGui.QColor(127, 0, 127)
    minuteColor = QtGui.QColor(0, 127, 127, 191)

    def __init__(self, w=150, h=150, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        #self.setWindowTitle("Analog Clock")
        self.resize(w, h)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()

        painter.setPen(AnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()

        painter.setPen(AnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)



class DigitalClock(QtGui.QLCDNumber):
    def __init__(self, w=150, h=40, parent=None):
        super(DigitalClock, self).__init__(parent)

        self.setSegmentStyle(QtGui.QLCDNumber.Filled)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.showTime()

        self.setWindowTitle("Digital Clock")
        self.resize(w, h)

    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.display(text)


class MyCalendar(QtGui.QCalendarWidget):

    def _init_(self, meetings = None):
        
        if meetings is None:
            self.meetings = []
        else:
            self.meetings = meetings

        self.setVerticalHeaderFormat(QtGui.QCalendarWidget.VerticalHeaderFormat.numerator)

    def add_meeting(self, metting):
        try:
            self.meetings.append(metting)
        except:
            self.meetings=[]
            self.meetings.append(metting)
        finally:
            self.updateCell(metting)


    def clear_meetings(self):
        self.meetings =[]



    def paintCell(self, painter, rect, date):
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

            #for item in day_list:
            #day_list = []
            
            # if (date.day() in day_list):
            try:
                if (date in self.meetings):
                # if (date.day() ==5):
                    painter.save()
                    painter.drawRect(rect)
                    painter.setPen(QtCore.Qt.blue)
                    painter.drawText(QtCore.QRectF(rect), QtCore.Qt.TextSingleLine|QtCore.Qt.AlignCenter, str(date.day()))
                    painter.restore()
                else:
                    QtGui.QCalendarWidget.paintCell(self, painter, rect, date)
            
            except:
                QtGui.QCalendarWidget.paintCell(self, painter, rect, date)
            




if __name__ == '__main__':

    import sys

    # app = QtGui.QApplication(sys.argv)
    # # clock = AnalogClock()
    # clock = DigitalClock()
    # clock.show()
    # sys.exit(app.exec_())