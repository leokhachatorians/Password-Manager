import sys
from PyQt4 import QtCore, QtGui, uic

about_page = uic.loadUiType("pages/about_page.ui")[0]

class AboutPage(QtGui.QDialog, about_page):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)