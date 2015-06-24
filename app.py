from classes.account_viewer_class import AccountViewer
from PyQt4 import QtGui
import sys

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	gui = AccountViewer()
	gui.show()
	gui.populate_manager()
	app.exec_()