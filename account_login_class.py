from account_db_init import session, Accounts
from main_page_class import MainWindow
import sys
from PyQt4 import QtCore, QtGui, uic

account_login_page = uic.loadUiType("account_login_page.ui")[0]

class AccountLogin(QtGui.QMainWindow, account_login_page):

	def __init__(self, account, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.account = account

		# Button actions
		self.save_button.clicked.connect(self.login_check)
		self.exit_button.clicked.connect(self.exit)

		# Display account variable, make sure to set to read only
		self.account_display.setText(account)
		self.account_display.setReadOnly(True)

		# Open main window check
		self.main_window = None

	def login_check(self):
		account = self.account_display.text()
		password = self.password_input.text()
		if session.query(Accounts).filter_by(account=account, password=password).count() == 1:
			if self.main_window is None:
				self.main_window = MainWindow(account)
			self.main_window.show()
			self.exit()
		else:
			QtGui.QMessageBox.information(self, "Invalid","You entered the wrong password")


	def exit(self):
		self.close()
