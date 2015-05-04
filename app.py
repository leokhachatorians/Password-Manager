from main_page_class import MainWindow
from PyQt4 import QtGui
import sys

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	gui = MainWindow()
	gui.show()
	gui.refresh()
	app.exec_()
