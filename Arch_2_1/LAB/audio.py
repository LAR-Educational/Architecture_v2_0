# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import sys
from PyQt4 import QtCore, QtGui

try:
    from PyQt4.phonon import Phonon
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "Music Player",
            "Your Qt installation does not have Phonon support.",
            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
            QtGui.QMessageBox.NoButton)
    sys.exit(1)


app = QtGui.QApplication(sys.argv)
vp = Phonon.VideoPlayer()
media = Phonon.MediaSource('C:\\video.mp4')
vp.load(media)
vp.play()
vp.show()
sys.exit(app.exec_())