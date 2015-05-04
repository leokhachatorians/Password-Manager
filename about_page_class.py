import sys
from PyQt4 import QtCore, QtGui, uic

about_page = uic.loadUiType("about_page.ui")[0]

class AboutPage(QtGui.QDialog, about_page):
	"""The 'about' window"""

	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
