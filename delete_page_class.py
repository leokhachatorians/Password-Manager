from db_init import session, Locker
import sys
from PyQt4 import QtCore, QtGui, uic


delete_page = uic.loadUiType("password_delete_page.ui")[0]

class DeletePage(QtGui.QDialog, delete_page):
	"""Window for whenever the user wishes to delete an existing entry"""

	def __init__(self, url, user, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.delete_button.clicked.connect(self.delete)
		self.exit_button.clicked.connect(self.exit)

		self.url = url
		self.user = user
		self.account = account

		#Display URL and USER selections and set to readonly
		self.url_delete_display.setText(url)
		self.url_delete_display.setReadOnly(True)

		self.user_delete_display.setText(user)
		self.user_delete_display.setReadOnly(True)

	def delete(self):
		session.query(Locker).filter_by(url=self.url,user=self.user,account=self.account).delete()
		session.commit()
		QtGui.QMessageBox.information(self,"Deleted","Sucessfully Deleted \n URL:[{}] \n USER:[{}]".format(self.url,self.user))
		self.close()

	def clear_input(self):
		#Clears input text area
		self.url_delete_display.clear()
		self.user_delete_display.clear()

	def exit(self):
		#Set displays to editable so when window reopens the displays are accurate
		self.clear_input()
		self.url_delete_display.setReadOnly(False)
		self.user_delete_display.setReadOnly(False)
		self.close()