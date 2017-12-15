import hub as hb
import sys
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
x = hb.Hub()
app.exec_()