from db_init import session, Locker
import sys
from PyQt4 import QtCore, QtGui, uic


password_modify_page = uic.loadUiType("password_modify_page.ui")[0]

class ModifyPasswordPage(QtGui.QDialog, password_modify_page):
	"""Window for when the user determines to modify their prior password"""

	def __init__(self, url, user, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)

		# Button Actions
		self.save_button.clicked.connect(self.modify)
		self.exit_button.clicked.connect(self.exit)

		self.url = url
		self.user = user
		self.account = account

		# Set UserName and Password displays
		self.url_display.setText(url)
		self.url_display.setReadOnly(True)

		self.user_display.setText(user)
		self.user_display.setReadOnly(True)


	def check_if_empty_string(self, url='null', user='null', password='null'):
		if not url or not url.strip() or not user or not user.strip() or not password or not password.strip():
			return True


	def modify(self):
		modify_url = str(self.url_display.text())
		modify_user = str(self.user_display.text())
		modify_password = str(self.password_input.text())

		if self.check_if_empty_string(modify_url, modify_user, modify_password):
			QtGui.QMessageBox.warning(
				self, "Invalid Entry", "Make sure you input a password.")
		else:
			new = session.query(Locker).filter_by(url=self.url,user=self.user,account=self.account).one()
			new.url = modify_url
			new.user = modify_user
			new.password = modify_password
			session.commit()
			QtGui.QMessageBox.information(self, "Completed", "Succesfully Updated \n URL:[{}] \n USER:[{}] \n PASSWORD:[{}]".format(modify_url, modify_user, (len(modify_password) * '*')))
			self.exit()

	def clear_input(self):
		#Clears input text area
		self.url_display.clear()
		self.user_display.clear()

	def exit(self):
		#Set displays to editable so when window reopens the displays are accurate
		self.clear_input()
		self.url_display.setReadOnly(False)
		self.user_display.setReadOnly(False)
		self.close()