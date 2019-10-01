import sys
import os
from PyQt4 import QtCore, QtGui
from PyQt4.phonon import Phonon
app = QtGui.QApplication(sys.argv)
print os.getcwd()
media = Phonon.MediaSource('LAB/tt.wav')
# media = Phonon.MediaSource('LAB/test.mp3')
# media = Phonon.MediaSource('/home/tozadore/Projects/Architecture_v2_0/Arch_2_1/LAB/test.avi')
vp = Phonon.VideoPlayer()
media = Phonon.MediaSource('LAB/abertura.mp4')
vp.load(media)
vp.play()
vp.show()
sys.exit(app.exec_())